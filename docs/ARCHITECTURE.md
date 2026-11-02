# 🏗️ Architecture & Technical Specification: HelixCore

This document describes the architectural design, component interactions, data pipelines, and security mechanisms of **HelixCore**.

---

## 🏛️ High-Level System Architecture

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
 │  1. Blueprint Loader (YAML)          │  │  1. Discord Gateway Listener         │
 │  2. Pydantic Schema Validator        │  │  2. Social Graph Memory (SQLite)     │
 │  3. Discord State Diff Engine        │  │  3. Dynamic Persona & Mood Engine    │
 │  4. Role Hierarchy Synchronizer      │  │  4. Hinglish/English Code-Switcher   │
 │  5. Category & Channel Provisioner   │  │  5. Groq LPU Inference (OSS-120B)   │
 │  6. Permission Overwrites Compiler   │  │  6. Multimodal Meme Vision Roaster   │
 │  7. AutoMod Rule Injector            │  │  7. Burst Message & Delay Simulator  │
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
                      │      Target Discord Community        │
                      └──────────────────────────────────────┘
```

---

## ⚙️ Subsystem 1: Declarative Provisioner

### 1. Data Flow & Compilation
The Provisioning Engine operates like a compiler for Discord server infrastructure:
1. **Source**: An input YAML document (`templates/ai-agent-community.yaml`).
2. **Abstract Syntax / Schema**: Pydantic models (`BlueprintSchema`, `RoleSchema`, `CategorySchema`, `ChannelSchema`) validate data types, colors, and permission dictionaries.
3. **Diffing & Idempotence**:
   - The engine checks current server state via `guild.roles`, `guild.categories`, and `guild.channels`.
   - Missing entities are created.
   - Modified entities are updated with `.edit()`.
   - Existing messages, threads, and user histories are strictly preserved.

### 2. Permission Hardening Pipeline
- **Baseline `@everyone` Lockdown**: Revokes `administrator`, `manage_guild`, `manage_roles`, `mention_everyone`, and `create_instant_invite`.
- **Private Category Inheritance**: When a category is marked `private: true`, children inherit `view_channel=False` for `@everyone` and explicit `view_channel=True` for roles listed in `allowed_roles`.
- **Channel Overrides**: Read-only announcement channels grant `@everyone` `read_messages=True` and `send_messages=False`.

---

## 🧠 Subsystem 2: The Autonomous Agent ("Helix")

### 1. Conversational Event Loop
```text
Discord Gateway Event (on_message)
  │
  ├──► 1. Guard Checks (Ignore self, ignore bots, check active channel / mentions)
  │
  ├──► 2. Social Graph Ingestion (Record user interaction, increment closeness)
  │
  ├──► 3. Probabilistic Reaction (15% chance to silently drop 💀/👀 and exit)
  │
  ├──► 4. Multimodal Check (If image attached ➔ invoke Vision Model roast)
  │
  ├──► 5. Context Synthesis (Fetch recent turns, user roles, current status, time)
  │
  ├──► 6. Persona & Anti-Repetition Modulation (Filter banned topics & code-switch)
  │
  ├──► 7. Groq Ultra-Low Latency Inference (openai/gpt-oss-120b)
  │
  ├──► 8. Deduplication Guard (difflib.SequenceMatcher against previous replies)
  │
  ├──► 9. Burst Message Splitting (Partition text into 1–2 rapid-fire mini messages)
  │
  └──► 10. Humanized Typing Simulation (Typing indicator with variable delay) ➔ Dispatch
```

### 2. Social Graph & Memory Schema (SQLite)
The agent maintains an embedded, persistent SQLite database (`helix_memory.db`) with three relational tables:

```sql
-- Tracks every community member's relationship with Helix
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    nickname TEXT,
    closeness INTEGER DEFAULT 0,          -- Relationship score (0 to 100)
    mood_towards TEXT DEFAULT 'neutral',  -- Friendly, petty, roasting, supportive
    traits TEXT DEFAULT '[]',             -- JSON list: ["coder", "night_owl", "gamer"]
    inside_jokes TEXT DEFAULT '[]',       -- JSON list of shared memorable moments
    last_seen REAL DEFAULT 0,
    notes TEXT DEFAULT ''
);

-- Stores conversational buffer per channel for high-context generation
CREATE TABLE message_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id TEXT,
    user_id TEXT,
    username TEXT,
    content TEXT,
    is_bot INTEGER DEFAULT 0,
    timestamp REAL
);

-- Persistent key-value store for global bot state
CREATE TABLE bot_state (
    key TEXT PRIMARY KEY,
    value TEXT
);
```

---

## ⚡ Performance & Latency Specifications

- **Groq LPU Inference**: ~300–450 tokens/second on `openai/gpt-oss-120b`. First-token latency typically `< 400ms`.
- **Typing Simulation**: Injected artificial micro-delays between `0.8s` and `1.8s` based on word count to perfectly mimic authentic human typing speed.
- **SQLite Transactions**: Connection pooling with WAL (Write-Ahead Logging) compatibility ensures sub-millisecond query execution.
- **Memory Footprint**: Average idle RAM consumption `< 65MB` in Python runtime, `< 95MB` in Docker container.
