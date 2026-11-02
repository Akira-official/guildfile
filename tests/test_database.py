"""
tests/test_database.py
Unit tests for SQLite Social Graph and message memory.
"""

import os
import pytest
from src.agent.database import AgentMemoryDB


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_memory.db"
    db = AgentMemoryDB(str(db_file))
    return db


def test_create_and_get_user(temp_db):
    user = temp_db.get_or_create_user("12345", "testuser")
    assert user["user_id"] == "12345"
    assert user["username"] == "testuser"
    assert user["closeness"] == 10


def test_record_interaction_and_history(temp_db):
    temp_db.record_interaction("12345", "testuser", "hello world", is_bot=False, channel_id="999")
    temp_db.record_interaction("bot_id", "Helix", "sup bro", is_bot=True, channel_id="999")

    history = temp_db.get_recent_history("999", limit=5)
    assert len(history) == 2
    assert history[0]["content"] == "hello world"
    assert history[1]["content"] == "sup bro"
