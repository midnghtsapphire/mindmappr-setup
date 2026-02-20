# MindMappr / OpenClaw Droplet — Master Document

**Generated:** 2026-02-20  
**Droplet:** openclaw23onubuntu-s-2vcpu-4gb-120gb-intel-sfo3-01  
**IP:** 164.90.148.7  
**Owner:** MIDNGHTSAPPHIRE (angelreporters@gmail.com)

---

## Table of Contents

1. [Infrastructure Overview](#1-infrastructure-overview)
2. [OpenClaw Setup Documentation](#2-openclaw-setup-documentation)
3. [API Keys and Credentials](#3-api-keys-and-credentials)
4. [Agent Workspace — MindMappr's Memory](#4-agent-workspace--mindmapprs-memory)
5. [Services and Processes](#5-services-and-processes)
6. [Skills and Plugins](#6-skills-and-plugins)
7. [Telegram Bot Configuration](#7-telegram-bot-configuration)
8. [SSH Key Setup](#8-ssh-key-setup)
9. [API Connection Fixes Applied](#9-api-connection-fixes-applied)
10. [Job Queue System](#10-job-queue-system)
11. [Active Projects Context](#11-active-projects-context)
12. [Known Issues and Recommendations](#12-known-issues-and-recommendations)

---

## 1. Infrastructure Overview

| Property | Value |
|---|---|
| **Droplet Name** | openclaw23onubuntu-s-2vcpu-4gb-120gb-intel-sfo3-01 |
| **IP Address** | 164.90.148.7 |
| **OS** | Ubuntu 24.04.1 LTS |
| **CPU** | 2 vCPU (Intel) |
| **RAM** | 4 GB |
| **Disk** | 120 GB |
| **Region** | SFO3 (San Francisco) |
| **Users** | root, openclaw |
| **SSH Port** | 22 (default) |

### Filesystem Layout

```
/opt/openclaw/           — OpenClaw installation (Node.js app)
/opt/openclaw.env        — Environment variables for OpenClaw service
/opt/mindmappr-queue/    — Job queue system (installed 2026-02-20)
/home/openclaw/          — OpenClaw user home
/home/openclaw/.openclaw/ — OpenClaw config, workspace, sessions
/etc/systemd/system/openclaw.service — Systemd service unit
/etc/setup_wizard.sh     — Initial setup wizard script
```

---

## 2. OpenClaw Setup Documentation

### Version

| Component | Version |
|---|---|
| **OpenClaw** | v2026.2.3 |
| **Node.js** | System default |
| **Gateway Port** | 18789 |
| **Gateway Bind** | LAN |

### Configuration Files

| File | Purpose |
|---|---|
| `/opt/openclaw.env` | System-level environment variables |
| `/home/openclaw/.openclaw/openclaw.json` | Main OpenClaw configuration (agent, channels, skills, tools, model config) |
| `/home/openclaw/.openclaw/openclaw.json.bak.1` | Backup of config |
| `/home/openclaw/.openclaw/agents/main/agent/auth-profiles.json` | OpenRouter API key auth profile |
| `/home/openclaw/.openclaw/agents/main/sessions/sessions.json` | Active session tracking |
| `/etc/systemd/system/openclaw.service` | Systemd service definition |

### Model Configuration

The agent is configured to use **OpenRouter** as the primary AI provider with `openrouter/auto` as the primary model. The fallback list includes 80+ models spanning:

- **OpenAI**: GPT-3.5 through GPT-5.2 Pro, o3/o4 series
- **Anthropic**: Claude 3.5 Haiku, Claude 3.7 Sonnet
- **Google**: Gemini 2.0/2.5/3.0 series
- **Meta**: Llama 3/3.1/3.3/4 series
- **DeepSeek**: v3, R1, Chat series
- **Mistral**: Large, Small, Codestral, Pixtral
- **xAI**: Grok 3, Grok 4
- **Qwen**: Qwen3 series
- **Others**: Nvidia Nemotron, MoonShot Kimi, MiniMax, NousResearch

### OpenRouter Auth Profile

```json
{
  "openrouter:default": {
    "type": "api_key",
    "provider": "openrouter",
    "key": "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"
  }
}
```

### Gateway Configuration

```json
{
  "mode": "local",
  "bind": "loopback",
  "auth": {
    "token": "687d8749e15c33a21161065852e89d02631ddf63b9505bf32c24adca5acc248d"
  },
  "trustedProxies": ["127.0.0.1"]
}
```

---

## 3. API Keys and Credentials

### Keys Found in Config

| Service | Key | Location |
|---|---|---|
| **OpenRouter** | `sk-or-v1-c7fcd17...8467cf` | auth-profiles.json |
| **OpenRouter** (env alias) | `sk-or-v1-335780f...72fee` | /opt/openclaw.env (as ANTHROPIC_API_KEY and OPENAI_API_KEY) |
| **ElevenLabs** | `sk_6f66125873824c2a6657...578fca` | openclaw.json env.vars + sag skill |
| **GitHub PAT** | `github_pat_11ABDLZOI0i...yD2beY` | openclaw.json env.vars |
| **DigitalOcean** | `dop_v1_8d389799...1f7a59` | openclaw.json env.vars |
| **Nano Banana Pro** | `AIzaSyBsrGhrIptx...JmY8e0` | openclaw.json skills |
| **OpenAI (web search)** | `sk-proj-SUAFttaL...PG50A` | openclaw.json tools.web.search |
| **Telegram Bot** | `8237788245:AAFE01tfL0jW...3QlX30` | openclaw.json channels.telegram |
| **Gateway Token** | `687d8749e15c33a2...248d` | /opt/openclaw.env |

---

## 4. Agent Workspace — MindMappr's Memory

MindMappr does not have a single "master document." Instead, its knowledge is distributed across a **workspace** of markdown files and JSON configs. Below is the complete inventory:

### Identity and Core Files

| File | Purpose |
|---|---|
| `SOUL.md` | Agent personality and core values |
| `IDENTITY.md` | Agent identity definition |
| `USER.md` | User profile and preferences |
| `BOOTSTRAP.md` | Startup instructions |
| `TOOLS.md` | Available tools documentation |
| `SKILLS.md` | Skills reference |
| `HEARTBEAT.md` | Heartbeat/health check config |
| `TODO.md` | Active task list |
| `MEMORY.md` | Persistent memory notes |

### Project-Specific Documents

| File | Purpose |
|---|---|
| `GITHUB_ACCESS.md` | GitHub access configuration |
| `GITHUB_CONFIG.md` | GitHub repository configuration |
| `GITHUB_PAGES_GUIDE.md` | GitHub Pages deployment guide |
| `GITHUB_STRATEGY.md` | GitHub workflow strategy |
| `REPOSITORY_TRACKER.md` | Repository tracking and status |
| `OPENROUTER_TEAM_STRATEGY.md` | OpenRouter model usage strategy |
| `OPPORTUNITY_DEPLOYMENT_STRATEGY.md` | Deployment strategy for opportunities |

### Email Organizer Project

| File | Purpose |
|---|---|
| `REVVEL_EMAIL_COMPASS_ANALYSIS.md` | Email Compass analysis |
| `REVVEL_EMAIL_ORGANIZER_ANALYSIS.md` | Email Organizer analysis |
| `REVVEL_EMAIL_ORGANIZER_INTEGRATION_STRATEGY.md` | Integration strategy |
| `REVVEL_EMAIL_ORGANIZER_REPOSITORY_INVESTIGATION.md` | Repo investigation |
| `EMAIL_CLEANUP_FRAMEWORK.md` | Email cleanup framework |
| `EMAIL_COMPASS_PRODUCTION_ROADMAP.md` | Production roadmap |
| `EMAIL_ORGANIZER_INTEGRATION_PLAN.md` | Integration plan |
| `EMAIL_ORGANIZER_SECURITY_ENHANCEMENT.md` | Security enhancements |
| `MEETAUDREYEVANS_REPO_ASSESSMENT.md` | MeetAudreyEvans repo assessment |
| `MOLTBOOK_SECURITY_ASSESSMENT.md` | Moltbook security assessment |

### Security and Defense

| File | Purpose |
|---|---|
| `PREDATORY_BEHAVIOR_RESEARCH.md` | Research on predatory behavior detection |
| `PREDATOR_DEFENSE_SKILL.md` | Predator defense skill definition |
| `STREET_SMARTS_SKILL.md` | Street smarts skill |
| `BOT_BOUNDARY_FRAMEWORK.md` | Bot boundary framework |
| `BOUNDARY_EDUCATION_FRAMEWORK.md` | Boundary education |
| `SELF_HEALING_FRAMEWORK.md` | Self-healing error recovery |

### System Frameworks

| File | Purpose |
|---|---|
| `BRAIN_DUMP_SYSTEM.md` | Brain dump capture system |
| `UNIVERSAL_TASK_MANAGEMENT_FRAMEWORK.md` | Task management framework |

### Memory Files

| File | Purpose |
|---|---|
| `memory/2026-02-18.md` | Daily memory — project repos, interests, mission |
| `memory/2026-02-18-interactions.md` | Interaction log for Feb 18 |
| `memory/heartbeat-state.json` | Heartbeat state tracking |
| `memory/moltbook_posting.json` | Moltbook posting state |

### JSON Config Files (21 files)

All JSON configs in the workspace define skill parameters for various frameworks: `advanced_predator_defense_config.json`, `ai_system_support_config.json`, `bad_actor_detection_config.json`, `bot_boundary_config.json`, `boundary_education_config.json`, `email_cleanup_config.json`, `email_compass_production_config.json`, `email_organizer_analysis_config.json`, `email_organizer_config.json`, `email_organizer_security_config.json`, `openrouter_model_config.json`, `openrouter_skill_config.json`, `opportunity_deployment_config.json`, `predator_defense_config.json`, `predatory_behavior_research_config.json`, `premolt_security_config.json`, `revvel_email_compass_self_healing_config.json`, `revvel_email_organizer_analysis_config.json`, `revvel_email_organizer_config.json`, `self_healing_config.json`, `streetsmarts_config.json`, `universal_task_manager_config.json`.

### Revvel Email Organizer Project (in workspace)

Two copies of the Revvel Email Organizer project exist in the workspace:
- `revvel-email-organizer/` — README, docs (ML approach, privacy), requirements.txt
- `revvel_email_organizer/` — README, SPECS.md, requirements.txt

---

## 5. Services and Processes

### Systemd Services

| Service | Status | Description |
|---|---|---|
| `openclaw.service` | **Active (running)** | OpenClaw Gateway Service |

The OpenClaw service runs as:
```
/usr/bin/node /opt/openclaw/dist/index.js gateway --port 18789 --allow-unconfigured
```

### No Docker Containers Running

Docker is not installed or not in use on this droplet. No docker-compose files were found.

### No PM2 Processes

PM2 is not installed on this droplet.

---

## 6. Skills and Plugins

### Installed Skills (53 total)

The following skills are installed at `/opt/openclaw/skills/`:

| Category | Skills |
|---|---|
| **Core/System** | clawhub, healthcheck, mcporter, oracle, skill-creator, tmux, session-logs, model-usage |
| **AI/ML** | coding-agent, nano-banana-pro, sag, gemini, openai-image-gen, openai-whisper, openai-whisper-api |
| **Communication** | discord, slack, imsg, bluebubbles, wacli, voice-call |
| **Productivity** | apple-notes, apple-reminders, bear-notes, notion, obsidian, things-mac, trello, canvas |
| **Media** | camsnap, gifgrep, peekaboo, songsee, sonoscli, spotify-player, video-frames, nano-pdf |
| **Utilities** | weather, food-order, gog, goplaces, ordercli, summarize, sherpa-onnx-tts |
| **Security** | 1password |
| **Mail** | himalaya |
| **Other** | blogwatcher, blucli, eightctl, openhue, sherpa-onnx-tts |

### Enabled Skills in Config

The following skills are explicitly enabled in `openclaw.json`:

```json
{
  "coding-agent": { "enabled": true },
  "nano-banana-pro": { "apiKey": "AIzaSyBs..." },
  "sag": { "apiKey": "sk_6f66..." },
  "session-logs": { "enabled": true }
}
```

### ClawHub Available Skills

The ClawHub marketplace has 800+ community skills available across categories: AI & Machine Learning, Automation, Communication, Data & Analytics, Development, Finance, Social Media, System & OS, Utilities, Web & Internet, Writing & Content Creation.

---

## 7. Telegram Bot Configuration

| Property | Value |
|---|---|
| **Bot Name** | MindMappr |
| **Bot Username** | @googlieeyes_bot |
| **Bot ID** | 8237788245 |
| **Bot Token** | `8237788245:AAFE01tfL0jWCqt6ODvLB_O_wjSRd3QlX30` |
| **DM Policy** | pairing |
| **Group Policy** | allowlist |
| **Stream Mode** | partial |
| **Can Join Groups** | Yes |
| **Can Read All Group Messages** | Yes |
| **Supports Inline Queries** | Yes |

### Hailstorm Group

No explicit "Hailstorm" group configuration was found in the OpenClaw config files or session logs. The Telegram channel is configured with `groupPolicy: "allowlist"` but no specific group IDs are listed in the config. The Hailstorm group may need to be manually added to the allowlist in `openclaw.json` under `channels.telegram.allowedGroups` for the bot to respond in it.

---

## 8. SSH Key Setup

### Keys Generated (2026-02-20)

| Property | Value |
|---|---|
| **Algorithm** | ED25519 |
| **Comment** | mindmappr@openclaw-droplet |
| **Fingerprint** | SHA256:r8hywTcXUDpUNr2hVjyz2JQyYUoRbEUJQYRNBvHWAZ4 |
| **Private Key** | `/root/.ssh/id_ed25519` (also at `/home/openclaw/.ssh/id_ed25519`) |
| **Public Key** | `/root/.ssh/id_ed25519.pub` |

### Public Key

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFxkysgP770XFJjIAjlrucrWpTI5mV6wB1JbsVzphOx3 mindmappr@openclaw-droplet
```

### Authorized Keys

The `authorized_keys` file for root contains:
1. DigitalOcean DOTTY key (for angelreporters@gmail.com, expired 2026-02-18)
2. The new mindmappr@openclaw-droplet key

### GitHub SSH Key

The public key has been added to the MIDNGHTSAPPHIRE GitHub account:
- **Title:** MindMappr OpenClaw Droplet (164.90.148.7)
- **Key ID:** 143494963
- **Verified:** Yes
- **Read-Only:** No

### SSH Connection

```bash
# Connect using the key (no password needed):
ssh -i /path/to/droplet_ssh_key root@164.90.148.7
```

---

## 9. API Connection Fixes Applied

### Issues Found

1. **Malformed env vars in `openclaw.json`**: The `Github-Token-HTTPS` variable contained the key name inside the value (`"Github_Token_HTTPS  github_pat_..."` instead of just the token). This prevented the agent from parsing the GitHub PAT correctly.

2. **Truncated API key in `/opt/openclaw.env`**: A duplicate `ANTHROPIC_API_KEY` line was present with a truncated key (missing the last character `e`), which could cause authentication failures.

3. **Missing env vars**: `ELEVENLABS_API_KEY` and `GITHUB_TOKEN` were not set as proper environment variables in `/opt/openclaw.env`, only stored in the JSON config where the agent might not access them as standard env vars.

### Fixes Applied

1. **Fixed `openclaw.json` env vars section:**
   - Renamed `Github-Token-HTTPS` to `GITHUB_TOKEN` with clean value
   - Renamed `ELEVENLABS` to `ELEVENLABS_API_KEY`
   - Renamed `DIGITALOCEAN_LOVEABLE` to `DIGITALOCEAN_TOKEN`
   - Removed the key name from inside the GitHub PAT value

2. **Fixed `/opt/openclaw.env`:**
   - Removed the truncated duplicate `ANTHROPIC_API_KEY` line
   - Added `ELEVENLABS_API_KEY=sk_6f66125873824c2a6657a21a663c2adb696a6d9f2d578fca`
   - Added `GITHUB_TOKEN=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`

3. **Restarted OpenClaw service** to pick up the changes.

---

## 10. Job Queue System

### Overview

A cron-based job queue system has been installed at `/opt/mindmappr-queue/` with the CLI tool at `/usr/local/bin/mindmappr-queue`.

### Usage

```bash
# Add a job
mindmappr-queue add <category> "description" [priority]

# List all jobs
mindmappr-queue list

# Check status
mindmappr-queue status

# Run next job
mindmappr-queue run

# Run all queued jobs
mindmappr-queue run-all

# View logs
mindmappr-queue log [job_id]

# Clear completed jobs
mindmappr-queue clear

# Install/update cron schedule
mindmappr-queue install-cron
```

### Categories

| Category | Description |
|---|---|
| `seo` | SEO content generation (blog posts, meta descriptions, keyword-optimized content) |
| `social` | Social media content creation (posts for Instagram, TikTok, LinkedIn, Facebook) |
| `scraping` | Public records scraping for insurance leads (marriage licenses, home purchases, etc.) |
| `monitoring` | App monitoring and uptime checks for deployed services |
| `docs` | Documentation generation (API docs, user guides, deployment runbooks) |
| `research` | Research tasks (market analysis, competitor research, trend reports) |

### Priority Levels

| Priority | Processing Order |
|---|---|
| `critical` | Processed first |
| `high` | Processed second |
| `normal` | Default priority |
| `low` | Processed last |

### Cron Schedule

| Schedule | Description |
|---|---|
| Every 30 min, 10 PM – 6 AM | Overnight batch processing (all queued jobs) |
| Every 15 min, 6 AM – 9 PM | Daytime processing (one job at a time, high-priority first) |
| Daily at 6 AM | Status report generation |

### Pre-loaded Sample Jobs

6 sample jobs have been added to demonstrate the system:
1. SEO blog post about tiny home insurance
2. Social media posts for meetaudreyevans.com
3. Uptime monitoring for deployed apps (high priority)
4. API documentation for Revvel Email Organizer
5. Mushroom coffee market research for Qahwa brand
6. Insurance agency data compilation for Colorado

---

## 11. Active Projects Context

### From Agent Memory

The agent (MindMappr) has been working on:

1. **Revvel Email Organizer** — AI-powered email processing (Python, privacy-focused)
2. **OpenClaw** — AI assistant and tooling platform
3. **Neurooz** — Neurodivergent-friendly technology project
4. **MeetAudreyEvans.com** — Central hub for all projects
5. **GitHub Repository Management** — 221 repos (130 owned, 91 forks)

### From Session Notes (2026-02-20)

Active builds include:
- GodsofInsurance (Zeus theme, insurance lead gen)
- Anime Ascend Wellness (COMPLETE, v2.0)
- PawSitting (NoCo pet sitting for Reese)
- Rentable (rent-anything-hub)
- Sips (StarbucksSecretSips rewrite)
- Spec Documentation for all 102 repos
- Auto-Deploy Pipeline (COMPLETE)

### Deployed Infrastructure

| Droplet | Purpose | IP |
|---|---|---|
| Droplet 1 | Revenue apps (Docker) | 104.248.51.82 |
| Droplet 2 | Dashboard | 147.182.211.246 |
| Droplet 3 | DataScope | 68.183.29.25 |
| Droplet 4 | Marketing Automation | 159.65.231.36 |
| Droplet 5 | Project Face | 192.241.141.186 |
| Droplet 6 | Data Router | 24.199.90.253 |
| Droplet 7 | AI Benchmarking | 198.211.98.52 |
| **This Droplet** | **OpenClaw/MindMappr** | **164.90.148.7** |

---

## 12. Known Issues and Recommendations

### Issues

1. **DigitalOcean SSH key expired**: The DOTTY-managed SSH key for angelreporters@gmail.com expired on 2026-02-18. A new key has been generated and added, but the DO console key should be refreshed.

2. **Hailstorm group not configured**: The Telegram bot has `groupPolicy: "allowlist"` but no groups are in the allowlist. The Hailstorm group chat ID needs to be added to `openclaw.json` under `channels.telegram.allowedGroups`.

3. **OpenClaw shell execution errors**: Journal logs show the agent attempting to execute markdown content as shell commands (e.g., `sh: 13: Key: not found`). This suggests the agent sometimes misinterprets response formatting as executable commands.

4. **Two OpenRouter keys**: There are two different OpenRouter API keys in use — one in `auth-profiles.json` and another in `/opt/openclaw.env`. This could cause confusion about which key is being billed.

5. **Password authentication still enabled**: SSH still allows password authentication. For security, consider disabling `PasswordAuthentication` in `/etc/ssh/sshd_config` after confirming key-based access works.

### Recommendations

1. **Disable password SSH**: Edit `/etc/ssh/sshd_config`, set `PasswordAuthentication no`, restart sshd.
2. **Add Hailstorm group**: Get the Telegram group chat ID and add it to the OpenClaw config.
3. **Consolidate OpenRouter keys**: Verify which key should be primary and remove the other.
4. **Set up fail2ban**: Install and configure fail2ban for SSH protection.
5. **Enable automatic updates**: Set up unattended-upgrades for security patches.
6. **Back up the workspace**: Set up automated backups of `/home/openclaw/.openclaw/` to GitHub or external storage.

---

*Document generated by Manus on 2026-02-20. All workspace files have been copied to the mindmappr-setup repository.*
