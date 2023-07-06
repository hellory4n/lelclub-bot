import discord
from discord import app_commands
import os

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print("m")

@tree.command(name="ping", description="Check if the bot committed unaliving")
async def ping(inter):
    await inter.response.send_message("i'm definitely alive :)")

client.run(os.environ["TOKEN"])