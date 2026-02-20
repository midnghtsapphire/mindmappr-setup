# MindMappr Setup — OpenClaw Droplet Documentation

Complete documentation and configuration backup for the MindMappr/OpenClaw agent running on DigitalOcean.

## Droplet Details

| Property | Value |
|---|---|
| **Name** | openclaw23onubuntu-s-2vcpu-4gb-120gb-intel-sfo3-01 |
| **IP** | 164.90.148.7 |
| **OS** | Ubuntu 24.04.1 LTS |
| **OpenClaw Version** | v2026.2.3 |
| **Agent Name** | MindMappr |
| **Telegram Bot** | @googlieeyes_bot |

## Repository Contents

```
mindmappr-setup/
├── README.md                    # This file
├── MASTER_DOCUMENT.md           # Complete setup documentation
├── workspace/                   # Full backup of agent workspace
│   ├── SOUL.md                  # Agent personality
│   ├── IDENTITY.md              # Agent identity
│   ├── USER.md                  # User profile
│   ├── MEMORY.md                # Persistent memory
│   ├── TODO.md                  # Active tasks
│   ├── memory/                  # Daily memory files
│   └── ...                      # All workspace files
├── job-queue/                   # Job queue system
│   └── mindmappr-queue.sh       # Queue CLI tool
├── configs/                     # Config file backups
│   ├── openclaw.env             # Environment variables
│   └── openclaw.json            # Main config (REDACTED)
└── ssh/                         # SSH key info
    └── README.md                # SSH setup instructions
```

## Quick Start

### SSH Access
```bash
ssh -i /path/to/droplet_ssh_key root@164.90.148.7
```

### Job Queue
```bash
# Add a task
mindmappr-queue add seo "Write blog post about tiny home insurance"

# Check status
mindmappr-queue status

# List jobs
mindmappr-queue list
```

### OpenClaw Service
```bash
# Check status
systemctl status openclaw

# Restart
systemctl restart openclaw

# View logs
journalctl -u openclaw -f
```

## API Keys Configured

- OpenRouter (AI models)
- ElevenLabs (voice synthesis)
- GitHub PAT (repository access)
- DigitalOcean (infrastructure)
- Telegram Bot (messaging)

## Changes Made (2026-02-20)

1. Fixed malformed environment variables in `openclaw.json`
2. Fixed truncated API key in `/opt/openclaw.env`
3. Added `ELEVENLABS_API_KEY` and `GITHUB_TOKEN` to env file
4. Generated SSH key pair and added to GitHub
5. Installed job queue system with cron scheduling
6. Backed up entire agent workspace
