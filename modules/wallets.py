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
    
    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount, wallet):
        EconomyBasics.setup_user(ctx.author.id)

        pain = {}
        with open(f"data/money/{ctx.author.id}.json", "r") as f:
            pain = json.load(f)
        
        # find wallet
        if not wallet in pain["wallets"]:
            embed = Embed(title="Error", description=f"Wallet `{wallet}` not found. (If the name has spaces then put it in quotes, example: `l.deposit 69 \"cool wallet\"`)", 
                            color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            try:
                # so you can use l.dep all "cool wallet"
                deposit = 0
                if amount == "all":
                    deposit = pain["money"]
                else:
                    deposit = float(amount)

                if pain["money"] >= deposit:
                    pain["money"] -= deposit
                    pain["wallets"][wallet] += deposit

                    with open(f"data/money/{ctx.author.id}.json", "w") as f:
                        json.dump(pain, f)
                    
                    embed = Embed(description=f"Successfully deposited B$ {deposit:,.2f} to {wallet}", 
                                    color=discord.Color(0x3eba49))
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)                        
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(title="Error", description=f"You only have {pain['money']:,.2f} in cash!", 
                                    color=discord.Color(0xff4865))
                    await ctx.send(embed=embed)
            except:
                embed = Embed(title="Error", description="Are you sure the arguments are numbers?", 
                                color=discord.Color(0xff4865))
                await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(Wallets(client))