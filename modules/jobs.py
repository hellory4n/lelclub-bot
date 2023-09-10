import disnake as discord
from disnake import Embed
from disnake.ext import commands, tasks
import os
import json
from .economy_basics import EconomyBasics

class Jobs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("job cog loaded")

def setup(client: commands.Bot):
    client.add_cog(Jobs(client))