#!/usr/bin/env python3

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.email_processor import EmailProcessor
from core.security_engine import SecurityEngine
from core.ml_classifier import EmailClassificationSystem
from config.openrouter_access import OpenRouterAccessManager

class EmailProcessingRequest(BaseModel):
    """
    Request model for email processing
    """
    archive_path: str = Field(..., description="Path to email archive")
    config: Optional[Dict[str, Any]] = Field(None, description="Processing configuration")

class EmailClassificationRequest(BaseModel):
    """
    Request model for email classification
    """
    emails: List[Dict[str, str]] = Field(..., description="List of emails to classify")

class TokenRequest(BaseModel):
    """
    Request model for token generation
    """
    app_name: str = Field(..., description="Name of the application")

class RevvelEmailOrganizerAPI:
    def __init__(self):
        """
        Initialize API with core components
        """
        # Load configurations
        self.config = self._load_config()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize core components
        self.security_engine = SecurityEngine(self.config)
        self.openrouter_manager = OpenRouterAccessManager()
        self.email_processor = EmailProcessor(self.config)
        self.ml_classifier = EmailClassificationSystem(self.config)
        
        # Create FastAPI app
        self.app = self._create_fastapi_app()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load API configuration
        
        Returns:
            Dict with configuration
        """
        default_config = {
            'api': {
                'cors': {
                    'allowed_origins': ['*'],
                    'allowed_methods': ['*'],
                    'allowed_headers': ['*']
                }
            },
            'security': {
                'jwt': {
                    'secret_key': 'your-secret-key',
                    'algorithm': 'HS256'
                }
            }
        }
        
        # In a real-world scenario, load from a config file or environment
        return default_config

    def _setup_logging(self):
        """
        Configure API logging
        """
        log_dir = '/var/log/revvel_email_organizer/api'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/api.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('RevvelEmailOrganizerAPI')

    def _create_fastapi_app(self) -> FastAPI:
        """
        Create FastAPI application with middleware and routes
        
        Returns:
            FastAPI application instance
        """
        app = FastAPI(
            title="Revvel Email Organizer API",
            description="Intelligent, privacy-preserving email processing API",
            version="1.0.0"
        )
        
        # CORS Middleware
        cors_config = self.config['api']['cors']
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_config['allowed_origins'],
            allow_credentials=True,
            allow_methods=cors_config['allowed_methods'],
            allow_headers=cors_config['allowed_headers']
        )
        
        # Register routes
        self._register_routes(app)
        
        return app

    def _register_routes(self, app: FastAPI):
        """
        Register API routes
        
        Args:
            app (FastAPI): FastAPI application instance
        """
        @app.post("/process/archive")
        async def process_email_archive(request: EmailProcessingRequest):
            """
            Process email archive
            """
            try:
                # Encrypt archive path
                encrypted_path = self.security_engine.encrypt_email_data({
                    'archive_path': request.archive_path
                })
                
                # Process emails
                result = self.email_processor.process_archive(
                    encrypted_path['archive_path'],
                    request.config or {}
                )
                
                return result
            
            except Exception as e:
                self.logger.error(f"Email archive processing error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/classify/emails")
        async def classify_emails(request: EmailClassificationRequest):
            """
            Classify emails using machine learning
            """
            try:
                # Classify emails
                result = self.ml_classifier.classify_emails(request.emails)
                return result
            
            except Exception as e:
                self.logger.error(f"Email classification error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/tokens/generate")
        async def generate_app_token(request: TokenRequest):
            """
            Generate application-specific token
            """
            try:
                token = self.openrouter_manager.generate_app_specific_token(request.app_name)
                return token
            
            except Exception as e:
                self.logger.error(f"Token generation error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/models/list")
        async def list_openrouter_models():
            """
            List available OpenRouter models
            """
            try:
                models = self.openrouter_manager.call_openrouter_api('models')
                return models
            
            except Exception as e:
                self.logger.error(f"Model listing error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/health")
        async def health_check():
            """
            API health check endpoint
            """
            return {
                "status": "healthy",
                "version": "1.0.0",
                "components": {
                    "email_processor": "running",
                    "ml_classifier": "running",
                    "security_engine": "running"
                }
            }

def create_fastapi_app():
    """
    Create and return FastAPI application
    
    Returns:
        FastAPI application instance
    """
    api = RevvelEmailOrganizerAPI()
    return api.app

def run_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Run API server
    
    Args:
        host (str): Server host
        port (int): Server port
    """
    uvicorn.run(
        "routes:create_fastapi_app()", 
        host=host, 
        port=port, 
        reload=True
    )

def main():
    # Run API server
    run_server()

if __name__ == "__main__":
    main()