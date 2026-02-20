#!/usr/bin/env python3

import os
import sys
import json
import logging
import requests
from typing import Dict, Any, Optional

class OpenRouterAccessManager:
    def __init__(self, config_path: str = None):
        """
        Manage OpenRouter API access and token management
        
        Args:
            config_path (str, optional): Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize API access
        self.api_key = self._get_api_key()
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from file or environment
        
        Args:
            config_path (str, optional): Path to config file
        
        Returns:
            Dict with configuration
        """
        # Default configuration
        default_config = {
            'openrouter': {
                'api_key_env': 'OPENROUTER_API_KEY',
                'base_url': 'https://openrouter.ai/api/v1',
                'app_name': 'Revvel Email Organizer',
                'app_url': 'https://revvel.com'
            },
            'token_management': {
                'rotation_days': 90,
                'storage_path': '/etc/revvel/tokens'
            }
        }
        
        # Load from config file if provided
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except (IOError, json.JSONDecodeError) as e:
                self.logger.warning(f"Config load error: {e}")
        
        return default_config

    def _setup_logging(self):
        """Configure logging for access management"""
        log_dir = '/var/log/revvel_email_organizer/openrouter'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/access.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('OpenRouterAccessManager')

    def _get_api_key(self) -> str:
        """
        Retrieve OpenRouter API key
        
        Returns:
            str: API key from environment or configuration
        """
        key_env = self.config['openrouter']['api_key_env']
        api_key = os.environ.get(key_env)
        
        if not api_key:
            self.logger.error(f"API key not found in environment: {key_env}")
            raise ValueError(f"OpenRouter API key must be set in {key_env}")
        
        return api_key

    def generate_app_specific_token(self, app_name: str) -> Dict[str, str]:
        """
        Generate a token specific to an application
        
        Args:
            app_name (str): Name of the application
        
        Returns:
            Dict with token details
        """
        try:
            # Generate unique token
            token_details = {
                'app_name': app_name,
                'token': self._create_unique_token(),
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(days=self.config['token_management']['rotation_days'])).isoformat()
            }
            
            # Store token securely
            self._store_token(token_details)
            
            return token_details
        
        except Exception as e:
            self.logger.error(f"Token generation error: {e}")
            raise

    def _create_unique_token(self) -> str:
        """
        Create a cryptographically secure unique token
        
        Returns:
            str: Unique token
        """
        return secrets.token_hex(32)  # 256-bit token

    def _store_token(self, token_details: Dict[str, str]):
        """
        Securely store application-specific token
        
        Args:
            token_details (Dict): Token information to store
        """
        storage_path = self.config['token_management']['storage_path']
        os.makedirs(storage_path, exist_ok=True)
        
        token_file = os.path.join(storage_path, f"{token_details['app_name']}_token.json")
        
        with open(token_file, 'w', opener=lambda path, flags: os.open(path, flags, 0o600)) as f:
            json.dump(token_details, f)

    def call_openrouter_api(self, endpoint: str, method: str = 'GET', data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make a generic call to OpenRouter API
        
        Args:
            endpoint (str): API endpoint
            method (str): HTTP method
            data (Dict, optional): Request payload
        
        Returns:
            Dict with API response
        """
        try:
            full_url = f"{self.config['openrouter']['base_url']}/{endpoint}"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': self.config['openrouter']['app_url'],
                'X-Title': self.config['openrouter']['app_name']
            }
            
            # Choose request method
            request_methods = {
                'GET': requests.get,
                'POST': requests.post,
                'PUT': requests.put,
                'DELETE': requests.delete
            }
            
            response = request_methods[method.upper()](
                full_url, 
                headers=headers, 
                json=data
            )
            
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            self.logger.error(f"OpenRouter API call error: {e}")
            raise

def main():
    # Example usage
    access_manager = OpenRouterAccessManager()
    
    # Generate app-specific token
    email_organizer_token = access_manager.generate_app_specific_token('email_organizer')
    print(json.dumps(email_organizer_token, indent=2))
    
    # Example API call
    try:
        models = access_manager.call_openrouter_api('models')
        print(json.dumps(models, indent=2))
    except Exception as e:
        print(f"API call failed: {e}")

if __name__ == "__main__":
    main()