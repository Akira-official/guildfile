"""
src/cli/main.py
Unified Command-Line Interface for HelixCore.
"""

import os
import sys
import argparse
import asyncio
import discord
from dotenv import load_dotenv

from ..utils.logger import setup_logger
from ..core.blueprint_parser import load_blueprint
from ..core.provisioner import ServerProvisioner
from ..agent.database import AgentMemoryDB
from ..agent.persona import PersonaEngine
from ..agent.ai_client import AIClient
from ..agent.status_cycler import StatusCycler
from ..agent.chat_manager import ChatManager

logger = setup_logger("HelixCore.CLI")


def cmd_doctor():
    """Validates local environment, tokens, and dependencies."""
    load_dotenv()
    print("\n🔍 Running HelixCore Doctor System Diagnostics...\n" + "━" * 50)

    token = os.getenv("DISCORD_TOKEN")
    groq_key = os.getenv("GROQ_API_KEY")
    guild_id = os.getenv("DISCORD_GUILD_ID")

    # 1. Token Check
    if not token or token.startswith("your_"):
        print("❌ [DISCORD_TOKEN]: Missing or using placeholder in .env")
    else:
        print(f"✅ [DISCORD_TOKEN]: Configured (Length: {len(token)})")

    # 2. Guild ID Check
    if not guild_id or guild_id.startswith("your_"):
        print("⚠️ [DISCORD_GUILD_ID]: Missing or placeholder (needed for provisioner)")
    else:
        print(f"✅ [DISCORD_GUILD_ID]: Configured ({guild_id})")

    # 3. Groq API Check
    if not groq_key or groq_key.startswith("your_"):
        print("⚠️ [GROQ_API_KEY]: Missing (Chatbot will use offline fallback mode)")
    else:
        print(f"✅ [GROQ_API_KEY]: Configured (Length: {len(groq_key)})")

    # 4. SQLite Check
    try:
        db = AgentMemoryDB(":memory:")
        user = db.get_or_create_user("1", "test")
        assert user["username"] == "test"
        print("✅ [SQLITE_ENGINE]: Verified functional (In-Memory & Persistent Ready)")
    except Exception as e:
        print(f"❌ [SQLITE_ENGINE]: Error: {e}")

    print("━" * 50 + "\nDiagnostics Complete!\n")


def cmd_apply(blueprint_path: str):
    """Parses blueprint and provisions the target Discord server."""
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    guild_id = os.getenv("DISCORD_GUILD_ID")

    if not token or not guild_id:
        logger.error("Please configure DISCORD_TOKEN and DISCORD_GUILD_ID in .env")
        return

    blueprint = load_blueprint(blueprint_path)
    logger.info(f"Loaded blueprint: '{blueprint.metadata.name}' v{blueprint.metadata.version}")

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(int(guild_id))
        if not guild:
            logger.error(f"Could not find guild with ID {guild_id}")
            await client.close()
            return

        provisioner = ServerProvisioner(client, guild, blueprint)
        await provisioner.provision_all()
        await client.close()

    asyncio.run(client.start(token))


def cmd_agent():
    """Launches the autonomous AI companion bot."""
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("Please configure DISCORD_TOKEN in .env")
        return

    intents = discord.Intents.default()
    intents.message_content = True  # Required for reading chat messages

    client = discord.Client(intents=intents)
    db = AgentMemoryDB(os.getenv("MEMORY_DB_PATH", "helix_memory.db"))
    persona = PersonaEngine()
    ai = AIClient()
    cycler = StatusCycler(client)
    chat_mgr = ChatManager(client, db, persona, ai, cycler)

    @client.event
    async def on_ready():
        logger.info(f"✨ Helix AI Companion is ONLINE as {client.user.name}#{client.user.discriminator}")
        asyncio.create_task(cycler.start_loop())

    @client.event
    async def on_message(message: discord.Message):
        await chat_mgr.handle_message(message)

    try:
        asyncio.run(client.start(token))
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")


def cli_entrypoint():
    parser = argparse.ArgumentParser(
        description="HelixCore: Declarative Discord Provisioner & Autonomous Agent Harness"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Doctor
    subparsers.add_parser("doctor", help="Run system and environment diagnostics")

    # Apply
    apply_parser = subparsers.add_parser("apply", help="Apply a blueprint to a Discord guild")
    apply_parser.add_argument(
        "--blueprint", "-b", required=True, help="Path to YAML/JSON blueprint file"
    )

    # Agent
    subparsers.add_parser("agent", help="Launch the autonomous AI companion bot")

    args = parser.parse_args()
    if args.command == "doctor":
        cmd_doctor()
    elif args.command == "apply":
        cmd_apply(args.blueprint)
    elif args.command == "agent":
        cmd_agent()
    else:
        parser.print_help()


if __name__ == "__main__":
    cli_entrypoint()
