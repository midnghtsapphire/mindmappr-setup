#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import logging
from typing import Dict, Any
import requests
import stripe

class MasterDeploymentSystem:
    def __init__(self, config_path: str):
        """
        Comprehensive deployment system for Revvel Email Organizer
        
        Args:
            config_path (str): Path to deployment configuration
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize deployment components
        self.deployment_steps = [
            self._validate_prerequisites,
            self._build_docker_images,
            self._run_security_checks,
            self._deploy_to_kubernetes,
            self._configure_payment_gateway,
            self._run_integration_tests,
            self._launch_marketing_campaign
        ]

    def _setup_logging(self):
        """Configure comprehensive deployment logging"""
        log_dir = '/var/log/revvel_email_organizer/deployment'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/master_deployment.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('MasterDeployment')

    def execute_deployment(self) -> Dict[str, Any]:
        """
        Execute comprehensive deployment sequence
        
        Returns:
            Dict with deployment results
        """
        deployment_results = {
            'overall_status': True,
            'step_results': {}
        }
        
        for step in self.deployment_steps:
            try:
                step_name = step.__name__
                self.logger.info(f"Executing deployment step: {step_name}")
                
                result = step()
                deployment_results['step_results'][step_name] = result
                
                if not result.get('status', False):
                    deployment_results['overall_status'] = False
                    self.logger.error(f"Deployment step failed: {step_name}")
                    break
            
            except Exception as e:
                deployment_results['overall_status'] = False
                deployment_results['step_results'][step.__name__] = {
                    'status': False,
                    'error': str(e)
                }
                self.logger.critical(f"Deployment step {step.__name__} failed: {e}")
                break
        
        # Send deployment notification
        self._send_deployment_notification(deployment_results)
        
        return deployment_results

    def _validate_prerequisites(self) -> Dict[str, Any]:
        """
        Validate system prerequisites
        
        Returns:
            Dict with validation results
        """
        try:
            # Check required tools
            required_tools = ['docker', 'kubectl', 'git']
            missing_tools = []
            
            for tool in required_tools:
                result = subprocess.run(['which', tool], capture_output=True)
                if result.returncode != 0:
                    missing_tools.append(tool)
            
            if missing_tools:
                return {
                    'status': False,
                    'message': f'Missing tools: {", ".join(missing_tools)}'
                }
            
            return {
                'status': True,
                'message': 'All prerequisites validated'
            }
        except Exception as e:
            return {
                'status': False,
                'message': f'Prerequisite validation failed: {e}'
            }

    def _build_docker_images(self) -> Dict[str, Any]:
        """
        Build Docker images for all services
        
        Returns:
            Dict with build results
        """
        services = ['backend', 'frontend', 'ml_processor', 'database_migrator']
        
        for service in services:
            try:
                # Build Docker image
                build_result = subprocess.run([
                    'docker', 'build',
                    '-t', f'revvel-email-organizer-{service}:latest',
                    f'./{service}'
                ], check=True, capture_output=True)
                
                # Push to registry
                push_result = subprocess.run([
                    'docker', 'push', 
                    f'revvel-email-organizer-{service}:latest'
                ], check=True, capture_output=True)
            
            except subprocess.CalledProcessError as e:
                return {
                    'status': False,
                    'message': f'Docker build failed for {service}: {e}'
                }
        
        return {
            'status': True,
            'message': 'All Docker images built and pushed successfully'
        }

    def _run_security_checks(self) -> Dict[str, Any]:
        """
        Run comprehensive security checks
        
        Returns:
            Dict with security check results
        """
        try:
            # Run Trivy for vulnerability scanning
            trivy_result = subprocess.run([
                'trivy', 'image', 
                'revvel-email-organizer-backend:latest'
            ], capture_output=True, text=True)
            
            # Check for high or critical vulnerabilities
            if 'HIGH' in trivy_result.stdout or 'CRITICAL' in trivy_result.stdout:
                return {
                    'status': False,
                    'message': 'Security vulnerabilities detected',
                    'details': trivy_result.stdout
                }
            
            return {
                'status': True,
                'message': 'No significant security vulnerabilities found'
            }
        
        except Exception as e:
            return {
                'status': False,
                'message': f'Security check failed: {e}'
            }

    def _deploy_to_kubernetes(self) -> Dict[str, Any]:
        """
        Deploy to Kubernetes cluster
        
        Returns:
            Dict with deployment results
        """
        try:
            # Apply Kubernetes manifests
            kubectl_result = subprocess.run([
                'kubectl', 'apply', 
                '-f', 'k8s/deployment.yaml'
            ], check=True, capture_output=True)
            
            # Verify deployment
            rollout_result = subprocess.run([
                'kubectl', 'rollout', 'status', 
                'deployment/revvel-email-organizer'
            ], check=True, capture_output=True)
            
            return {
                'status': True,
                'message': 'Successful Kubernetes deployment'
            }
        
        except subprocess.CalledProcessError as e:
            return {
                'status': False,
                'message': f'Kubernetes deployment failed: {e}'
            }

    def _configure_payment_gateway(self) -> Dict[str, Any]:
        """
        Configure Stripe payment gateway
        
        Returns:
            Dict with payment configuration results
        """
        try:
            # Set Stripe API key
            stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
            
            # Create product
            product = stripe.Product.create(
                name="Revvel Email Organizer",
                type="service"
            )
            
            # Create pricing tiers
            tiers = [
                {
                    'name': 'Free',
                    'price': 0,
                    'interval': 'month'
                },
                {
                    'name': 'Pro',
                    'price': 9.99,
                    'interval': 'month'
                },
                {
                    'name': 'Enterprise',
                    'price': 49.99,
                    'interval': 'month'
                }
            ]
            
            for tier in tiers:
                stripe.Price.create(
                    product=product.id,
                    unit_amount=int(tier['price'] * 100),
                    currency='usd',
                    recurring={'interval': tier['interval']},
                    nickname=tier['name']
                )
            
            return {
                'status': True,
                'message': 'Stripe payment gateway configured successfully'
            }
        
        except Exception as e:
            return {
                'status': False,
                'message': f'Payment gateway configuration failed: {e}'
            }

    def _run_integration_tests(self) -> Dict[str, Any]:
        """
        Run comprehensive integration tests
        
        Returns:
            Dict with test results
        """
        try:
            # Run integration test script
            test_result = subprocess.run([
                'python', 
                '/home/openclaw/.openclaw/workspace/revvel_email_organizer_integration.py'
            ], capture_output=True, text=True)
            
            # Check test output
            if test_result.returncode != 0:
                return {
                    'status': False,
                    'message': 'Integration tests failed',
                    'details': test_result.stderr
                }
            
            return {
                'status': True,
                'message': 'All integration tests passed successfully'
            }
        
        except Exception as e:
            return {
                'status': False,
                'message': f'Integration test execution failed: {e}'
            }

    def _launch_marketing_campaign(self) -> Dict[str, Any]:
        """
        Initiate marketing campaign
        
        Returns:
            Dict with marketing campaign results
        """
        try:
            # Send launch announcement
            requests.post(
                'https://api.mailchimp.com/3.0/campaigns',
                headers={
                    'Authorization': f'Bearer {os.environ.get("MAILCHIMP_API_KEY")}',
                    'Content-Type': 'application/json'
                },
                json={
                    'type': 'regular',
                    'recipients': {'list_id': 'YOUR_LIST_ID'},
                    'settings': {
                        'subject_line': 'Revvel Email Organizer is Live!',
                        'preview_text': 'Intelligent email management is here'
                    }
                }
            )
            
            return {
                'status': True,
                'message': 'Marketing campaign initiated successfully'
            }
        
        except Exception as e:
            return {
                'status': False,
                'message': f'Marketing campaign launch failed: {e}'
            }

    def _send_deployment_notification(self, deployment_results: Dict[str, Any]):
        """
        Send deployment notification via multiple channels
        
        Args:
            deployment_results (Dict): Comprehensive deployment results
        """
        try:
            # Slack notification
            requests.post(
                os.environ.get('SLACK_WEBHOOK_URL', ''),
                json={
                    'text': f"Deployment {'Successful' if deployment_results['overall_status'] else 'Failed'}: Revvel Email Organizer"
                }
            )
            
            # Email notification
            requests.post(
                'https://api.sendgrid.com/v3/mail/send',
                headers={
                    'Authorization': f'Bearer {os.environ.get("SENDGRID_API_KEY")}',
                    'Content-Type': 'application/json'
                },
                json={
                    'personalizations': [{
                        'to': [{'email': 'audrey@revvel.com'}]
                    }],
                    'from': {'email': 'deployments@revvel.com'},
                    'subject': f"Deployment {'Success' if deployment_results['overall_status'] else 'Failure'}",
                    'content': [{
                        'type': 'text/plain',
                        'value': json.dumps(deployment_results, indent=2)
                    }]
                }
            )
        
        except Exception as e:
            self.logger.error(f"Notification sending failed: {e}")

def main():
    # Path to deployment configuration
    config_path = "/home/openclaw/.openclaw/workspace/revvel_email_organizer_config.json"
    
    # Initialize deployment system
    deployment_system = MasterDeploymentSystem(config_path)
    
    # Execute deployment
    deployment_results = deployment_system.execute_deployment()
    
    # Print deployment results
    print(json.dumps(deployment_results, indent=2))
    
    # Exit with appropriate status
    sys.exit(0 if deployment_results['overall_status'] else 1)

if __name__ == "__main__":
    main()