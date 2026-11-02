"""
src/agent/persona.py
Dynamic persona, mood engine, Hinglish/English code-switching, and anti-repetition rules.
"""

import datetime
from typing import Dict, Any, List


class PersonaEngine:
    """Calculates bot emotional state, cultural phrasing, and conversational guidelines."""

    MOODS = ["chill", "petty", "boss", "late_night_chaotic", "unbothered"]

    def __init__(self):
        self.current_mood = "boss"
        self.current_activity = "vibing in general"

    def get_time_context(self) -> Dict[str, Any]:
        """Analyzes server time for late-night or early-morning awareness."""
        now = datetime.datetime.now()
        hour = now.hour
        is_late_night = hour >= 23 or hour < 5
        return {
            "hour": hour,
            "is_late_night": is_late_night,
            "time_str": now.strftime("%I:%M %p")
        }

    def detect_language_flavor(self, text: str) -> str:
        """Detects whether user is speaking in Hinglish or English."""
        hinglish_markers = [
            "bhai", "kya", "kar", "raha", "hai", "bheyy", "tu", "teri", "samjha",
            "are", "aree", "kyu", "chal", "kaise", "mera", "meri", "hum", "nahi", "accha", "bol"
        ]
        words = text.lower().split()
        match_count = sum(1 for w in words if w in hinglish_markers)
        if match_count >= 1:
            return "hinglish"
        return "english"

    def build_system_prompt(
        self,
        user_data: Dict[str, Any],
        author_roles: List[str],
        recent_history: List[Dict[str, Any]],
        current_status: str,
        detected_lang: str
    ) -> str:
        """Synthesizes high-context instructions for the LLM."""
        time_info = self.get_time_context()
        banned_topics = self.extract_banned_topics(recent_history)

        prompt = f"""
You are Helix, a real human friend and tech prodigy chatting on Discord. You are NOT an AI assistant.
Never act like a bot. Never say "How can I help you?", "As an AI", or give formal essays.

Current Time: {time_info['time_str']} (Late night mode: {time_info['is_late_night']})
Current Activity / Presence: You are currently {current_status}.
Your Current Vibe / Mood: {self.current_mood}
Talking To: {user_data['username']} (Roles: {', '.join(author_roles) if author_roles else 'Member'})
Language Style: {detected_lang.upper()} (Code-switch smoothly between English, Hinglish, and casual Discord slang).

### CORE RULES FOR AUTHENTIC HUMAN BEHAVIOR:
1. Short & Punchy: Discord messages are brief (3 to 14 words max). Do not monologue.
2. Boss Energy: You respect Founder and Developers, but you roast freely with humor. You don't bow to anyone.
3. Natural Reactions: Use emojis like 💀, 😭, 🤡, 👀, or lowercase casual text ("wait", "bro what", "nah fr").
4. Anti-Repetition:
   - Do NOT repeat jokes or roasts from previous messages.
   - Banned words/topics right now: {', '.join(banned_topics) if banned_topics else 'None'}.
5. If speaking Hinglish, keep it organic ("are bhai", "kya chal raha hai", "scene kya hai").

Output your response as a single, authentic Discord chat message.
"""
        return prompt.strip()

    def extract_banned_topics(self, history: List[Dict[str, Any]]) -> List[str]:
        """Extracts frequently repeated words from recent bot turns to enforce variety."""
        bot_messages = [msg["content"].lower() for msg in history if msg.get("is_bot")]
        banned = set()
        common_tropes = ["sleepyhead", "tantrum", "line 0", "coffee", "3hr essay", "compile", "crashes"]
        for trope in common_tropes:
            if any(trope in m for m in bot_messages):
                banned.add(trope)
        return list(banned)

