import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import database as db

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")


async def main():
    db.init_db()
    async with bot:
        await bot.load_extension("cogs.economy")
        await bot.load_extension("cogs.fun")
        await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
