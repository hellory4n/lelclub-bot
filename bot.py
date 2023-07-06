import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# cog stuff :)
initial_extensions = ['modules.election']
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_ready():
    await client.tree.sync()
    print("m")

@client.tree.command(name="ping", description="Check if the bot committed unaliving")
async def ping(inter):
    await inter.response.send_message("i'm definitely alive :)")

@client.command(name="sync", description="Owner only")
async def sync(ctx: commands.Context):
    if ctx.author.id == 748560377763201185:
        print("hi :)")
        await client.tree.sync()
        await ctx.send("there you go")
    else:
        await ctx.send("you're not the bot owner lol")

client.run(os.environ["TOKEN"])