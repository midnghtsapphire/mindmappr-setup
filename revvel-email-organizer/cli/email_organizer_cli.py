#!/usr/bin/env python3

import os
import sys
import argparse
import json
import logging
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.email_processor import EmailProcessor
from config.openrouter_access import OpenRouterAccessManager

class EmailOrganizerCLI:
    def __init__(self):
        """
        Initialize CLI with configuration and logging
        """
        self._setup_logging()
        self.openrouter_manager = OpenRouterAccessManager()
        self.email_processor = None

    def _setup_logging(self):
        """
        Configure CLI logging
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('EmailOrganizerCLI')

    def process_archive(self, archive_path: str, config: Dict[str, Any] = None):
        """
        Process email archive from CLI
        
        Args:
            archive_path (str): Path to email archive
            config (Dict, optional): Processing configuration
        """
        try:
            # Default configuration
            default_config = {
                'privacy': {
                    'anonymize': True,
                    'retention_days': 30
                },
                'logging': {
                    'level': 'INFO'
                }
            }
            
            # Merge user config with default
            if config:
                default_config.update(config)
            
            # Initialize processor
            self.email_processor = EmailProcessor(default_config)
            
            # Process archive
            result = self.email_processor.process_archive(archive_path)
            
            # Output results
            print(json.dumps(result, indent=2))
        
        except Exception as e:
            self.logger.error(f"Email archive processing failed: {e}")
            sys.exit(1)

    def generate_token(self, app_name: str):
        """
        Generate application-specific token
        
        Args:
            app_name (str): Name of the application
        """
        try:
            token = self.openrouter_manager.generate_app_specific_token(app_name)
            print(json.dumps(token, indent=2))
        except Exception as e:
            self.logger.error(f"Token generation failed: {e}")
            sys.exit(1)

    def list_models(self):
        """
        List available OpenRouter models
        """
        try:
            models = self.openrouter_manager.call_openrouter_api('models')
            print(json.dumps(models, indent=2))
        except Exception as e:
            self.logger.error(f"Model listing failed: {e}")
            sys.exit(1)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Revvel Email Organizer CLI')
    
    # Define subcommands
    subparsers = parser.add_subparsers(dest='command', help='CLI Commands')
    
    # Process archive command
    process_parser = subparsers.add_parser('process', help='Process email archive')
    process_parser.add_argument('archive_path', help='Path to email archive')
    process_parser.add_argument('--config', type=json.loads, help='JSON configuration')
    
    # Token generation command
    token_parser = subparsers.add_parser('token', help='Generate application-specific token')
    token_parser.add_argument('app_name', help='Name of the application')
    
    # List models command
    subparsers.add_parser('models', help='List available OpenRouter models')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize CLI
    cli = EmailOrganizerCLI()
    
    # Execute command
    if args.command == 'process':
        cli.process_archive(args.archive_path, args.config)
    elif args.command == 'token':
        cli.generate_token(args.app_name)
    elif args.command == 'models':
        cli.list_models()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()