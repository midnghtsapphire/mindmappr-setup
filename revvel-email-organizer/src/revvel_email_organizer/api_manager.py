import os
import httpx
import asyncio
from typing import Dict, Any, Optional
from .token_manager import TokenManager

class APIConnectionManager:
    """
    Manages secure API connections for Revvel Email Organizer.
    
    Supports:
    - OpenRouter API integration
    - Secure token management
    - Async connection handling
    - Error resilience
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 token_manager: Optional[TokenManager] = None):
        """
        Initialize API Connection Manager.
        
        :param api_key: OpenRouter API key
        :param token_manager: Optional TokenManager instance
        """
        self.api_key = api_key or os.environ.get('OPENROUTER_API_KEY')
        self.token_manager = token_manager or TokenManager()
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
    
    async def make_request(self, 
                           endpoint: str, 
                           method: str = 'GET', 
                           data: Optional[Dict[str, Any]] = None,
                           component: str = 'default') -> Dict[str, Any]:
        """
        Make a secure, authenticated API request.
        
        :param endpoint: API endpoint
        :param method: HTTP method
        :param data: Request payload
        :param component: Component making the request
        :return: API response
        """
        # Validate component token
        token = self.token_manager.generate_token(component)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'X-Component-Token': token,
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            try:
                if method == 'GET':
                    response = await client.get(endpoint, headers=headers)
                elif method == 'POST':
                    response = await client.post(endpoint, headers=headers, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                # Implement sophisticated error handling
                print(f"API Request Failed: {e}")
                return {}
            except Exception as e:
                print(f"Unexpected error: {e}")
                return {}
    
    async def get_available_models(self) -> Dict[str, Any]:
        """
        Retrieve available AI models from OpenRouter.
        
        :return: Dictionary of available models
        """
        return await self.make_request(
            'https://openrouter.ai/api/v1/models', 
            component='model_discovery'
        )