import os
import uuid
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class TokenManager:
    """
    Secure token generation and management for Revvel Email Organizer.
    
    Provides cryptographically secure token generation with:
    - Component-specific tokens
    - Secure storage
    - Encryption key derivation
    """
    
    def __init__(self, config_dir: str = None):
        """
        Initialize TokenManager with secure configuration.
        
        :param config_dir: Directory for storing encrypted tokens
        """
        self.config_dir = config_dir or os.path.expanduser('~/.revvel/tokens')
        os.makedirs(self.config_dir, exist_ok=True)
    
    def _derive_key(self, salt: bytes) -> bytes:
        """
        Derive a secure encryption key using PBKDF2.
        
        :param salt: Salt for key derivation
        :return: Derived encryption key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        return base64.urlsafe_b64encode(kdf.derive(os.environ.get('REVVEL_MASTER_KEY', '').encode()))
    
    def generate_token(self, component: str) -> str:
        """
        Generate a secure, component-specific token.
        
        :param component: Target component (e.g., 'email_classifier')
        :return: Cryptographically secure token
        """
        # Generate a unique token with component-specific salt
        token_id = str(uuid.uuid4())
        salt = os.urandom(16)
        
        # Create a hash-based token with additional security
        token_data = f"{component}:{token_id}:{salt.hex()}"
        token_hash = hashlib.sha3_256(token_data.encode()).hexdigest()
        
        # Optional: Encrypt and store token securely
        key = self._derive_key(salt)
        f = Fernet(key)
        encrypted_token = f.encrypt(token_hash.encode())
        
        # Save encrypted token with component metadata
        token_file = os.path.join(self.config_dir, f"{component}_token.enc")
        with open(token_file, 'wb') as f:
            f.write(encrypted_token)
        
        return token_hash
    
    def validate_token(self, component: str, token: str) -> bool:
        """
        Validate a token for a specific component.
        
        :param component: Target component
        :param token: Token to validate
        :return: Validation result
        """
        token_file = os.path.join(self.config_dir, f"{component}_token.enc")
        
        if not os.path.exists(token_file):
            return False
        
        try:
            with open(token_file, 'rb') as f:
                encrypted_token = f.read()
            
            # Attempt decryption
            key = self._derive_key(os.urandom(16))
            f = Fernet(key)
            decrypted_token = f.decrypt(encrypted_token).decode()
            
            return decrypted_token == token
        except Exception:
            return False