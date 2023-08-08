import disnake as discord
from disnake.ext import commands, tasks
import os
import asyncio
import json
import random
import dotenv

dotenv.load_dotenv(".env")

epic_cool_intents = discord.Intents.default()
epic_cool_intents.message_content = True
client = commands.Bot(command_prefix=commands.when_mentioned_or("l-"), intents=epic_cool_intents)
client.remove_command("help")

@client.event
async def on_ready():
    await suffering.start()
    print("hi")

# top tier error handling
@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Error", description=f"`{error}`\n\nFeel free to ping <@748560377763201185> when seeing errors like this, we need to help the bot be more stable for the good of lelclub <:lelflag:1136802749347020870> <:lelflag:1136802749347020870>", color=discord.Color(0xff4865))
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f"i'm definitely alive")

@client.command()
async def help(ctx):
    cool_embed = discord.Embed(
        title="Cool lelclub bot™",
        description="`l.ping`: yeah\n`l.help`: this command\n`l.nominate`: become a candidate\n`l.dismiss`: stop being a candidate\n`l.vote`: vote omgogmogmg"
    )
    await ctx.send(embed=cool_embed)

cool_token = os.getenv("TOKEN")
version = os.getenv("VERSION")

# it's a loop :)
@tasks.loop(seconds = 30)
async def suffering():
    pain = [
        "Wii Are Resorting to Violence",
        "Mining & Crafting",
        "UnderCroch",
        "Overlook",
        "Galaxy Citizen",
        "Power Distance 5",
        "Pablo",
        "Squilliam Fancyson",
        "MOMAZOS DIEGO ADVENTURE 2",
        "Funcade",
        "Funcade Adventures"
    ]
    await client.change_presence(activity=discord.Game(f"{random.choice(pain)} on Is Tim"))

client.load_extensions("./modules/")
client.run(cool_token)