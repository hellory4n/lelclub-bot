import disnake as discord
from disnake.ext import commands

class EconomyBasics(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("economy basics cog loaded")

def setup(client: commands.Bot):
    client.add_cog(EconomyBasics(client))