import discord

from . import controller
from .models import Hour

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} started.")


@bot.slash_command(name="pray", description="Pray one of the hours")
async def pray(
    ctx: discord.ApplicationContext,
    hour: str = discord.Option(choices=[hour.value for hour in Hour]),
):
    controller.pray_hour(Hour(hour))
    await ctx.respond(f"Deo Gratias - {hour} prayed", ephemeral=True)


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
