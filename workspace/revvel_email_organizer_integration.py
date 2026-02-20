#!/usr/bin/env python3

import os
import sys
import json
import logging
from typing import Dict, List, Any

class RevvelEmailOrganizerIntegrator:
    def __init__(self, config_path: str):
        """
        Initialize comprehensive email organizer integration
        
        Args:
            config_path (str): Path to integration configuration
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize integration components
        self.components = {
            'security': self._initialize_security(),
            'ml_classifier': self._initialize_ml_classifier(),
            'email_processor': self._initialize_email_processor(),
            'database': self._initialize_database()
        }

    def _setup_logging(self):
        """Configure comprehensive logging system"""
        log_dir = '/var/log/revvel_email_organizer/integration'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/integration.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('EmailOrganizerIntegration')

    def _initialize_security(self) -> Dict[str, Any]:
        """
        Initialize security components
        
        Returns:
            Dict with security initialization details
        """
        try:
            from cryptography.fernet import Fernet
            
            return {
                'encryption_key': Fernet.generate_key(),
                'status': 'initialized'
            }
        except ImportError:
            self.logger.error("Cryptography library not found")
            return {'status': 'error', 'message': 'Cryptography library missing'}

    def _initialize_ml_classifier(self) -> Dict[str, Any]:
        """
        Initialize machine learning classifier
        
        Returns:
            Dict with ML classifier initialization details
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.ensemble import RandomForestClassifier
            
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=5000
            )
            
            classifier = RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
            
            return {
                'vectorizer': vectorizer,
                'classifier': classifier,
                'status': 'initialized'
            }
        except ImportError:
            self.logger.error("Machine learning libraries not found")
            return {'status': 'error', 'message': 'ML libraries missing'}

    def _initialize_email_processor(self) -> Dict[str, Any]:
        """
        Initialize email processing components
        
        Returns:
            Dict with email processor initialization details
        """
        try:
            import mailparser
            
            return {
                'supported_formats': ['mbox', 'eml', 'msg'],
                'parser': mailparser,
                'status': 'initialized'
            }
        except ImportError:
            self.logger.error("Email parsing library not found")
            return {'status': 'error', 'message': 'Email parsing library missing'}

    def _initialize_database(self) -> Dict[str, Any]:
        """
        Initialize database connection
        
        Returns:
            Dict with database initialization details
        """
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            
            # Create database engine
            engine = create_engine(
                self.config['database']['connection_string'],
                pool_size=20,
                max_overflow=10
            )
            
            # Create session factory
            SessionLocal = sessionmaker(bind=engine)
            
            return {
                'engine': engine,
                'session_factory': SessionLocal,
                'status': 'initialized'
            }
        except ImportError:
            self.logger.error("Database libraries not found")
            return {'status': 'error', 'message': 'Database libraries missing'}

    def validate_integration(self) -> Dict[str, Any]:
        """
        Validate integration of all components
        
        Returns:
            Dict with integration validation results
        """
        validation_results = {}
        
        for component, details in self.components.items():
            validation_results[component] = (
                details['status'] == 'initialized'
            )
        
        return {
            'overall_status': all(validation_results.values()),
            'component_status': validation_results
        }

    def perform_integration_tests(self) -> Dict[str, Any]:
        """
        Run comprehensive integration tests
        
        Returns:
            Dict with integration test results
        """
        test_results = {
            'security_test': self._run_security_test(),
            'ml_classification_test': self._run_ml_test(),
            'email_processing_test': self._run_email_processing_test(),
            'database_test': self._run_database_test()
        }
        
        return {
            'overall_test_status': all(
                result['status'] == 'passed' 
                for result in test_results.values()
            ),
            'test_results': test_results
        }

    def _run_security_test(self) -> Dict[str, Any]:
        """
        Run security component integration test
        
        Returns:
            Dict with security test results
        """
        try:
            from cryptography.fernet import Fernet
            
            key = self.components['security']['encryption_key']
            f = Fernet(key)
            
            test_message = b"Test security integration"
            encrypted = f.encrypt(test_message)
            decrypted = f.decrypt(encrypted)
            
            return {
                'status': 'passed' if decrypted == test_message else 'failed',
                'message': 'Encryption/decryption test completed'
            }
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}

    def _run_ml_test(self) -> Dict[str, Any]:
        """
        Run machine learning component integration test
        
        Returns:
            Dict with ML test results
        """
        try:
            vectorizer = self.components['ml_classifier']['vectorizer']
            classifier = self.components['ml_classifier']['classifier']
            
            # Dummy test data
            test_texts = [
                "This is a test email about work",
                "Personal email discussing family",
                "Promotional email about products"
            ]
            
            # Vectorize test data
            X_test = vectorizer.fit_transform(test_texts)
            
            # Dummy training
            y_train = [0, 1, 2]  # Dummy labels
            classifier.fit(X_test, y_train)
            
            return {
                'status': 'passed',
                'message': 'ML classifier integration test completed'
            }
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}

    def _run_email_processing_test(self) -> Dict[str, Any]:
        """
        Run email processing component integration test
        
        Returns:
            Dict with email processing test results
        """
        try:
            parser = self.components['email_processor']['parser']
            
            # Dummy test email
            test_email = b"""
            From: test@example.com
            Subject: Test Email
            
            This is a test email body.
            """
            
            # Parse test email
            parsed_email = parser.parse_from_bytes(test_email)
            
            return {
                'status': 'passed',
                'message': 'Email processing integration test completed',
                'parsed_subject': parsed_email.subject
            }
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}

    def _run_database_test(self) -> Dict[str, Any]:
        """
        Run database component integration test
        
        Returns:
            Dict with database test results
        """
        try:
            SessionLocal = self.components['database']['session_factory']
            
            with SessionLocal() as session:
                # Dummy database operation
                result = session.execute("SELECT 1")
                
            return {
                'status': 'passed',
                'message': 'Database connection test completed'
            }
        except Exception as e:
            return {'status': 'failed', 'message': str(e)}

def main():
    # Path to integration configuration
    config_path = "/home/openclaw/.openclaw/workspace/revvel_email_organizer_config.json"
    
    # Initialize integrator
    integrator = RevvelEmailOrganizerIntegrator(config_path)
    
    # Validate integration
    validation_results = integrator.validate_integration()
    print("Integration Validation:")
    print(json.dumps(validation_results, indent=2))
    
    # Run integration tests
    test_results = integrator.perform_integration_tests()
    print("\nIntegration Tests:")
    print(json.dumps(test_results, indent=2))

if __name__ == "__main__":
    main()