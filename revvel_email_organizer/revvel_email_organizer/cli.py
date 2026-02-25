"""
Command-Line Interface for Revvel Email Organizer

Provides a comprehensive CLI for email archive processing, 
token generation, and model discovery.
"""

import click
import logging
from typing import Optional

from .models import ModelManager
from .token_manager import TokenManager
from .email_processor import EmailProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
@click.version_option()
def main():
    """
    Revvel Email Organizer: AI-powered email archive management tool.
    
    Process email archives, generate secure tokens, and explore AI models.
    """
    pass

@main.command()
@click.argument('archive_path', type=click.Path(exists=True))
@click.option('--model', default='default', 
              help='AI model to use for processing')
@click.option('--dry-run', is_flag=True, 
              help='Simulate processing without making changes')
def process(archive_path: str, model: str, dry_run: bool):
    """
    Process an email archive using AI-powered categorization.
    
    ARCHIVE_PATH: Path to the email archive to process
    """
    try:
        processor = EmailProcessor()
        stats = processor.process_archive(
            source_path=archive_path, 
            model_name=model, 
            dry_run=dry_run
        )
        
        # Pretty print processing statistics
        click.echo("🔍 Email Processing Results:")
        click.echo(f"Total Emails: {stats['total_emails']}")
        click.echo(f"Processed Emails: {stats['processed_emails']}")
        click.echo(f"Categorized Emails: {stats['categorized_emails']}")
    
    except Exception as e:
        logger.error(f"Email processing failed: {e}")
        raise click.ClickException(str(e))

@main.command()
@click.option('--identifier', required=True, 
              help='Unique identifier for the token (e.g., username)')
@click.option('--type', default='app', 
              help='Type of token to generate')
@click.option('--expiry', default=365, 
              help='Token validity period in days')
def token(identifier: str, type: str, expiry: int):
    """
    Generate a secure application token.
    
    Creates a cryptographically secure token for authentication.
    """
    try:
        token_manager = TokenManager()
        new_token = token_manager.generate_token(
            identifier=identifier, 
            token_type=type, 
            expiry_days=expiry
        )
        
        # Securely display token
        click.echo("🔐 Generated Token:")
        click.echo(new_token)
        click.echo("\n⚠️  Keep this token secret and secure!")
    
    except Exception as e:
        logger.error(f"Token generation failed: {e}")
        raise click.ClickException(str(e))

@main.command()
@click.option('--api-key', 
              help='OpenRouter API key (optional, can use environment variable)')
def models(api_key: Optional[str]):
    """
    List available AI models for email processing.
    
    Retrieves model information from OpenRouter.
    """
    try:
        model_manager = ModelManager(api_key)
        available_models = model_manager.list_models()
        
        # Display models in a tabular format
        click.echo("🤖 Available AI Models:")
        for model in available_models:
            click.echo(
                f"Name: {model.get('id', 'N/A')} | "
                f"Description: {model.get('name', 'No description')}"
            )
    
    except Exception as e:
        logger.error(f"Model retrieval failed: {e}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main()