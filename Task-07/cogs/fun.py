import random
from datetime import datetime, timedelta, timezone

import aiohttp
import discord
from discord.ext import commands

import database as db


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duel(self, ctx, choice: str):
        if db.get_balance(ctx.author) < 10:
            await ctx.send("You need at least 10 berries to duel!")
            return

        user_choice = choice.lower()
        choices = ["rock", "paper", "scissors"]
        if user_choice not in choices:
            await ctx.send(f"{user_choice} is not a valid choice!")
            return

        async def tied():
            await ctx.send("The bot also picked the same!")

        async def win(user, user_choice, bot_choice):
            await ctx.send(f"{user_choice} beats {bot_choice}! You win 10 berries!")
            db.update_balance(user, db.get_balance(user) + 10)

        async def lose(user, user_choice, bot_choice):
            await ctx.send(f"{user_choice} loses to {bot_choice}! You lose 10 berries!")
            db.update_balance(user, db.get_balance(user) - 10)

        bot_choice = random.choice(choices)
        match bot_choice:
            case "rock":
                match user_choice:
                    case "rock":
                        await tied()
                    case "paper":
                        await win(ctx.author, "paper", "rock")
                    case "scissors":
                        await lose(ctx.author, "scissors", "rock")
            case "paper":
                match user_choice:
                    case "rock":
                        await lose(ctx.author, user_choice, "rock")
                    case "paper":
                        await tied()
                    case "scissors":
                        await win(ctx.author, user_choice, "rock")
            case "scissors":
                match user_choice:
                    case "rock":
                        await win(ctx.author, user_choice, "rock")
                    case "paper":
                        await lose(ctx.author, user_choice, "rock")
                    case "scissors":
                        await tied()

    @commands.command()
    async def roast(self, ctx, target: discord.Member):
        INSULTS = [
            "{user}, even yer shadow looks disappointed in ye.",
            "By the seven seas, {user}, how are ye this useless with both hands?",
            "Ye call yerself a pirate, {user}? I’ve seen seagulls conduct better raids.",
            "{user}, ye’ve got the charisma of a wet rope.",
            "Oi, {user}! The crew voted, and somehow the parrot outranks ye.",
            "{user}, even the Kraken took one look at ye and said, ‘I’m not eating that.’",
            "By Neptune’s beard, {user}, I’ve seen barnacles with better social skills.",
            "{user}, if stupidity were doubloons, ye’d own Tortuga.",
            "Arrr, {user}! Ye’re the reason pirates invented the phrase ‘man overboard.’",
            "Arrr, {user}, ye’re not a pirate. Ye’re a passenger who got lost on the way to the ferry.",
        ]

        insult = random.choice(INSULTS)
        await ctx.send(insult.format(user=target.mention))

    @commands.command()
    async def raid(self, ctx, target: discord.Member):
        last_rob_str = db.get_last_rob(ctx.author)
        last_rob = datetime.fromisoformat(last_rob_str) if last_rob_str else None
        current_time = datetime.now(timezone.utc)
        if last_rob is not None:
            difference = current_time - last_rob
            if difference < timedelta(days=1):
                await ctx.send("Wait 24 hours between raids!")
                return
        db.set_last_rob(ctx.author, current_time.isoformat())

        base_chance = 0.3
        currency_factor = base_chance + 0.05 * db.get_balance(ctx.author)

        chance = random.random()
        if chance > currency_factor:
            target_balance = db.get_balance(target)
            robbed = int(chance * target_balance)
            db.update_balance(ctx.author, db.get_balance(ctx.author) + robbed)
            db.update_balance(target, target_balance - robbed)
            await ctx.send(
                f"Raid {target.mention} successful! Raided {chance * target_balance} berries"
            )

    @commands.command()
    async def logpose(self, ctx):
        APIS = [
            "https://api.api-onepiece.com/v2/fruits/en",
            "https://api.api-onepiece.com/v2/sagas/en",
            "https://api.api-onepiece.com/v2/crews/en",
        ]

        async with aiohttp.ClientSession() as session:
            response = await session.get(random.choice(APIS))
            data = await response.json()

        item = random.choice(data).items()
        item = list(item)[1:]

        output = "Random Trivia:"
        for key, value in item:
            output += f"\n{key}: {value}"

        await ctx.send(output)


async def setup(bot):
    await bot.add_cog(Fun(bot))
