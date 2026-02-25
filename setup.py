from setuptools import setup, find_packages

setup(
    name='revvel-email-organizer',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click>=8.0.0',
        'cryptography>=3.4.7',
        'httpx>=0.22.0',
        'python-dotenv>=0.19.0',
        'openrouter-python>=0.1.0'
    ],
    entry_points={
        'console_scripts': [
            'revvel-email-organizer=revvel_email_organizer.cli:main',
        ],
    }
)