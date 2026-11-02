"""
src/agent/chat_manager.py
Orchestrates autonomous chat handling, multi-message bursts, typing simulation, and reactions.
"""

import asyncio
import random
import discord
from typing import List
from ..utils.logger import setup_logger
from .database import AgentMemoryDB
from .persona import PersonaEngine
from .ai_client import AIClient
from .status_cycler import StatusCycler

logger = setup_logger("HelixCore.ChatManager")


class ChatManager:
    """Core conversational manager simulating realistic human behavior on Discord."""

    REACTIONS = ["💀", "👀", "🤡", "💅", "🔥", "😭"]

    def __init__(self, client: discord.Client, db: AgentMemoryDB, persona: PersonaEngine, ai: AIClient, cycler: StatusCycler):
        self.client = client
        self.db = db
        self.persona = persona
        self.ai = ai
        self.cycler = cycler
        self.is_processing = False

    async def handle_message(self, message: discord.Message):
        """Processes an incoming chat message with human-like latency and decisions."""
        if message.author == self.client.user or message.author.bot:
            return

        # 1. Update Social Graph
        user_data = self.db.get_or_create_user(str(message.author.id), message.author.name)
        self.db.record_interaction(
            user_id=str(message.author.id),
            username=message.author.name,
            content=message.content,
            is_bot=False,
            channel_id=str(message.channel.id)
        )

        # 2. Check if bot should engage (Direct Mention, keyword 'helix', or active channel)
        is_mentioned = self.client.user in message.mentions or "helix" in message.content.lower()
        is_active_channel = "general-chat" in message.channel.name

        if not is_mentioned and not is_active_channel:
            return

        # 3. Silent Reaction Chance (15% chance to just react with an emoji and stay silent)
        if not is_mentioned and random.random() < 0.15:
            reaction = random.choice(self.REACTIONS)
            try:
                await message.add_reaction(reaction)
                logger.info(f"Silently reacted {reaction} to {message.author.name}")
            except Exception:
                pass
            return

        if self.is_processing:
            return

        self.is_processing = True
        try:
            # 4. Check for attached image/meme vision
            if message.attachments and message.attachments[0].content_type and "image" in message.attachments[0].content_type:
                logger.info(f"Image attached by {message.author.name}. Inspecting with vision...")
                async with message.channel.typing():
                    roast = self.ai.analyze_image_and_roast(message.attachments[0].url, message.content)
                    if roast:
                        await asyncio.sleep(random.uniform(1.0, 2.0))
                        await message.reply(roast)
                        return

            # 5. Build Context & Generate Text
            author_roles = [r.name for r in getattr(message.author, "roles", []) if r.name != "@everyone"]
            recent_turns = self.db.get_recent_history(str(message.channel.id), limit=10)
            lang = self.persona.detect_language_flavor(message.content)

            system_prompt = self.persona.build_system_prompt(
                user_data=user_data,
                author_roles=author_roles,
                recent_history=recent_turns,
                current_status=self.cycler.current_activity_name,
                detected_lang=lang
            )

            llm_messages = []
            for t in recent_turns:
                role = "assistant" if t["is_bot"] else "user"
                llm_messages.append({"role": role, "content": f"{t['username']}: {t['content']}"})

            reply_text = self.ai.generate_chat_reply(system_prompt, llm_messages)
            if not reply_text:
                return

            # 6. Multi-Message Burst Execution
            bursts = self._split_into_bursts(reply_text)
            for i, part in enumerate(bursts):
                async with message.channel.typing():
                    # Natural human typing delay based on word count
                    delay = max(0.8, min(2.5, len(part.split()) * 0.25))
                    await asyncio.sleep(delay)

                if i == 0:
                    sent = await message.reply(part)
                else:
                    sent = await message.channel.send(part)

                self.db.record_interaction(
                    user_id=str(self.client.user.id),
                    username=self.client.user.name,
                    content=part,
                    is_bot=True,
                    channel_id=str(message.channel.id)
                )

        finally:
            self.is_processing = False

    def _split_into_bursts(self, text: str) -> List[str]:
        """Splits sentences into 1-2 rapid-fire mini-messages."""
        if len(text.split()) < 10 or "?" not in text and "!" not in text and "\n" not in text:
            return [text]

        # Split on newline or question mark
        parts = [p.strip() for p in text.replace("?", "?\n").replace("!", "!\n").split("\n") if p.strip()]
        if len(parts) >= 2:
            return parts[:2]
        return [text]
