from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands

import database as db


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bounty(self, ctx):
        await ctx.send(f"Current balance: {db.get_balance(ctx.author)}")

    @commands.command()
    async def worstgeneration(self, ctx):
        top_5: list[tuple[str, int]] = db.get_worst_generation()
        leaderboard = "TOP 5"

        for i, user in enumerate(top_5):
            leaderboard += f"\n{i + 1}. {user[0]}: Balance: {user[1]}"

        await ctx.send(leaderboard)

    @commands.command()
    async def trade(self, ctx, user: discord.Member, amt: int):
        if amt <= 0:
            await ctx.send("Amount must be greater than zero")
            return

        sender_balance = db.get_balance(ctx.author)
        if sender_balance < amt:
            await ctx.send("You don't have enough money!")
            return
        db.update_balance(ctx.author, db.get_balance(ctx.author) - amt)
        db.update_balance(user, db.get_balance(user) + amt)

        await ctx.send(
            f"{ctx.author.mention}({db.get_balance(ctx.author)}) traded {amt} with {user.mention}({db.get_balance(user)})"
        )

    @commands.command()
    async def setsail(self, ctx):
        last_daily_str = db.get_last_daily(ctx.author)
        last_daily = datetime.fromisoformat(last_daily_str) if last_daily_str else None
        current_time = datetime.now(timezone.utc)

        if last_daily is not None:
            difference = current_time - last_daily
            if difference < timedelta(days=1):
                await ctx.send("Wait 24 hours between daily claims!")
                return

        db.set_last_daily(ctx.author, current_time.isoformat())
        db.update_balance(ctx.author, db.get_balance(ctx.author) + 50)
        await ctx.send("You claimed your daily 50 berries!")


async def setup(bot):
    await bot.add_cog(Economy(bot))
