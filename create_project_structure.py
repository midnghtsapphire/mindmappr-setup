#!/usr/bin/env python3

import os
import subprocess

def create_project_structure():
    """
    Create comprehensive project structure for Revvel Email Organizer
    """
    base_path = "/home/openclaw/.openclaw/workspace/revvel-email-organizer"
    
    # Create main project directories
    directories = [
        # Core source code
        "src/core",
        "src/api",
        "src/ml",
        "src/utils",
        
        # Testing
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        
        # Documentation
        "docs",
        
        # Configuration
        "config",
        
        # Deployment
        "k8s",
        "docker",
        
        # Static assets
        "static",
        "frontend"
    ]
    
    for dir_path in directories:
        full_path = os.path.join(base_path, dir_path)
        os.makedirs(full_path, exist_ok=True)
        
        # Create __init__.py in each directory for Python package structure
        init_file = os.path.join(full_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Revvel Email Organizer Module\n")
    
    # Create README
    readme_path = os.path.join(base_path, "README.md")
    with open(readme_path, 'w') as f:
        f.write("""# Revvel Email Organizer

## Overview
Intelligent, privacy-focused email organization and management tool.

## Features
- Advanced email processing
- Machine learning classification
- Privacy-first design
- Neurodivergent-friendly interface

## Installation
`pip install revvel-email-organizer`

## Quick Start
```python
from revvel_email_organizer import EmailOrganizer

organizer = EmailOrganizer()
organizer.process_archive("/path/to/email/archive")
```

## Contributing
See CONTRIBUTING.md

## License
MIT License
""")
    
    # Create requirements file
    requirements_path = os.path.join(base_path, "requirements.txt")
    with open(requirements_path, 'w') as f:
        f.write("""# Core Dependencies
fastapi
uvicorn
sqlalchemy
cryptography
scikit-learn
pandas
numpy

# Security
python-jose[cryptography]
passlib[bcrypt]

# Email Processing
mail-parser
imapclient

# Machine Learning
tensorflow
xgboost

# Development & Testing
pytest
mypy
black
flake8

# Deployment
gunicorn
""")
    
    # Create setup.py
    setup_path = os.path.join(base_path, "setup.py")
    with open(setup_path, 'w') as f:
        f.write("""from setuptools import setup, find_packages

setup(
    name='revvel-email-organizer',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'fastapi',
        'sqlalchemy',
        'scikit-learn',
        'cryptography'
    ],
    author='Audrey Evans',
    author_email='audrey@revvel.com',
    description='Intelligent Email Organization Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/midnghtsapphire/revvel-email-organizer',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ]
)
""")

def main():
    create_project_structure()
    print("Revvel Email Organizer project structure created successfully!")

if __name__ == "__main__":
    main()