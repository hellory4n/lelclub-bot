import discord
from discord import app_commands
from discord.ext import commands

class Election(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("this sucks tbh")

    @app_commands.command(name="start-election", description="Start an election, wowser")
    async def start_election(self, inter: discord.Interaction) -> None:
        await inter.response.send_message("my life be like oooo aaaa oooo")

def setup(bot: commands.Bot):
    bot.add_cog(Election(bot))