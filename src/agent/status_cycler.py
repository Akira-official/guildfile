"""
src/agent/status_cycler.py
Dynamic Discord activity and presence cycler.
"""

import random
import asyncio
import discord
from ..utils.logger import setup_logger

logger = setup_logger("HelixCore.StatusCycler")


class StatusCycler:
    """Rotates realistic Discord activity states in the background."""

    ACTIVITIES = [
        {"type": discord.ActivityType.playing, "name": "Minecraft (mining diamonds 💎)"},
        {"type": discord.ActivityType.playing, "name": "VALORANT (bottom fragging 💀)"},
        {"type": discord.ActivityType.listening, "name": "Spotify - 3hr video essay"},
        {"type": discord.ActivityType.watching, "name": "people take Ls in 4K"},
        {"type": discord.ActivityType.playing, "name": "with the production database"}
    ]

    def __init__(self, client: discord.Client):
        self.client = client
        self.current_activity_name = "vibing in general"

    async def start_loop(self, interval_seconds: int = 420):
        """Periodically updates the bot presence."""
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            item = random.choice(self.ACTIVITIES)
            self.current_activity_name = item["name"]
            activity = discord.Activity(type=item["type"], name=item["name"])
            try:
                await self.client.change_presence(status=discord.Status.online, activity=activity)
                logger.debug(f"Presence updated: {item['name']}")
            except Exception as e:
                logger.warning(f"Could not change presence: {e}")
            await asyncio.sleep(interval_seconds)
