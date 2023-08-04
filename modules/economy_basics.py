import disnake as discord
from disnake import Embed
from disnake.ext import commands
import os
import json
import random

class EconomyBasics(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("economy basics cog loaded")

    @staticmethod
    def setup_user(user_id: int):
        """Creates the files necessary for a user to function in the economy if they don't exist"""

        user = str(user_id)

        if not os.path.exists(f"data/money/{user}.json"):
            init = {"money": 0.00, "wallets": {}}
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

        yes = {}
        with open(f"data/money/{user.id}.json", "r") as f:
            yes = json.load(f)

        embed = Embed(color=discord.Color(0x008cff))
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        embed.description = f"**Cash**: B$ {yes['money']:,.2f}\n"

        # now get the cool wallets
        total = yes["money"]
        thej = ""
        for name, value in yes["wallets"].items():
            thej += f"**{name}**: B$ {value:,.2f}\n"
            total += value
        
        embed.description += f"{thej}**Total**: B$ {total:,.2f}"

        await ctx.send(embed=embed)



    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def work(self, ctx):
        self.setup_user(ctx.author.id)

        # get work payout
        min = 0
        max = 0
        with open(f"data/economic_policies.json", "r") as f:
            m = json.load(f)
            min = m["work_min"]
            max = m["work_max"]

        # getting B$ 36.81 wouldn't look nice
        moneys = random.randint(int(min), int(max))
        replies = [
            f"You saved entire lelclub by throwing poop at people and got B$ {moneys} from government",
            f"you exploded thousands of things and magically got B$ {moneys}",
            f"you did ***something*** and got B$ {moneys}",
            f"you said \"flying spaghetti monster please give me lelgolds :place_of_worship: :place_of_worship: :place_of_worship:\" and magically got B$ {moneys}",
            f"you printed monis and got B$ {moneys}",
        ]

        # this does something 
        with open(f"data/money/{ctx.author.id}.json", "r+") as f:
            pain = json.load(f)
            pain["money"] += moneys
            f.seek(0)
            f.write(json.dumps(pain))
            f.truncate()

        embed = Embed(description=random.choice(replies), color=discord.Color(0x3eba49))
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
    
    # cool cooldown message :)
    @work.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(description=f"You cannot work for {error.retry_after:.2f}s.",
                                  color=discord.Color(0xff4865))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
    


    @commands.command(aliases=["give-money", "give_money"])
    async def pay(self, ctx, user: discord.User, amount: float):
        self.setup_user(ctx.author.id)
        self.setup_user(user.id)

        # does the author have moneys?
        author_moneys = 0
        with open(f"data/money/{ctx.author.id}.json", "r") as f:
            author_moneys = json.load(f)["money"]
        
        if author_moneys >= amount:
            # yes.
            with open(f"data/money/{ctx.author.id}.json", "r+") as f:
                pain = json.load(f)
                pain["money"] -= amount
                f.seek(0)
                f.write(json.dumps(pain))
                f.truncate()
            
            with open(f"data/money/{user.id}.json", "r+") as f:
                pain = json.load(f)
                pain["money"] += amount
                f.seek(0)
                f.write(json.dumps(pain))
                f.truncate()
            
            embed = Embed(description=f"Successfully transfered B$ {amount:,.2f} to {user.mention}.",
                          color=discord.Color(0x3eba49))
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = Embed(title="Error", description=f"You don't have that amount in cash!", 
                          color=discord.Color(0xff4865))
            await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(EconomyBasics(client))