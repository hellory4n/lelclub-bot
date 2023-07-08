import discord
from discord import app_commands
from discord.ext import commands

class Election(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("this sucks tbh")

    @app_commands.command(name="start-election", description="Start an election, wowser")
    async def start_election(self, inter: discord.Interaction):
        await inter.response.send_message("my life be like ooooo aaaaa ooooo")

async def setup(client: commands.Bot):
    await client.add_cog(Election(client))