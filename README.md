<div align="center">

# 🌐 HelixCore
### Declarative Discord Server Provisioner & Autonomous Antigravity AI Agent Harness

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-v2.3.2-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
[![Groq Cloud](https://img.shields.io/badge/Powered%20By-Groq%20LPU-f55036?logo=groq&logoColor=white)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*Set up production-grade Discord servers in 3 minutes with Infrastructure-as-Code blueprints, paired with a hyper-human, autonomous AI community companion.*

[Quickstart](#-quickstart-guide) • [Architecture](#-architecture) • [Blueprint Schema](#-blueprint-schema) • [Agent Features](#-the-helix-ai-companion) • [Docker](#-docker-deployment) • [Contributing](#-contributing)

</div>

---

## 💡 What is HelixCore?

Setting up a modern, enterprise-grade Discord server takes **15–20 hours** of manual clicking: creating 20+ roles, configuring channel permission matrices, setting up regex AutoMod rules, and tuning onboarding. Most server bots are bloated, paid, or stiff.

**HelixCore solves this permanently:**
1. **Infrastructure-as-Code for Discord**: Define your entire server (roles, categories, channels, permissions, AutoMod, and tickets) in a declarative YAML manifest. Apply it with a single command (`helixcore apply`).
2. **Living, Hyper-Human AI Companion ("Helix")**: A Groq-powered autonomous AI agent that chats like a real friend with rapid-fire mini-messages, typing pauses, multimodal meme roasting, emotional memory, and Discord presence cycling.

---

## ⚡ Features at a Glance

| Feature | Description |
| :--- | :--- |
| **Declarative Provisioning** | Define roles, channels, permissions, and categories in clean YAML blueprints. |
| **Idempotent Sync** | Safely updates roles and channels without wiping existing chat history or servers. |
| **Security Hardening** | Automatically deploys 5 native AutoMod rules and seals `@everyone` permissions. |
| **Hyper-Human Bursts** | Splits responses into 2–3 rapid-fire mini-messages with realistic typing delays. |
| **Multimodal Meme Vision** | Inspects photos, selfies, and code screenshots with Groq vision to roast or critique. |
| **SQLite Social Graph** | Remembers user closeness scores, nicknames, and past inside jokes over time. |
| **Hinglish & Slang Adaptability** | Seamlessly detects and code-switches between English, Hinglish, and developer banter. |
| **Rich Presence Cycling** | Automatically rotates games (Minecraft, VALORANT), Spotify listening, and mood statuses. |
| **Antigravity Harness** | Ready for AI pair-programming agents and MCP tools to govern servers autonomously. |

---

## 🏗️ Architecture

```text
                             ┌─────────────────────────────────┐
                             │       Developer / Admin CLI     │
                             └────────────────┬────────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
      ┌───────────────────────────────┐               ┌───────────────────────────────┐
      │       PROVISIONING CORE       │               │       AUTONOMOUS AGENT        │
      │    (Declarative Blueprint)    │               │       (Helix AI Companion)    │
      ├───────────────────────────────┤               ├───────────────────────────────┤
      │ • Role Hierarchy & Perms      │               │ • Multi-Message Burst Engine  │
      │ • Category & Channel Trees    │               │ • SQLite Social Graph Memory  │
      │ • AutoMod RegEx & Filters     │               │ • Multimodal Meme Vision      │
      │ • Ticket Desk & Permissions   │               │ • Dynamic Presence & Status   │
      │ • Idempotent State Diffing    │               │ • Hinglish/English Code-Switch│
      └───────────────┬───────────────┘               └───────────────┬───────────────┘
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │      Discord API & Gateway      │
                             └─────────────────────────────────┘
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python **3.10+**
- A Discord Bot Token ([Discord Developer Portal](https://discord.com/developers/applications))
  * *Enable `Message Content Intent` and `Server Members Intent` under the Bot tab.*
- A Groq API Key ([Groq Console](https://console.groq.com/keys))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/HelixCore.git
cd HelixCore

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -e .
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id_here
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 4. Verify System Health
Run the built-in diagnostic doctor:
```bash
helixcore doctor
```

### 5. Provision Your Server with a Blueprint
Apply the official AI Agent Community blueprint to your target server:
```bash
helixcore apply --blueprint templates/ai-agent-community.yaml
```

### 6. Start the Helix AI Companion
Launch the autonomous chatbot:
```bash
helixcore agent
```

---

## 📜 Blueprint Schema

Blueprints are written in simple YAML. Below is a minimal example:

```yaml
metadata:
  name: "My Community"
  version: "1.0.0"

roles:
  - name: "Core Maintainer"
    color: "#E74C3C"
    hoist: true
    permissions:
      administrator: true
  - name: "Community Member"
    color: "#3498DB"

categories:
  - name: "📌 ┆ START HERE"
    channels:
      - name: "👋・welcome"
        type: "text"
        read_only: true
      - name: "📜・rules"
        type: "text"
        read_only: true

  - name: "💬 ┆ COMMUNITY"
    channels:
      - name: "💬・general-chat"
        type: "text"
        slowmode: 2
      - name: "🔊・General Lounge"
        type: "voice"

  - name: "🔒 ┆ STAFF"
    private: true
    allowed_roles:
      - "Core Maintainer"
    channels:
      - name: "💼・staff-chat"
        type: "text"
```

Ready-made templates are available in the [`templates/`](templates/) folder:
- `templates/ai-agent-community.yaml`: Full enterprise blueprint with support desks, forums, and ticket categories.
- `templates/dev-startup.yaml`: Streamlined layout for open-source repositories and dev teams.

---

## 🤖 The Helix AI Companion

Helix is designed to feel indistinguishable from an authentic, witty friend:

- **Burst Messaging**: Instead of a monolithic paragraph, Helix sends short rapid-fire messages:
  ```text
  [8:15 AM] Akira: yo helix are you awake?
  [8:15 AM] Helix: yeah what's up?
  [8:15 AM] Helix: spit it out, i'm all ears
  ```
- **Time-of-Day Awareness**: Detects 3:00 AM late-night chatters:
  > *"why are you awake right now bro? go to sleep 😭"*
- **Vision Roasts**: Drop a blurry selfie, broken code screenshot, or meme into `#general-chat`, and Helix will inspect and roast it on sight.
- **Silent Lurking**: Sometimes real friends don't talk—they just drop a `💀` or `👀` reaction and keep scrolling.

---

## 🐳 Docker Deployment

To self-host the Helix agent on any VPS (AWS, DigitalOcean, Railway) with Docker Compose:

```bash
cd docker
docker compose up -d --build
```
Your SQLite memory graph and logs persist in the host directory automatically.

---

## 🤝 Contributing

We love contributions! Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feat/amazing-feature`)
3. Commit your Changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the Branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<div align="center">
Built with ❤️ by the <b>Helix Community</b> & <b>Vyoma Group</b>.
</div>
