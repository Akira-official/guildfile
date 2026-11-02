# 📋 Blueprint Schema & Specification: HelixCore

HelixCore blueprints are declarative YAML or JSON documents that describe the complete architecture and security model of a Discord guild.

---

## 🗂️ Top-Level Document Structure

A blueprint consists of four primary sections:

```yaml
metadata:    # Information about the blueprint
  ...
roles:       # Role hierarchy, colors, and permissions
  ...
categories:  # Channel categories, privacy, and channels
  ...
automod:     # Native security rules and regex filters
  ...
```

---

## 1. `metadata` Section

| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | **Yes** | Server name or template title | `"Helix | AI Agent Community"` |
| `description` | `string` | No | Community purpose or guild topic | `"Official home for AI agents"` |
| `version` | `string` | No | Blueprint version | `"1.0.0"` |
| `author` | `string` | No | Author or organization | `"Vyoma Group"` |

---

## 2. `roles` Section

Roles are created and synchronized in the exact order listed (top to bottom).

```yaml
roles:
  - name: "Core Developer"       # Required: Display name
    color: "#9B59B6"             # Hex color code (defaults to #99AAB5)
    hoist: true                  # Display members separately in sidebar
    mentionable: true            # Allow anyone to @mention this role
    permissions:                 # Mapping of discord.Permissions flags
      administrator: false
      manage_messages: true
      manage_threads: true
      view_audit_log: true
```

### Supported Permission Flags
`administrator`, `manage_guild`, `manage_roles`, `manage_channels`, `kick_members`, `ban_members`, `moderate_members`, `view_audit_log`, `view_guild_insights`, `send_messages`, `send_messages_in_threads`, `manage_messages`, `manage_threads`, `embed_links`, `attach_files`, `read_message_history`, `mention_everyone`, `use_external_emojis`, `connect`, `speak`, `mute_members`, `deafen_members`, `move_members`, `use_voice_activation`.

---

## 3. `categories` Section

Each category groups channels and defines baseline permissions.

```yaml
categories:
  - name: "🔒 ┆ STAFF & OPERATIONS"
    private: true                # If true, @everyone is denied view_channel
    allowed_roles:               # Roles granted explicit view_channel access
      - "Founder"
      - "Senior Moderator"
      - "Ticket Support"
    channels:
      - name: "💼・staff-chat"
        type: "text"             # Channel type: text | voice | forum
        topic: "Internal staff discussion"
        slowmode: 0              # Slowmode in seconds (0 to 21600)
        read_only: false         # If true, @everyone cannot send messages

      - name: "✨・showcase"
        type: "forum"
        topic: "Community showcase threads"

      - name: "🎙️・Staff Meeting"
        type: "voice"
        user_limit: 10           # Max users in voice room (0 for unlimited)
```

---

## 4. `automod` Section

Deploys native Discord AutoMod filters directly into the server:

```yaml
automod:
  # Keyword Filter Rule
  - name: "Block Unapproved Discord Invites"
    trigger_type: "keyword"
    keyword_filter:
      - "*discord.gg/*"
      - "*discord.com/invite/*"
    actions:
      - "block_message"
      - "send_alert_notice: #moderation-log"

  # Regex Secrets Blocker Rule
  - name: "Block Leaked API Keys"
    trigger_type: "regex"
    regex_patterns:
      - "(?i)(gsk_[a-zA-Z0-9]{48})"      # Groq API Key
      - "(?i)(sk-[a-zA-Z0-9]{48})"       # OpenAI API Key
      - "(?i)(ghp_[a-zA-Z0-9]{36})"      # GitHub Personal Access Token
    actions:
      - "block_message"
      - "send_alert_notice: #moderation-log"

  # Anti-Mention Spam Rule
  - name: "Anti-Mention Spam"
    trigger_type: "mention_spam"
    mention_limit: 5
    actions:
      - "block_message"
      - "timeout_member: 300"           # 300 seconds timeout
```
