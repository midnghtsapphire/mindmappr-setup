from setuptools import setup, find_packages

setup(
    name='revvel-email-organizer',
    version='1.0.0',
    description='Intelligent, Privacy-First Email Organization Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Audrey Evans',
    author_email='audrey@revvel.com',
    url='https://github.com/midnghtsapphire/revvel-email-organizer',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'revvel-email-organizer=cli.email_organizer_cli:main'
        ]
    },
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy',
        'requests',
        'cryptography',
        'mailparser',
        'fastapi',
        'uvicorn'
    ],
    extras_require={
        'dev': [
            'pytest',
            'mypy',
            'black',
            'flake8'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='email organization machine-learning privacy neurodivergent',
    python_requires='>=3.10',
    project_urls={
        'Source': 'https://github.com/midnghtsapphire/revvel-email-organizer',
        'Bug Reports': 'https://github.com/midnghtsapphire/revvel-email-organizer/issues'
    }
)