import disnake as discord
from disnake import app_commands
from disnake.ext import commands
import os
import asyncio

client = commands.Bot(command_prefix="fuckofflolgdjgkl,ndjkflgnfhiop", intents=discord.Intents(message_content=True))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("in ben we trust"))
    client.remove_command("help")
    print("hi")

@client.slash_command(name="ping", description="Check if the bot committed unaliving", guild_ids=[748564859226161224])
async def ping(inter):
    await inter.send(f"i'm definitely alive: latency is {round(client.latency * 1000)} ms")

cool_token = os.getenv("TOKEN")

async def main():
    client.load_extensions("./modules/")
    await client.start(cool_token)

asyncio.run(main())