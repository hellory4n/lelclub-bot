import disnake as discord
from disnake import app_commands
from disnake.ext import commands
import os
import asyncio
import json

epic_cool_intents = discord.Intents.default()
epic_cool_intents.message_content = True
client = commands.Bot(command_prefix=commands.when_mentioned_or("l."), intents=epic_cool_intents)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("in ben we trust"))
    print("hi")

@client.command()
async def ping(ctx):
    await ctx.send(f"i'm definitely alive: latency is {round(client.latency * 1000)} ms")

@client.command()
async def help(ctx):
    cool_embed = discord.Embed(
        title="Cool lelclub bot™",
        description="`l.ping`: yeah\n`l.help`: this command\n`l.nominate`: become a candidate\n`l.dismiss`: stop being a candidate\n`l.vote`: vote omgogmogmg"
    )
    await ctx.send(embed=cool_embed)

cool_token = os.getenv("TOKEN")

async def main():
    # create cool election data
    if not os.path.exists("/data/"):
        os.makedirs("/data/")
    
    if not os.path.exists("/data/election.json"):
        init = {"started": False, "candidates": {}, "votes": {}}
        with open("/data/election.json", "w") as json_file:
            json.dump(init, json_file)

    # now we actually run the bot
    client.load_extensions("./modules/")
    await client.start(cool_token)

asyncio.run(main())