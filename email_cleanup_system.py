#!/usr/bin/env python3

import os
import re
import json
import logging
from typing import Dict, List, Any, Optional
import hashlib
import email
import mailbox
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dateutil.parser import parse
import concurrent.futures

class EmailCleanupSystem:
    def __init__(self, input_path: str, output_path: str):
        """
        Initialize Email Cleanup System
        
        Args:
            input_path (str): Path to input email archive
            output_path (str): Path for cleaned email archive
        """
        self.input_path = input_path
        self.output_path = output_path
        
        # Configure logging
        logging.basicConfig(
            filename=os.path.join(output_path, 'email_cleanup.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger('EmailCleanup')
        
        # Cleanup configuration
        self.config = {
            'duplicate_threshold': 0.85,  # Similarity threshold for duplicates
            'spam_threshold': 0.7,  # Spam classification threshold
            'min_email_length': 50,  # Minimum characters to consider
            'keep_recent_months': 24  # Keep emails from last 24 months
        }
        
        # Create output directories
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(os.path.join(output_path, 'processed'), exist_ok=True)
        os.makedirs(os.path.join(output_path, 'spam'), exist_ok=True)

    def process_email_archive(self) -> Dict[str, Any]:
        """
        Comprehensive email archive processing
        
        Returns:
            Dict with cleanup statistics and summary
        """
        try:
            # Detect email archive type
            archive_type = self._detect_archive_type(self.input_path)
            
            # Load emails
            emails = self._load_emails(self.input_path, archive_type)
            
            # Preprocessing
            processed_emails = self._preprocess_emails(emails)
            
            # Deduplication
            deduplicated_emails = self._remove_duplicates(processed_emails)
            
            # Spam filtering
            cleaned_emails, spam_emails = self._filter_spam(deduplicated_emails)
            
            # Save processed emails
            self._save_processed_emails(cleaned_emails, spam_emails)
            
            # Generate cleanup report
            cleanup_report = self._generate_cleanup_report(
                emails, 
                processed_emails, 
                cleaned_emails, 
                spam_emails
            )
            
            return cleanup_report
        
        except Exception as e:
            self.logger.error(f"Email archive processing error: {e}")
            return {"status": "error", "message": str(e)}

    def _detect_archive_type(self, input_path: str) -> str:
        """
        Detect email archive type
        
        Supports:
        - Mailbox (MBOX)
        - Outlook PST
        - Individual .eml files
        """
        if input_path.lower().endswith('.mbox'):
            return 'mbox'
        elif input_path.lower().endswith('.pst'):
            return 'pst'
        elif os.path.isdir(input_path) and any(f.lower().endswith('.eml') for f in os.listdir(input_path)):
            return 'eml_directory'
        else:
            raise ValueError("Unsupported email archive format")

    def _load_emails(self, input_path: str, archive_type: str) -> List[Dict[str, Any]]:
        """
        Load emails from various archive types
        
        Standardizes email representation
        """
        emails = []
        
        if archive_type == 'mbox':
            mbox = mailbox.mbox(input_path)
            for msg in mbox:
                emails.append(self._parse_email_message(msg))
        
        elif archive_type == 'eml_directory':
            for filename in os.listdir(input_path):
                if filename.lower().endswith('.eml'):
                    with open(os.path.join(input_path, filename), 'rb') as f:
                        msg = email.message_from_binary_file(f)
                        emails.append(self._parse_email_message(msg))
        
        elif archive_type == 'pst':
            # Placeholder for PST processing
            # Would use a library like libpst
            raise NotImplementedError("PST processing not yet implemented")
        
        return emails

    def _parse_email_message(self, msg: email.message.Message) -> Dict[str, Any]:
        """
        Parse email message into standardized dictionary
        
        Extracts key metadata and content
        """
        try:
            # Extract email content
            body = self._extract_email_body(msg)
            
            return {
                'message_id': msg.get('Message-ID', ''),
                'subject': msg.get('Subject', ''),
                'from': msg.get('From', ''),
                'to': msg.get('To', ''),
                'date': msg.get('Date', ''),
                'body': body,
                'hash': hashlib.md5(body.encode()).hexdigest()
            }
        except Exception as e:
            self.logger.warning(f"Email parsing error: {e}")
            return {}

    def _extract_email_body(self, msg: email.message.Message) -> str:
        """
        Extract email body with preference for plain text
        
        Handles multipart messages
        """
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')
        
        # Basic text cleaning
        body = re.sub(r'\s+', ' ', body).strip()
        return body

    def _preprocess_emails(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Preprocess emails
        
        Filters based on length, recency
        """
        processed_emails = []
        current_time = datetime.now()
        
        for email_data in emails:
            # Filter by minimum length
            if len(email_data.get('body', '')) < self.config['min_email_length']:
                continue
            
            # Filter by recency
            try:
                email_date = parse(email_data.get('date', ''))
                months_ago = (current_time - email_date).days / 30
                
                if months_ago > self.config['keep_recent_months']:
                    continue
            except:
                # If date parsing fails, skip
                continue
            
            processed_emails.append(email_data)
        
        return processed_emails

    def _remove_duplicates(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Advanced duplicate removal
        
        Uses content-based similarity and hash matching
        """
        # Hash-based exact duplicate removal
        unique_hashes = set()
        unique_emails = []
        
        for email_data in emails:
            email_hash = email_data['hash']
            if email_hash not in unique_hashes:
                unique_hashes.add(email_hash)
                unique_emails.append(email_data)
        
        # TF-IDF based near-duplicate detection
        vectorizer = TfidfVectorizer(stop_words='english')
        email_texts = [email['body'] for email in unique_emails]
        
        if len(email_texts) > 1:
            tfidf_matrix = vectorizer.fit_transform(email_texts)
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            near_duplicate_indices = set()
            for i in range(len(similarity_matrix)):
                for j in range(i+1, len(similarity_matrix)):
                    if similarity_matrix[i][j] > self.config['duplicate_threshold']:
                        # Mark the later email as a duplicate
                        near_duplicate_indices.add(j)
            
            # Remove near duplicates
            deduplicated_emails = [
                email for idx, email in enumerate(unique_emails)
                if idx not in near_duplicate_indices
            ]
        else:
            deduplicated_emails = unique_emails
        
        return deduplicated_emails

    def _filter_spam(self, emails: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Intelligent spam filtering
        
        Uses multiple heuristics for classification
        """
        spam_keywords = [
            'unsubscribe', 'marketing', 'promotion', 
            'advertisement', 'bulk', 'newsletter'
        ]
        
        cleaned_emails = []
        spam_emails = []
        
        for email_data in emails:
            spam_score = 0
            
            # Keyword-based spam detection
            spam_score += sum(
                1 for keyword in spam_keywords 
                if keyword in email_data['body'].lower()
            )
            
            # Sender reputation (basic heuristic)
            sender_domain = email_data.get('from', '').split('@')[-1].lower()
            spam_domains = ['marketing.com', 'bulk.com', 'newsletter.net']
            if any(domain in sender_domain for domain in spam_domains):
                spam_score += 2
            
            # Normalize spam score
            normalized_spam_score = spam_score / len(spam_keywords)
            
            if normalized_spam_score > self.config['spam_threshold']:
                spam_emails.append(email_data)
            else:
                cleaned_emails.append(email_data)
        
        return cleaned_emails, spam_emails

    def _save_processed_emails(self, cleaned_emails: List[Dict[str, Any]], spam_emails: List[Dict[str, Any]]):
        """
        Save processed emails to output directories
        """
        # Save cleaned emails
        processed_mbox = mailbox.mbox(os.path.join(self.output_path, 'processed', 'cleaned_emails.mbox'))
        for email_data in cleaned_emails:
            msg = email.message.EmailMessage()
            msg.set_content(email_data['body'])
            for key in ['subject', 'from', 'to', 'date']:
                msg[key] = email_data.get(key, '')
            processed_mbox.add(msg)
        processed_mbox.close()
        
        # Save spam emails
        spam_mbox = mailbox.mbox(os.path.join(self.output_path, 'spam', 'spam_emails.mbox'))
        for email_data in spam_emails:
            msg = email.message.EmailMessage()
            msg.set_content(email_data['body'])
            for key in ['subject', 'from', 'to', 'date']:
                msg[key] = email_data.get(key, '')
            spam_mbox.add(msg)
        spam_mbox.close()

    def _generate_cleanup_report(self, 
                                  original_emails: List[Dict[str, Any]], 
                                  processed_emails: List[Dict[str, Any]], 
                                  cleaned_emails: List[Dict[str, Any]], 
                                  spam_emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive cleanup report
        """
        return {
            "status": "success",
            "original_email_count": len(original_emails),
            "processed_email_count": len(processed_emails),
            "cleaned_email_count": len(cleaned_emails),
            "spam_email_count": len(spam_emails),
            "deduplication_rate": 1 - (len(cleaned_emails) / len(processed_emails)),
            "spam_rate": len(spam_emails) / len(original_emails),
            "output_paths": {
                "cleaned_emails": os.path.join(self.output_path, 'processed', 'cleaned_emails.mbox'),
                "spam_emails": os.path.join(self.output_path, 'spam', 'spam_emails.mbox')
            }
        }

def main():
    # Example usage
    input_path = "/path/to/your/email/archive.mbox"
    output_path = "/path/to/cleaned/email/archive"
    
    email_cleanup = EmailCleanupSystem(input_path, output_path)
    cleanup_report = email_cleanup.process_email_archive()
    
    print(json.dumps(cleanup_report, indent=2))

if __name__ == "__main__":
    main()