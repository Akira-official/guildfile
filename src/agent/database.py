"""
src/agent/database.py
Persistent SQLite Social Graph & Memory Engine for Helix.
"""

import sqlite3
import json
import time
from typing import Dict, Any, List, Optional
from ..utils.logger import setup_logger

logger = setup_logger("HelixCore.Database")


class AgentMemoryDB:
    """Manages persistent user closeness, memory tags, inside jokes, and dialogue history."""

    def __init__(self, db_path: str = "helix_memory.db"):
        self.db_path = db_path
        self._mem_conn = None
        if self.db_path == ":memory:":
            self._mem_conn = sqlite3.connect(":memory:")
            self._mem_conn.row_factory = sqlite3.Row
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if self._mem_conn:
            return self._mem_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            # User Social Graph
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT,
                    nickname TEXT,
                    closeness INTEGER DEFAULT 0,
                    mood_towards TEXT DEFAULT 'neutral',
                    traits TEXT DEFAULT '[]',
                    inside_jokes TEXT DEFAULT '[]',
                    last_seen REAL DEFAULT 0,
                    notes TEXT DEFAULT ''
                )
            """)

            # Bot Emotional State
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bot_state (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

            # Conversation Memory
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS message_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT,
                    user_id TEXT,
                    username TEXT,
                    content TEXT,
                    is_bot INTEGER DEFAULT 0,
                    timestamp REAL
                )
            """)
            conn.commit()

    def get_or_create_user(self, user_id: str, username: str) -> Dict[str, Any]:
        """Retrieves user profile from social graph or initializes a new one."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
            row = cursor.fetchone()
            if row:
                data = dict(row)
                data["traits"] = json.loads(data["traits"])
                data["inside_jokes"] = json.loads(data["inside_jokes"])
                return data

            default_data = {
                "user_id": str(user_id),
                "username": username,
                "nickname": username,
                "closeness": 10,
                "mood_towards": "neutral",
                "traits": [],
                "inside_jokes": [],
                "last_seen": time.time(),
                "notes": ""
            }
            cursor.execute("""
                INSERT INTO users (user_id, username, nickname, closeness, mood_towards, traits, inside_jokes, last_seen, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(user_id), username, username, 10, "neutral", "[]", "[]", time.time(), ""
            ))
            conn.commit()
            return default_data

    def record_interaction(self, user_id: str, username: str, content: str, is_bot: bool, channel_id: str):
        """Records a chat event and updates user activity in the social graph."""
        now = time.time()
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO message_history (channel_id, user_id, username, content, is_bot, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(channel_id), str(user_id), username, content, 1 if is_bot else 0, now))

            if not is_bot:
                cursor.execute("""
                    UPDATE users
                    SET last_seen = ?,
                        closeness = MIN(100, closeness + 1)
                    WHERE user_id = ?
                """, (now, str(user_id)))
            conn.commit()

    def get_recent_history(self, channel_id: str, limit: int = 12) -> List[Dict[str, Any]]:
        """Retrieves recent conversation turns for context generation."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, username, content, is_bot, timestamp
                FROM message_history
                WHERE channel_id = ?
                ORDER BY id DESC LIMIT ?
            """, (str(channel_id), limit))
            rows = cursor.fetchall()
            history = [dict(r) for r in reversed(rows)]
            return history

    def close(self):
        """Closes memory connection if open."""
        if self._mem_conn:
            try:
                self._mem_conn.close()
            except Exception:
                pass
            self._mem_conn = None


