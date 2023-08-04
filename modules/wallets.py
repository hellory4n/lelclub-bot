import disnake as discord
from disnake import Embed, Button, ButtonStyle
from discord.ui import View
from disnake.ext import commands
import json
from .economy_basics import EconomyBasics
import asyncio

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
    


    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount, wallet):
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
                withdraw = 0
                if amount == "all":
                    withdraw = pain["wallets"][wallet]
                else:
                    withdraw = float(amount)

                if pain["wallets"][wallet] >= withdraw:
                    pain["money"] += withdraw
                    pain["wallets"][wallet] -= withdraw

                    with open(f"data/money/{ctx.author.id}.json", "w") as f:
                        json.dump(pain, f)
                    
                    embed = Embed(description=f"Successfully withdrawn B$ {withdraw:,.2f} from {wallet}", 
                                    color=discord.Color(0x3eba49))
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)                        
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(title="Error", description=f"You only have {pain['wallet'][wallet]:,.2f} in {pain[wallet]}!", 
                                    color=discord.Color(0xff4865))
                    await ctx.send(embed=embed)
            except:
                embed = Embed(title="Error", description="Are you sure the arguments are numbers?", 
                                color=discord.Color(0xff4865))
                await ctx.send(embed=embed)
    



    @commands.command(aliases=["remove-wallet", "delete-wallet", "remove_wallet"])
    async def delete_wallet(self, ctx, *, wallet):
        EconomyBasics.setup_user(ctx.author.id)

        pain = {}
        with open(f"data/money/{ctx.author.id}.json", "r") as f:
            pain = json.load(f)
        
        # find wallet
        if not wallet in pain["wallets"]:
            embed = Embed(title="Error", description=f"Wallet `{wallet}` not found.", 
                            color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            # we need to ask the user to confirm cuz yes
            embed = Embed(description=f"Are you sure you want to delete {wallet}? **BS {pain['wallets'][wallet]:,.2f}** will be permanently lost!\n\nSend \"y\" to confirm.",
                          color=discord.Color(0xff4865))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            yes = await ctx.send(embed=embed)

            def check(message):
                return message.author == ctx.author and str(message.content) == "y"

            try:
                reply = await self.client.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await yes.edit(content="Operation cancelled.", embed=None)
            else:
                del pain["wallets"][wallet]
                with open(f"data/money/{ctx.author.id}.json", "w") as f:
                    json.dump(pain, f)

                await ctx.send(f"{wallet} is now gone.")
            

def setup(client: commands.Bot):
    client.add_cog(Wallets(client))