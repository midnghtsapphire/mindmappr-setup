# Revvel Email Organizer 📧🤖

A powerful CLI tool for processing email archives using AI-powered models.

## Features

- 🔍 Process Email Archives
- 🔐 Secure Token Generation
- 🌐 AI Model Discovery

## Installation

```bash
pip install revvel-email-organizer
```

## Usage

### Process Email Archive

```bash
revvel process /path/to/email/archive
```

Options:
- `--model`: Select specific AI model
- `--dry-run`: Simulate processing without changes

### Generate Secure Token

```bash
revvel token --identifier myapp --type app --expiry 365
```

### List Available Models

```bash
revvel models
```

## Configuration

Set OpenRouter API key:
```bash
export OPENROUTER_API_KEY=your_api_key_here
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Security

- Tokens generated with cryptographic security
- Configurable token expiration
- Secure file storage with restricted permissions