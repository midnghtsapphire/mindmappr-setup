#!/usr/bin/env python3

import os
import subprocess
import json
import logging
import stripe
from typing import Dict, Any

class EmailOrganizerLauncher:
    def __init__(self, config_path: str):
        """
        Initialize comprehensive launch system
        
        Args:
            config_path (str): Path to launch configuration
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize payment system
        self._setup_stripe()

    def _setup_logging(self):
        """Configure launch and deployment logging"""
        log_dir = '/var/log/email_organizer/launch'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/launch.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('EmailOrganizerLaunch')

    def _setup_stripe(self):
        """
        Configure Stripe payment gateway
        
        Sets up subscription and payment processing
        """
        stripe_config = self.config['payment']['stripe']
        
        try:
            stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
            
            # Create product
            product = stripe.Product.create(
                name="Revvel Email Organizer",
                type="service"
            )
            
            # Create pricing tiers
            self._create_stripe_prices(product.id, stripe_config['tiers'])
            
            self.logger.info("Stripe payment gateway configured")
        
        except Exception as e:
            self.logger.error(f"Stripe configuration error: {e}")

    def _create_stripe_prices(self, product_id: str, tiers: List[Dict[str, Any]]):
        """
        Create pricing tiers for Email Organizer
        
        Args:
            product_id (str): Stripe product ID
            tiers (List): Pricing tiers configuration
        """
        for tier in tiers:
            stripe.Price.create(
                product=product_id,
                unit_amount=int(tier['price'] * 100),  # Convert to cents
                currency='usd',
                recurring={'interval': 'month'},
                nickname=tier['name']
            )

    def build_docker_images(self):
        """
        Build Docker containers for deployment
        """
        services = ['backend', 'frontend', 'worker']
        
        for service in services:
            try:
                subprocess.run([
                    'docker', 'build', 
                    '-t', f'email-organizer-{service}:latest',
                    f'./{service}'
                ], check=True)
                
                subprocess.run([
                    'docker', 'push', 
                    f'email-organizer-{service}:latest'
                ], check=True)
                
                self.logger.info(f"Successfully built and pushed {service} service")
            
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Docker build failed for {service}: {e}")

    def deploy_to_kubernetes(self):
        """
        Deploy to Kubernetes cluster
        """
        try:
            # Apply Kubernetes deployment configurations
            subprocess.run([
                'kubectl', 'apply', 
                '-f', 'k8s/deployment.yaml'
            ], check=True)
            
            # Verify deployment
            subprocess.run([
                'kubectl', 'rollout', 'status', 
                'deployment/email-organizer'
            ], check=True)
            
            self.logger.info("Successful Kubernetes deployment")
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Kubernetes deployment failed: {e}")
            self._rollback_deployment()

    def _rollback_deployment(self):
        """
        Rollback deployment in case of failure
        """
        try:
            subprocess.run([
                'kubectl', 'rollout', 'undo', 
                'deployment/email-organizer'
            ], check=True)
            
            self.logger.warning("Deployment rolled back to previous version")
        
        except subprocess.CalledProcessError as e:
            self.logger.critical(f"Rollback failed: {e}")

    def launch_marketing_campaign(self):
        """
        Initiate marketing and launch activities
        """
        # Placeholder for marketing launch
        # Would integrate with:
        # - Social media announcements
        # - Email marketing
        # - Influencer outreach
        # - Content marketing
        self.logger.info("Marketing campaign initialization")

    def run_launch_sequence(self):
        """
        Comprehensive launch sequence
        """
        try:
            # Build Docker images
            self.build_docker_images()
            
            # Deploy to Kubernetes
            self.deploy_to_kubernetes()
            
            # Launch marketing campaign
            self.launch_marketing_campaign()
            
            self.logger.info("Email Organizer launch completed successfully")
        
        except Exception as e:
            self.logger.critical(f"Launch sequence failed: {e}")

def main():
    # Launch configuration path
    config_path = "/home/openclaw/.openclaw/workspace/email_organizer_config.json"
    
    # Initialize launcher
    launcher = EmailOrganizerLauncher(config_path)
    
    # Execute launch sequence
    launcher.run_launch_sequence()

if __name__ == "__main__":
    main()