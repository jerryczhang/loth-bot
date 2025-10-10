import asyncio
import datetime
from typing import Awaitable
from typing import Callable
from typing import Iterable
from typing import Sequence
from zoneinfo import ZoneInfo

import discord

from . import controller
from .models import Requirement


async def _wait_until(
    target_time: datetime.time,
    tzinfo: ZoneInfo = ZoneInfo("US/Pacific"),
) -> None:
    """Wait until the next occurrence of the given time (defaults to Pacific Time)"""
    now = datetime.datetime.now(tzinfo)
    next_run = datetime.datetime.combine(now.date(), target_time, tzinfo)
    if now > next_run:
        next_run += datetime.timedelta(days=1)
    wait_seconds = (next_run - now).total_seconds()
    await asyncio.sleep(wait_seconds)


def _join_english(items: Sequence) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return str(items[0])
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


async def schedule_daily(
    bot: discord.Bot,
    callback: Callable[[discord.Bot], Awaitable[None]],
    time: datetime.time,
    *,
    tzinfo: ZoneInfo = ZoneInfo("US/Pacific"),
) -> None:
    """Run a callback every day at a specific time."""
    await bot.wait_until_ready()

    while not bot.is_closed():
        await _wait_until(time, tzinfo)
        await callback(bot)


def get_check_requirements_callback(
    requirements: Iterable[Requirement],
) -> Callable[[discord.Bot], Awaitable[None]]:
    async def callback(bot: discord.Bot) -> None:
        missed_requirements = controller.check_requirements(requirements)
        if not missed_requirements:
            return
        guilds = bot.guilds
        for guild in guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(
                        f"@everyone {_join_english([r.title() for r in missed_requirements])} missed! Current total missed hours: {controller.get_hours_missed()}"
                    )
                except discord.errors.Forbidden:
                    continue

    return callback


def get_warn_requirements_callback(
    requirements: Iterable[Requirement], due_time: datetime.time
) -> Callable[[discord.Bot], Awaitable[None]]:
    async def callback(bot: discord.Bot) -> None:
        missed_requirements = controller.check_requirements(
            requirements, increment_missed=False
        )
        if not missed_requirements:
            return
        guilds = bot.guilds
        for guild in guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(
                        f"@everyone Warning: {_join_english([r.title() for r in missed_requirements])} pray by {due_time.strftime('%I:%M %p')}"
                    )
                except discord.errors.Forbidden:
                    continue

    return callback


async def reset_prayed(_: discord.Bot) -> None:
    controller.reset_prayed()
