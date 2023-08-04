import disnake as discord
from disnake import Embed
from disnake.ext import commands
import os
import json
from .economy_basics import EconomyBasics

class Wallets(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("wallet cog loaded")

    @commands.command(aliases=["create-wallet", "add-wallet", "add_wallet"])
    async def create_wallet(self, ctx, *, name):
        EconomyBasics.setup_user(ctx.author.id)

        with open(f"data/money/{ctx.author.id}.json", "r+") as f:
            pain = json.load(f)
            pain["wallets"].update({name: 0.00})
            f.seek(0)
            f.write(json.dumps(pain))
            f.truncate()

        embed = Embed(description=f"Successfully created wallet `{name}`",
                      color=discord.Color(0x3eba49))
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(Wallets(client))