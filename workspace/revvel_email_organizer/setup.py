from setuptools import setup, find_packages

setup(
    name='revvel-email-organizer',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'cryptography',
        'openrouter-python'
    ],
    entry_points={
        'console_scripts': [
            'revvel-email-organizer=revvel_email_organizer.cli:main',
        ],
    },
    author='Audrey Evans',
    author_email='angelreporters@gmail.com',
    description='Intelligent Email Organization Tool',
    long_description=open('README.md').read() if open('README.md').read() else '',
    long_description_content_type='text/markdown',
    url='https://github.com/midnghtsapphire/revvel-email-organizer',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)