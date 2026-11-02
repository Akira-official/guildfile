# 💻 CLI Reference Manual: HelixCore

HelixCore includes a unified Command-Line Interface (`helixcore` or `python -m src.cli.main`) for server provisioning, health auditing, and agent control.

---

## 🛠️ Global Syntax

```bash
helixcore [COMMAND] [OPTIONS]
# or
python -m src.cli.main [COMMAND] [OPTIONS]
```

---

## 📌 Available Commands

### 1. `doctor`
Performs comprehensive system diagnostics, credential verification, and database checks.

```bash
helixcore doctor
```

**What it tests:**
- ✅ Presence and length of `DISCORD_TOKEN`.
- ✅ Configuration of `DISCORD_GUILD_ID`.
- ✅ Validation of `GROQ_API_KEY`.
- ✅ In-Memory and persistent SQLite database operations.

---

### 2. `apply`
Applies a declarative YAML or JSON blueprint to the configured Discord server.

```bash
helixcore apply --blueprint <PATH_TO_YAML>
# Short flag:
helixcore apply -b templates/ai-agent-community.yaml
```

**Options:**
| Flag | Short | Required | Description |
| :--- | :--- | :--- | :--- |
| `--blueprint` | `-b` | **Yes** | Path to the YAML or JSON blueprint file. |

**Execution Pipeline:**
1. Loads and validates YAML structure against Pydantic schema.
2. Synchronizes roles (names, colors, hoist, and permissions).
3. Hardens `@everyone` baseline permissions.
4. Synchronizes categories and channels (text, voice, forums).
5. Applies permission overwrites for private channels.

---

### 3. `agent`
Launches the autonomous Helix AI companion bot in chat channels.

```bash
helixcore agent
```

**Requirements:**
- `DISCORD_TOKEN` with `Message Content Intent` enabled in Discord Developer Portal.
- `GROQ_API_KEY` for ultra-low latency inference.

**Runtime Logs:**
Logs stream in real-time to stdout and rotate into `helixcore.log` (5MB cap, 3 backups).

---

## 🌐 Environment Variables Reference

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `DISCORD_TOKEN` | **Yes** | `None` | Bot authentication token from Developer Portal. |
| `DISCORD_GUILD_ID` | Yes (for apply) | `None` | Target Discord server ID. |
| `GROQ_API_KEY` | Recommended | `None` | Groq LPU API key for ultra-fast generation. |
| `GROQ_MODEL` | No | `openai/gpt-oss-120b` | Flagship reasoning chat model. |
| `GROQ_VISION_MODEL`| No | `qwen-2.5-32b` | Multimodal model for meme/screenshot roasts. |
| `MEMORY_DB_PATH` | No | `helix_memory.db` | Path to persistent SQLite memory graph. |
| `LOG_LEVEL` | No | `INFO` | Console verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
