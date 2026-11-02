# 🤖 AI Agent & Developer Instructions: HelixCore

> **Purpose**: This guide is specifically written for AI agents (Google Antigravity, Claude Code, Cursor, Copilot) and autonomous systems working with or modifying **HelixCore**.

---

## 📌 System Identity & Philosophy
HelixCore is a dual-engine Discord automation ecosystem:
1. **The Provisioning Engine**: A declarative, idempotent Infrastructure-as-Code (IaC) framework that compiles YAML/JSON blueprints into live Discord guilds via `discord.py`.
2. **The Autonomous Agent Engine ("Helix")**: A hyper-human, low-latency companion bot powered by Groq LPUs (`openai/gpt-oss-120b`), designed to simulate authentic human communication patterns on Discord.

### ⚠️ Cardinal Rules for AI Agents
1. **Idempotence First**: When modifying or applying blueprints, never delete channels or wipe user messages unless explicitly instructed. Always diff and sync.
2. **Never Hardcode Credentials**: Never write Discord tokens, Groq keys, or webhooks into codebase files. Always use `.env` and `os.getenv()`.
3. **Respect Discord Rate Limits**: Discord Gateway & REST API enforce strict rate limits (5 requests/second per route, 50 guild edits/10 minutes). Ensure delays and backoffs are respected.
4. **Human Realism over AI Formality**: The chatbot must never talk like ChatGPT or a customer support bot. No "How may I assist you?", no multi-paragraph summaries. Keep it short, witty, bursty, and contextual.

---

## 🧭 Key Project Paths & Modules

| Path | Purpose | What Agents Should Know |
| :--- | :--- | :--- |
| `src/core/blueprint_parser.py` | Blueprint YAML parsing & Pydantic schema | Modify this when adding new blueprint capabilities (e.g., custom emoji packs, sticker templates). |
| `src/core/provisioner.py` | Discord API synchronization engine | Handles role creation, `@everyone` hardening, category permissions, and text/voice/forum creation. |
| `src/agent/ai_client.py` | LLM inference & multimodal vision | Integrates Groq / OpenAI SDKs. Uses `difflib.SequenceMatcher` to prevent the bot from repeating jokes. |
| `src/agent/chat_manager.py` | Conversational orchestrator | Controls rolling buffer, burst message splitting, typing delays, and probabilistic reactions (15% chance). |
| `src/agent/database.py` | SQLite Social Graph & Memory | Persistent SQLite storage for user profiles, closeness scores (0–100), nicknames, and chat history. |
| `src/agent/persona.py` | Dynamic mood & language switching | Detects Hinglish vs. English markers, late-night awareness, and maintains topic blacklists. |
| `src/agent/status_cycler.py` | Presence & Activity cycler | Background loop rotating games (Minecraft, VALORANT) and Spotify states. |
| `src/cli/main.py` | Command-line interface | Unified entrypoint for `doctor`, `apply`, and `agent` subcommands. |
| `templates/` | Pre-built community blueprints | Production-ready YAML manifests (`ai-agent-community.yaml`, `dev-startup.yaml`). |

---

## 🛠️ Common Workflows for AI Agents

### 1. Extending the Blueprint Schema
If you need to support new Discord features (e.g., voice channel bitrate, NSFW filters):
1. Add the field to `ChannelSchema` or `RoleSchema` in `src/core/blueprint_parser.py`.
2. Update the sync logic in `src/core/provisioner.py` (`_sync_channel()` or `sync_roles()`).
3. Add a test case in `tests/test_blueprint_parser.py`.
4. Update `docs/BLUEPRINT_SCHEMA.md`.

### 2. Modifying Agent Personality & Tone
To adjust Helix's conversational tone:
1. Edit `PersonaEngine.build_system_prompt()` in `src/agent/persona.py`.
2. Update `common_tropes` in `extract_banned_topics()` to prevent overused phrases.
3. Test language switching with `PersonaEngine.detect_language_flavor()`.

### 3. Adding New LLM Providers
To add Anthropic Claude or Ollama local models:
1. Extend `AIClient.__init__()` in `src/agent/ai_client.py`.
2. Implement fallback logic in `generate_chat_reply()`: try primary provider (Groq) -> on failure/rate limit, fall back to secondary.

---

## 🔍 Verification Checklist for Code Changes
Before completing any task, execute:
```bash
# 1. Environment and database integrity check
python -m src.cli.main doctor

# 2. Syntax and lint verification
python -m unittest discover tests

# 3. Blueprint validation check
python -c "from src.core.blueprint_parser import load_blueprint; load_blueprint('templates/ai-agent-community.yaml'); print('OK')"
```
