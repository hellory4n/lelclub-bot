import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("in ben we trust"))
    await client.remove_command("help")
    print("hi")

@client.tree.command(name="ping", description="Check if the bot committed unaliving")
async def ping(inter):
    await inter.response.send_message(f"i'm definitely alive: latency is {round(client.latency * 1000)} ms")

@client.command(name="sync", description="Owner only")
async def sync(ctx: commands.Context):
    if ctx.author.id == 748560377763201185:
        await client.tree.sync()
        await ctx.send("there you go")
    else:
        await ctx.send("you're not the bot owner lol")

cool_token = os.environ["TOKEN"]

async def main():
    async with client:
        await client.load_extension("modules.election")
        await client.start(cool_token)
        await client.tree.sync()

asyncio.run(main())