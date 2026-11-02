<div align="center">

# 🌐 HelixCore
### Declarative Discord Server Provisioner & Autonomous Antigravity AI Agent Harness

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-v2.3.2-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io)
[![Groq Cloud](https://img.shields.io/badge/Powered%20By-Groq%20LPU-f55036?logo=groq&logoColor=white)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*Set up production-grade, enterprise-hardened Discord servers in 3 minutes using Infrastructure-as-Code manifests, paired with a hyper-human, autonomous AI community companion.*

---

[Quickstart](#-quickstart-guide-in-5-minutes) • [Architecture](#-architecture--how-it-works) • [Blueprint Engine](#-declarative-blueprint-engine) • [Helix AI Companion](#-the-helix-ai-companion) • [Documentation Index](#-documentation-index) • [Docker](#-docker-deployment) • [FAQ](#-frequently-asked-questions)

</div>

---

## 💡 Why HelixCore?

Setting up a modern, enterprise-grade Discord server takes **15–20 hours** of manual clicking:
- Creating 25+ roles with precise colors and permission bitmasks.
- Configuring isolated category permissions for staff and moderation teams.
- Setting up complex regex AutoMod rules to block token leaks and invite spam.
- Configuring ticket desks, onboarding questions, and forum tags.
- Most existing Discord bots are bloated with ads, lock essential features behind expensive monthly paywalls (MEE6), or send stiff, robotic Wikipedia summaries.

**HelixCore provides a complete, modern open-source alternative:**
1. **Infrastructure-as-Code (IaC) for Discord**: Define your entire server architecture in a clean, human-readable YAML blueprint. Apply it idempotently in seconds without wiping existing channels or messages.
2. **Autonomous AI Companion ("Helix")**: Powered by Groq LPUs (`openai/gpt-oss-120b`), Helix chats with authentic human-like behavior: rapid-fire multi-message burst typing, dynamic mood swings, Hinglish/English code-switching, SQLite relationship memory, multimodal meme roasting, and Discord presence cycling.
3. **Built for Agentic AI Pair-Programming**: Engineered to integrate seamlessly with Google Antigravity, Cursor, and Claude Code via structured documentation and CLI harnesses.

---

## 🏗️ Architecture & How It Works

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                           USER & DEVELOPER                             │
 └───────────────────┬────────────────────────────────┬───────────────────┘
                     │                                │
        [ Declarative Blueprint YAML ]        [ Chat Interaction ]
                     │                                │
                     ▼                                ▼
 ┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐
 │          PROVISIONING SUBSYSTEM      │  │        AUTONOMOUS AGENT SUBSYSTEM    │
 ├──────────────────────────────────────┤  ├──────────────────────────────────────┤
 │  • Blueprint Loader (YAML / JSON)    │  │  • Discord Gateway Event Listener    │
 │  • Pydantic Schema Validation        │  │  • SQLite Social Graph (Memory DB)   │
 │  • Idempotent State Diff Engine      │  │  • Dynamic Persona & Mood Engine     │
 │  • Role Hierarchy Synchronizer       │  │  • Hinglish/English Code-Switcher    │
 │  • Category & Channel Provisioner    │  │  • Groq LPU Inference (OSS-120B)    │
 │  • Baseline Security Hardening       │  │  • Multimodal Meme Vision Roaster    │
 │  • AutoMod RegEx Rules Injector      │  │  • Burst Typing Simulator            │
 └───────────────────┬──────────────────┘  └──────────────────┬───────────────────┘
                     │                                        │
                     └───────────────────┬────────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │         Discord REST & Gateway       │
                      │     (discord.py Async Runtime)       │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │       Live Discord Community         │
                      └──────────────────────────────────────┘
```

---

## 🚀 Quickstart Guide (in 5 Minutes)

### 1. Prerequisites
- **Python 3.10, 3.11, or 3.12** installed on your system.
- A **Discord Bot Token** from the [Discord Developer Portal](https://discord.com/developers/applications):
  * Under the **Bot** tab, enable **`Message Content Intent`** and **`Server Members Intent`**.
  * Invite the bot to your server with `Administrator` permissions.
- A free **Groq API Key** from the [Groq Console](https://console.groq.com/keys).

### 2. Clone & Install
```bash
# Clone the repository
git clone https://github.com/your-username/HelixCore.git
cd HelixCore

# Create and activate a virtual environment
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install in editable mode
pip install -e .
```

### 3. Configure Credentials
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your keys:
```env
DISCORD_TOKEN=MTU2NjU2...
DISCORD_GUILD_ID=1564658375613091890
GROQ_API_KEY=gsk_nPBk38...
```

### 4. Verify System Health (`doctor`)
Run the automated environment and database check:
```bash
helixcore doctor
```
```text
🔍 Running HelixCore Doctor System Diagnostics...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ [DISCORD_TOKEN]: Configured (Length: 72)
✅ [DISCORD_GUILD_ID]: Configured (1564658375613091890)
✅ [GROQ_API_KEY]: Configured (Length: 56)
✅ [SQLITE_ENGINE]: Verified functional (In-Memory & Persistent Ready)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Diagnostics Complete!
```

### 5. Provision the Server with a Blueprint (`apply`)
Apply the official AI Agent Community template:
```bash
helixcore apply --blueprint templates/ai-agent-community.yaml
```

### 6. Launch the Helix AI Companion (`agent`)
Start Helix in your server:
```bash
helixcore agent
```

---

## 📜 Declarative Blueprint Engine

Blueprints are human-readable YAML documents defining your server's entire hierarchy and permissions.

### Example Blueprint Snippet
```yaml
metadata:
  name: "Helix | AI Agent Community"
  description: "Official community for AI agents, developers, and builders."
  version: "1.0.0"

roles:
  - name: "Founder"
    color: "#E74C3C"
    hoist: true
    permissions:
      administrator: true

  - name: "Community Administrator"
    color: "#E67E22"
    hoist: true
    permissions:
      manage_guild: true
      manage_roles: true
      manage_channels: true

  - name: "Ticket Support"
    color: "#3498DB"
    hoist: false

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
      - name: "✨・showcase"
        type: "forum"
      - name: "🔊・Community Lounge"
        type: "voice"

  - name: "🔒 ┆ STAFF & OPERATIONS"
    private: true
    allowed_roles:
      - "Founder"
      - "Community Administrator"
      - "Ticket Support"
    channels:
      - name: "💼・staff-chat"
        type: "text"
      - name: "📜・ticket-transcripts"
        type: "text"
```

> 📖 **Full Blueprint Documentation**: Check out [`docs/BLUEPRINT_SCHEMA.md`](docs/BLUEPRINT_SCHEMA.md) for all supported fields, permission bitmasks, and AutoMod triggers.

---

## 🤖 The Helix AI Companion

Helix is engineered to overcome every flaw of traditional AI chatbots:

### 1. Multi-Message "Burst" Typing
Real humans send rapid-fire mini messages instead of walls of text:
```text
[8:15 AM] Akira: yo helix are you awake?
[8:15 AM] Helix: yeah what's up?
[8:15 AM] Helix: spit it out, i'm all ears
```

### 2. Multimodal Meme Vision (Roasting)
Upload a photo, selfie, gameplay clip, or buggy code screenshot into `#general-chat`:
* Helix automatically inspects the image using Groq multimodal vision (`qwen-2.5-32b`).
* It drops an instant, witty critique or roast:
  > *"who told you to upload this blurfest 💀 looks like you took this screenshot with a microwave"*

### 3. Cultural Code-Switching (English / Hinglish / Slang)
* Automatically detects language markers (`bhai`, `kya`, `scene`, `samjha`) and code-switches organically:
  > *"are bhai, diamond mine kar raha hu... tu bata tera code compile hua ya abhi bhi line 0 pe atka hai? 💀"*

### 4. SQLite Social Graph & Relationship Memory
* Remembers user closeness scores (0–100), personalized nicknames, and shared inside jokes across server restarts.
* Features an **anti-repetition engine** that blacklists overused jokes from previous turns.

### 5. Dynamic Presence Cycling
* In the background, Helix rotates its rich presence every few minutes:
  * 🎮 Playing: `Minecraft (mining diamonds 💎)`
  * 🎮 Playing: `VALORANT (bottom fragging 💀)`
  * 🎧 Listening to: `Spotify - 3hr video essay`
  * 📺 Watching: `people take Ls in 4K`

> 📖 **Full Agent Realism Deep Dive**: Read [`docs/AGENT_HARNESS.md`](docs/AGENT_HARNESS.md).

---

## 📚 Documentation Index

For in-depth developer and agent documentation, explore the [`docs/`](docs/) directory:

| Document | Description |
| :--- | :--- |
| **[`docs/AI_AGENT_INSTRUCTIONS.md`](docs/AI_AGENT_INSTRUCTIONS.md)** | Mandatory guide for AI coding agents (Antigravity, Cursor, Claude Code) working on HelixCore. |
| **[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)** | Deep architectural specifications, pipeline diagrams, database schemas, and performance specs. |
| **[`docs/BLUEPRINT_SCHEMA.md`](docs/BLUEPRINT_SCHEMA.md)** | Complete YAML/JSON schema reference for roles, categories, channels, permissions, and AutoMod. |
| **[`docs/AGENT_HARNESS.md`](docs/AGENT_HARNESS.md)** | Detailed breakdown of burst typing, mood algorithms, Hinglish switching, and multimodal vision. |
| **[`docs/CLI_REFERENCE.md`](docs/CLI_REFERENCE.md)** | Manual for the `helixcore` command line interface, flags, and environment variables. |
| **[`docs/ANTIGRAVITY_INTEGRATION.md`](docs/ANTIGRAVITY_INTEGRATION.md)** | Guide on controlling and extending HelixCore via Google Antigravity agentic workflows. |

---

## 🐳 Docker Deployment

Self-host HelixCore 24/7 on any cloud VPS (AWS, DigitalOcean, Railway, or Raspberry Pi) with Docker Compose:

```bash
cd docker
docker compose up -d --build
```

Your persistent SQLite memory graph (`helix_memory.db`) and rotating logs (`helixcore.log`) mount directly to the host machine for seamless backups.

---

## ❓ Frequently Asked Questions

<details>
<summary><b>Q: Does running <code>helixcore apply</code> wipe existing chat messages?</b></summary>
<b>No!</b> The Provisioning Engine is strictly idempotent. It inspects existing categories and channels and only creates missing elements or updates permissions. Existing message history is completely untouched.
</details>

<details>
<summary><b>Q: Why do I get <code>PrivilegedIntentsRequired</code> error?</b></summary>
You must enable <b>Message Content Intent</b> in your bot's settings on the <a href="https://discord.com/developers/applications">Discord Developer Portal</a> under the <b>Bot</b> tab. Helix requires this intent to read and respond to chat messages.
</details>

<details>
<summary><b>Q: Can I use OpenAI or Anthropic models instead of Groq?</b></summary>
Yes! HelixCore uses an OpenAI-compatible interface. If you provide an <code>OPENAI_API_KEY</code> without a Groq key, it seamlessly routes requests to OpenAI.
</details>

---

## 🤝 Contributing

We welcome contributions of all kinds! Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

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
