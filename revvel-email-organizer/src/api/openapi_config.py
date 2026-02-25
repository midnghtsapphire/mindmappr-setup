#!/usr/bin/env python3

from typing import Dict, Any

def generate_openapi_config() -> Dict[str, Any]:
    """
    Generate comprehensive OpenAPI configuration
    
    Returns:
        Dict with OpenAPI configuration
    """
    return {
        "info": {
            "title": "Revvel Email Organizer API",
            "description": """
            # Intelligent Email Processing API

            ## Features
            - Privacy-preserving email archive processing
            - Machine learning email classification
            - Secure token management
            - OpenRouter model integration

            ## Accessibility
            - Neurodivergent-friendly design
            - Low cognitive load interactions
            - Clear, predictable workflows

            ## Privacy Principles
            - Minimal data retention
            - Automatic anonymization
            - Configurable privacy controls
            """,
            "version": "1.0.0",
            "contact": {
                "name": "Audrey Evans",
                "email": "audrey@revvel.com",
                "url": "https://revvel.com"
            },
            "license": {
                "name": "MIT License",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "servers": [
            {
                "url": "https://api.revvel.com/email-organizer/v1",
                "description": "Production Server"
            },
            {
                "url": "https://staging-api.revvel.com/email-organizer/v1",
                "description": "Staging Server"
            }
        ],
        "tags": [
            {
                "name": "Email Processing",
                "description": "Email archive processing and classification"
            },
            {
                "name": "Authentication",
                "description": "Token and authentication management"
            },
            {
                "name": "Models",
                "description": "OpenRouter model management"
            }
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [
            {
                "bearerAuth": []
            }
        ],
        "externalDocs": {
            "description": "GitHub Repository",
            "url": "https://github.com/midnghtsapphire/revvel-email-organizer"
        }
    }

def main():
    # Print OpenAPI configuration for verification
    import json
    print(json.dumps(generate_openapi_config(), indent=2))

if __name__ == "__main__":
    main()