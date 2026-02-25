"""
OpenRouter Model Integration Module

Handles retrieval and management of available AI models for email processing.
"""

import os
import logging
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manages interactions with OpenRouter for model discovery and selection.
    
    Attributes:
        api_key (str): OpenRouter API key for authentication
        base_url (str): Base URL for OpenRouter API
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the ModelManager with OpenRouter credentials.
        
        Args:
            api_key (str, optional): OpenRouter API key. 
                Defaults to environment variable OPENROUTER_API_KEY.
        
        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        # Load environment variables
        load_dotenv()
        
        # Prioritize passed API key, then environment variable
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key is required. "
                "Set OPENROUTER_API_KEY environment variable or pass directly."
            )
        
        self.base_url = "https://openrouter.ai/api/v1"
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        Retrieve available AI models from OpenRouter.
        
        Returns:
            List of dictionaries containing model information.
        
        Raises:
            requests.RequestException: For network or API request errors.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.base_url}/models", 
                headers=headers
            )
            
            response.raise_for_status()  # Raise exception for bad responses
            
            models = response.json().get('data', [])
            
            logger.info(f"Retrieved {len(models)} available models")
            return models
        
        except requests.RequestException as e:
            logger.error(f"Error retrieving models: {e}")
            raise