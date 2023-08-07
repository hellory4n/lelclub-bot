import disnake as discord
from disnake import Embed
from disnake.ext import commands
import os
import json

class EconomicPolicies(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("economic policies cog loaded")

    @commands.command(aliases=["work-payout"])
    async def work_payout(self, ctx, min, max):
        # only the ceo of economy can use this
        role = discord.utils.get(ctx.message.guild.roles, name='CEO of economy')
        if role not in ctx.author.roles:
            embed = Embed(title="Error", description="You're not the CEO of economy!", color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            try:
                new_min = float(min)
                new_max = float(max)

                # indeed
                if new_min > new_max:
                    embed = Embed(title="Error", description="Minimum amount is bigger than maximum amount.",
                                color=discord.Color(0xff4865))
                    await ctx.send(embed=embed)
                else:
                    # actually save the amounts lol
                    with open(f"data/economic_policies.json", "r+") as f:
                        pain = json.load(f)
                        pain["work_min"] = new_min
                        pain["work_max"] = new_max
                        f.seek(0)
                        f.write(json.dumps(pain))
                        f.truncate()
                    
                    embed = Embed(title="Success", description="Work's payout has been successfully changed.",
                            color=discord.Color(0x3eba49))
                    await ctx.send(embed=embed)
            except:
                embed = Embed(title="Error", description="Are you sure the arguments are numbers?",
                            color=discord.Color(0xff4865))
                await ctx.send(embed=embed)
    


    @commands.command(aliases=["set-tax"])
    async def set_tax(self, ctx: commands.Context, threshold, percentage):
        # only the ceo of economy can use this
        role = discord.utils.get(ctx.message.guild.roles, name='CEO of economy')
        if role not in ctx.author.roles:
            embed = Embed(title="Error", description="You're not the CEO of economy!", color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            try:
                new_threshold = float(threshold)
                new_percentage = float(percentage)

                # indeed
                if new_percentage > 10 or new_percentage < 0 or new_threshold < 0:
                    embed = Embed(title="Error", description="The values provided seem very wrong.",
                                color=discord.Color(0xff4865))
                    await ctx.send(embed=embed)
                else:
                    # actually save the amounts lol
                    with open(f"data/economic_policies.json", "r+") as f:
                        pain = json.load(f)
                        pain["tax_threshold"] = new_threshold
                        pain["tax_percentage"] = new_percentage
                        f.seek(0)
                        f.write(json.dumps(pain))
                        f.truncate()
                    
                    embed = Embed(title="Success", description="Taxes have been successfully changed.",
                            color=discord.Color(0x3eba49))
                    await ctx.send(embed=embed)
            except:
                embed = Embed(title="Error", description="Are you sure the arguments are numbers?",
                            color=discord.Color(0xff4865))
                await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(EconomicPolicies(client))