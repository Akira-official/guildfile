# 🌌 Google Antigravity Integration Guide: HelixCore

HelixCore is built from the ground up to pair natively with **Google Antigravity (AGY)** and agentic coding workflows.

---

## 🎯 What is the Antigravity Connection?

When you connect an Antigravity agent to HelixCore:
- You don't have to manually edit YAML blueprints or write Discord API calls.
- You can command your AI pair-programmer in plain English:
  * *"Antigravity, add a new 'VIP Early Access' role to our server with gold color and private lounge access."*
  * *"Antigravity, audit our server permissions and ensure moderation logs are hidden from normal members."*
  * *"Antigravity, tune Helix's persona to be more sarcastic when people ask about release dates."*

---

## 🔌 Using HelixCore as an Antigravity Skill / Tool

Antigravity agents can invoke HelixCore via the native `run_command` tool:

```python
# 1. Run server diagnostics
run_command(
    CommandLine="python -m src.cli.main doctor",
    WaitMsBeforeAsync=5000,
    toolSummary="Check HelixCore environment"
)

# 2. Deploy modified blueprints
run_command(
    CommandLine="python -m src.cli.main apply -b templates/ai-agent-community.yaml",
    WaitMsBeforeAsync=10000,
    toolSummary="Apply Discord blueprint"
)

# 3. Launch or verify autonomous agent
run_command(
    CommandLine="python -m src.cli.main agent",
    WaitMsBeforeAsync=500,
    IsDaemon=True,
    toolSummary="Run Helix AI Companion"
)
```

---

## 🤖 Antigravity Subagent Best Practices for Discord

When delegating Discord server tasks to Antigravity subagents:
1. **Always run `doctor` first**: Check that `DISCORD_TOKEN` and intents are valid before attempting API calls.
2. **Validate Blueprints Locally**: Use `load_blueprint()` to catch syntax or schema errors before touching the live Discord server.
3. **Respect Hierarchy**: In Discord, bots cannot modify roles or channels positioned above the bot's own top role. Make sure the bot's role is near the top of the server hierarchy.
