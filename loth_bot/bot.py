from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta

import discord

from . import constants
from . import controller
from . import tasks
from .models import Hour
from .models import Requirement

bot = discord.Bot()


def _add_timedelta(time: time, timedelta: timedelta) -> time:
    return (datetime.combine(date.min, time) + timedelta).time()


def _schedule_warning_tasks(bot: discord.Bot) -> None:
    matins_and_lauds_warning = tasks.get_warn_requirements_callback(
        (Requirement.MATINS, Requirement.LAUDS), constants.MATINS_AND_LAUDS_DEADLINE
    )
    daytime_warning = tasks.get_warn_requirements_callback(
        (Requirement.DAYTIME,), constants.DAYTIME_DEADLINE
    )
    vespers_warning = tasks.get_warn_requirements_callback(
        (Requirement.VESPERS,), constants.VESPERS_DEADLINE
    )
    compline_warning = tasks.get_warn_requirements_callback(
        (Requirement.COMPLINE,), constants.COMPLINE_DEADLINE
    )
    warning_tasks = [
        tasks.schedule_daily(
            bot,
            matins_and_lauds_warning,
            _add_timedelta(
                constants.MATINS_AND_LAUDS_DEADLINE, constants.REMINDER_TIMEDELTA
            ),
        ),
        tasks.schedule_daily(
            bot,
            daytime_warning,
            _add_timedelta(constants.DAYTIME_DEADLINE, constants.REMINDER_TIMEDELTA),
        ),
        tasks.schedule_daily(
            bot,
            vespers_warning,
            _add_timedelta(constants.VESPERS_DEADLINE, constants.REMINDER_TIMEDELTA),
        ),
        tasks.schedule_daily(
            bot,
            compline_warning,
            _add_timedelta(constants.COMPLINE_DEADLINE, constants.REMINDER_TIMEDELTA),
        ),
    ]
    for task in warning_tasks:
        bot.loop.create_task(task)


def _schedule_check_tasks(bot: discord.Bot) -> None:
    matins_and_lauds = tasks.get_check_requirements_callback(
        (Requirement.MATINS, Requirement.LAUDS)
    )
    daytime = tasks.get_check_requirements_callback((Requirement.DAYTIME,))
    vespers = tasks.get_check_requirements_callback((Requirement.VESPERS,))
    compline = tasks.get_check_requirements_callback((Requirement.COMPLINE,))
    check_tasks = [
        tasks.schedule_daily(
            bot,
            matins_and_lauds,
            constants.MATINS_AND_LAUDS_DEADLINE,
        ),
        tasks.schedule_daily(bot, daytime, constants.DAYTIME_DEADLINE),
        tasks.schedule_daily(bot, vespers, constants.VESPERS_DEADLINE),
        tasks.schedule_daily(bot, compline, constants.COMPLINE_DEADLINE),
    ]
    for task in check_tasks:
        bot.loop.create_task(task)


@bot.event
async def on_ready():
    _schedule_warning_tasks(bot)
    _schedule_check_tasks(bot)
    bot.loop.create_task(tasks.schedule_daily(bot, tasks.reset_prayed, time(0, 0)))
    print(f"{bot.user} started.")


@bot.slash_command(name="pray", description="Pray one of the hours")
async def pray(
    ctx: discord.ApplicationContext,
    hour: str = discord.Option(choices=[hour.title() for hour in Hour]),
):
    controller.pray_hour(Hour(hour))
    await ctx.respond(f"Deo Gratias - {hour.title()} prayed", ephemeral=True)


missed = bot.create_group(
    "missed", description="See and reset the number of missed hours"
)


@missed.command(description="See the number of missed hours")
async def count(ctx: discord.ApplicationContext):
    missed_hours = controller.get_hours_missed()
    await ctx.respond(
        f"{missed_hours} missed hour{'' if missed_hours == 1 else 's'}", ephemeral=True
    )


@missed.command(description="Reset the number of missed hours")
async def reset(ctx: discord.ApplicationContext):
    controller.reset_missed_hours()
    await ctx.respond("Missed hours reset!")


@bot.slash_command(name="help", description="Show available commands")
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="LoTHBot Commands",
        color=discord.Color.blurple(),
    )

    for command in bot.commands:
        embed.add_field(
            name=f"/{command.name}",
            value=getattr(command, "description", ""),
            inline=False,
        )

    await ctx.respond(embed=embed, ephemeral=True)
