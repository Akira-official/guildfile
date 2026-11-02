"""
tests/test_persona_engine.py
Unit tests for persona, mood calculation, and language detection.
"""

from src.agent.persona import PersonaEngine


def test_language_detection():
    persona = PersonaEngine()
    assert persona.detect_language_flavor("are bhai kya chal raha hai?") == "hinglish"
    assert persona.detect_language_flavor("hey bro, what is the server status?") == "english"


def test_extract_banned_topics():
    persona = PersonaEngine()
    history = [
        {"content": "your code crashes harder than my coffee", "is_bot": True},
        {"content": "wake up sleepyhead", "is_bot": True}
    ]
    banned = persona.extract_banned_topics(history)
    assert "coffee" in banned
    assert "sleepyhead" in banned

