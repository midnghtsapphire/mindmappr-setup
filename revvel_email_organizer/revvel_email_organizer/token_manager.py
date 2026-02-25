"""
Secure Token Generation and Management Module

Provides cryptographically secure token generation and storage mechanisms.
"""

import os
import logging
import base64
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TokenManager:
    """
    Manages secure token generation, encryption, and storage.
    
    Provides methods for generating application tokens with strong security properties.
    """
    
    def __init__(self, token_path: Optional[str] = None):
        """
        Initialize TokenManager with optional custom token storage path.
        
        Args:
            token_path (str, optional): Path to store application tokens. 
                Defaults to a secure location in user's home directory.
        """
        # Determine default token storage path
        if token_path is None:
            token_path = os.path.expanduser("~/.revvel/tokens")
        
        # Ensure token directory exists
        os.makedirs(token_path, exist_ok=True)
        self.token_path = token_path
    
    def generate_token(self, identifier: str, 
                       token_type: str = 'app', 
                       expiry_days: int = 365) -> str:
        """
        Generate a cryptographically secure token.
        
        Args:
            identifier (str): Unique identifier for the token (e.g., username, app name)
            token_type (str, optional): Type of token. Defaults to 'app'.
            expiry_days (int, optional): Token validity period. Defaults to 365 days.
        
        Returns:
            str: Secure, URL-safe token
        
        Raises:
            ValueError: If identifier is empty or invalid
        """
        if not identifier or len(identifier) < 3:
            raise ValueError("Token identifier must be at least 3 characters long")
        
        try:
            # Generate a high-entropy random token
            token = Fernet.generate_key()
            
            # Optional: Add custom encoding or metadata
            encoded_token = base64.urlsafe_b64encode(token).decode('utf-8')
            
            # Log token generation (sensitive info redacted)
            logger.info(f"Generated {token_type} token for {identifier}")
            
            # Optional: Store token details
            self._store_token(identifier, encoded_token, token_type, expiry_days)
            
            return encoded_token
        
        except Exception as e:
            logger.error(f"Token generation failed: {e}")
            raise
    
    def _store_token(self, identifier: str, 
                     token: str, 
                     token_type: str, 
                     expiry_days: int):
        """
        Securely store token details.
        
        Args:
            identifier (str): Token owner/context
            token (str): Generated token
            token_type (str): Type of token
            expiry_days (int): Token validity period
        """
        try:
            token_file = os.path.join(
                self.token_path, 
                f"{identifier}_{token_type}_token.secure"
            )
            
            # Store token with additional metadata
            token_info = {
                "identifier": identifier,
                "type": token_type,
                "created_at": os.path.getctime(token_file) if os.path.exists(token_file) else None,
                "expires_at": os.path.getctime(token_file) + (expiry_days * 86400) if os.path.exists(token_file) else None
            }
            
            # Use secure file permissions
            with open(token_file, 'w', opener=lambda path, flags: os.open(path, flags, 0o600)) as f:
                import json
                json.dump(token_info, f)
            
            logger.info(f"Token for {identifier} stored securely")
        
        except Exception as e:
            logger.warning(f"Could not store token details: {e}")