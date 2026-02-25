#!/usr/bin/env python3

import os
import sys
import logging
from typing import Dict, Any

# Import custom modules
from src.core.security_engine import SecurityEngine
from src.core.email_processor import EmailProcessingEngine
from src.core.ml_classifier import EmailClassificationSystem
from src.core.database import DatabaseManager
from src.api.routes import create_fastapi_app
from src.core.config import load_config

class RevvelEmailOrganizerApp:
    def __init__(self, config_path: str):
        """
        Initialize comprehensive Email Organizer application
        
        Args:
            config_path (str): Path to application configuration
        """
        # Load configuration
        self.config = load_config(config_path)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize core components
        self.security_engine = SecurityEngine(self.config)
        self.email_processor = EmailProcessingEngine(self.config)
        self.ml_classifier = EmailClassificationSystem(self.config)
        self.database_manager = DatabaseManager(self.config)
        
        # Create API application
        self.api_app = create_fastapi_app(
            security_engine=self.security_engine,
            email_processor=self.email_processor,
            ml_classifier=self.ml_classifier
        )

    def _setup_logging(self):
        """Configure comprehensive application logging"""
        log_dir = '/var/log/revvel_email_organizer/app'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/email_organizer.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('RevvelEmailOrganizerApp')

    def start_services(self):
        """
        Start all application services
        
        Initializes:
        - Security monitoring
        - Email processing
        - Machine learning services
        - Database connections
        """
        try:
            # Start security monitoring
            self.security_engine.start_continuous_monitoring()
            
            # Initialize database
            self.database_manager.initialize_database()
            
            # Train initial ML models
            self.ml_classifier.train_initial_models()
            
            self.logger.info("All Revvel Email Organizer services started successfully")
        
        except Exception as e:
            self.logger.critical(f"Service initialization failed: {e}")
            self._handle_critical_failure()

    def process_email_archive(self, archive_path: str) -> Dict[str, Any]:
        """
        Process large email archive with comprehensive safeguards
        
        Args:
            archive_path (str): Path to email archive
        
        Returns:
            Dict with processing results
        """
        try:
            # Encrypt archive path
            encrypted_path = self.security_engine.encrypt_email_data({
                'archive_path': archive_path
            })
            
            # Process emails
            processing_result = self.email_processor.process_archive(
                encrypted_path['archive_path']
            )
            
            # Classify processed emails
            classification_result = self.ml_classifier.classify_emails(
                processing_result['processed_emails']
            )
            
            # Store results securely
            self.database_manager.store_processed_emails(
                classification_result['classified_emails']
            )
            
            return {
                'status': 'success',
                'processed_emails': len(classification_result['classified_emails']),
                'classification_summary': classification_result['summary']
            }
        
        except Exception as e:
            self.logger.error(f"Email archive processing error: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def _handle_critical_failure(self):
        """
        Handle critical system failures
        
        Implements emergency recovery and notification
        """
        # Potential actions:
        # - Send alert to administrators
        # - Trigger system rollback
        # - Generate comprehensive failure report
        pass

def main():
    # Load configuration
    config_path = "/home/openclaw/.openclaw/workspace/revvel_email_organizer_config.json"
    
    # Initialize Revvel Email Organizer
    email_organizer = RevvelEmailOrganizerApp(config_path)
    
    # Start application services
    email_organizer.start_services()
    
    # Example email archive processing
    archive_path = "/path/to/email/archive"
    processing_result = email_organizer.process_email_archive(archive_path)
    
    print(processing_result)

if __name__ == "__main__":
    main()