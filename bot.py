import discord
import os

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print("sucky")

client.run(os.environ["TOKEN"])