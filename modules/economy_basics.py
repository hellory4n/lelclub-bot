import disnake as discord
from disnake import Embed
from disnake.ext import commands
import os
import json

class EconomyBasics(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("economy basics cog loaded")

    def setup_user(self, user_id: int):
        """Creates the files necessary for a user to function in the economy if they don't exist"""

        user = str(user_id)

        if not os.path.exists(f"data/money/{user}.json"):
            init = {"money": 0}
            with open(f"data/money/{user}.json", "w+") as json_file:
                json.dump(init, json_file)
    
    @commands.command(aliases=["bal", "money"])
    async def balance(self, ctx, user: discord.User = None):
        """
        Parameters
        ----------
        user: Who to check the balance
        """
        if user == None:
            user = ctx.author
        self.setup_user(user.id)

        moneys = 0
        with open(f"data/money/{user.id}.json", "r") as f:
            moneys = json.load(f)["money"]
        
        embed = Embed(title="Balance", description=f"{user.mention} has B$ {moneys:,}")
        await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(EconomyBasics(client))