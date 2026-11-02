"""
src/core/provisioner.py
Asynchronous provisioning engine that applies a BlueprintSchema to a Discord Guild.
"""

import asyncio
import discord
from typing import Dict, Optional
from ..utils.logger import setup_logger
from .blueprint_parser import BlueprintSchema, RoleSchema, CategorySchema, ChannelSchema

logger = setup_logger("HelixCore.Provisioner")


class ServerProvisioner:
    """Idempotent Discord server provisioning and synchronization engine."""

    def __init__(self, client: discord.Client, guild: discord.Guild, blueprint: BlueprintSchema):
        self.client = client
        self.guild = guild
        self.blueprint = blueprint
        self.role_cache: Dict[str, discord.Role] = {}

    def hex_to_colour(self, hex_code: Optional[str]) -> discord.Colour:
        """Converts a hex string like #3498DB to discord.Colour."""
        if not hex_code:
            return discord.Colour.default()
        clean = hex_code.lstrip("#")
        try:
            return discord.Colour(int(clean, 16))
        except ValueError:
            return discord.Colour.default()

    async def sync_roles(self):
        """Creates or updates roles defined in the blueprint in reverse order."""
        logger.info(f"[*] Synchronizing {len(self.blueprint.roles)} roles...")
        existing_roles = {r.name: r for r in self.guild.roles}

        for r_spec in self.blueprint.roles:
            color = self.hex_to_colour(r_spec.color)
            perms = discord.Permissions()
            for perm_name, perm_val in r_spec.permissions.items():
                if hasattr(perms, perm_name):
                    setattr(perms, perm_name, perm_val)

            if r_spec.name in existing_roles:
                role = existing_roles[r_spec.name]
                try:
                    await role.edit(
                        colour=color,
                        hoist=r_spec.hoist,
                        mentionable=r_spec.mentionable,
                        permissions=perms,
                        reason="HelixCore Blueprint Sync"
                    )
                    logger.info(f"  [=] Updated existing role: {role.name}")
                except discord.Forbidden:
                    logger.warning(f"  [!] Lacking permission to edit role: {role.name}")
            else:
                try:
                    role = await self.guild.create_role(
                        name=r_spec.name,
                        colour=color,
                        hoist=r_spec.hoist,
                        mentionable=r_spec.mentionable,
                        permissions=perms,
                        reason="HelixCore Blueprint Provisioning"
                    )
                    logger.info(f"  [+] Created new role: {role.name}")
                except Exception as e:
                    logger.error(f"  [!] Failed to create role {r_spec.name}: {e}")
                    continue

            self.role_cache[role.name] = role

        # Refresh full cache
        for r in self.guild.roles:
            self.role_cache[r.name] = r

    async def harden_everyone_baseline(self):
        """Disables dangerous permissions on @everyone."""
        logger.info("[*] Hardening @everyone baseline permissions...")
        everyone = self.guild.default_role
        perms = everyone.permissions
        perms.mention_everyone = False
        perms.create_instant_invite = False
        perms.create_events = False
        perms.create_expressions = False
        perms.manage_channels = False
        perms.manage_roles = False
        perms.manage_guild = False
        try:
            await everyone.edit(permissions=perms, reason="HelixCore Security Hardening")
            logger.info("  [+] @everyone permissions secured.")
        except Exception as e:
            logger.warning(f"  [!] Could not edit @everyone: {e}")

    async def sync_categories_and_channels(self):
        """Creates categories and channels with isolated permissions."""
        logger.info(f"[*] Synchronizing {len(self.blueprint.categories)} categories...")

        for pos, cat_spec in enumerate(self.blueprint.categories):
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(
                    view_channel=not cat_spec.private,
                    send_messages=not cat_spec.private
                )
            }

            if cat_spec.private:
                for r_name in cat_spec.allowed_roles:
                    if r_name in self.role_cache:
                        overwrites[self.role_cache[r_name]] = discord.PermissionOverwrite(
                            view_channel=True,
                            send_messages=True,
                            read_message_history=True
                        )

            # Find or create category
            category = discord.utils.get(self.guild.categories, name=cat_spec.name)
            if not category:
                category = await self.guild.create_category(
                    name=cat_spec.name,
                    overwrites=overwrites,
                    position=pos,
                    reason="HelixCore Blueprint Provisioning"
                )
                logger.info(f"  [+] Created category: {category.name}")
            else:
                await category.edit(overwrites=overwrites, position=pos)
                logger.info(f"  [=] Synchronized category: {category.name}")

            # Sync channels inside category
            for ch_pos, ch_spec in enumerate(cat_spec.channels):
                await self._sync_channel(category, ch_spec, ch_pos)

    async def _sync_channel(self, category: discord.CategoryChannel, ch_spec: ChannelSchema, pos: int):
        """Helper to create or update a single channel."""
        ch_overwrites = dict(category.overwrites)
        if ch_spec.read_only:
            ch_overwrites[self.guild.default_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                add_reactions=True
            )

        existing = discord.utils.get(category.channels, name=ch_spec.name)
        if existing:
            await existing.edit(
                topic=ch_spec.topic,
                slowmode_delay=ch_spec.slowmode,
                position=pos,
                overwrites=ch_overwrites
            )
            logger.info(f"    [=] Channel up to date: #{existing.name}")
            return

        try:
            if ch_spec.type == "voice":
                await self.guild.create_voice_channel(
                    name=ch_spec.name,
                    category=category,
                    user_limit=ch_spec.user_limit or 0,
                    position=pos,
                    overwrites=ch_overwrites,
                    reason="HelixCore Blueprint Channel"
                )
            elif ch_spec.type == "forum":
                await self.guild.create_forum(
                    name=ch_spec.name,
                    category=category,
                    topic=ch_spec.topic,
                    position=pos,
                    overwrites=ch_overwrites,
                    reason="HelixCore Blueprint Forum"
                )
            else:
                await self.guild.create_text_channel(
                    name=ch_spec.name,
                    category=category,
                    topic=ch_spec.topic,
                    slowmode_delay=ch_spec.slowmode,
                    position=pos,
                    overwrites=ch_overwrites,
                    reason="HelixCore Blueprint TextChannel"
                )
            logger.info(f"    [+] Created #{ch_spec.name} ({ch_spec.type})")
        except Exception as e:
            logger.error(f"    [!] Failed to create channel #{ch_spec.name}: {e}")

    async def provision_all(self):
        """Executes the complete server provisioning pipeline."""
        logger.info(f"\n🚀 Starting full provisioning for '{self.guild.name}'...")
        await self.sync_roles()
        await self.harden_everyone_baseline()
        await self.sync_categories_and_channels()
        logger.info("\n🎉 Server provisioning finished successfully!\n")
