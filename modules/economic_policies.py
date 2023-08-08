import disnake as discord
from disnake import Embed
from disnake.ext import commands, tasks
import os
import json
from datetime import datetime, timezone
from .economy_basics import EconomyBasics
import itertools

class EconomicPolicies(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @tasks.loop(minutes=60.0)
    async def economy_stats(self):
        if datetime.now(timezone.utc).hour == 16:
            # calculate gdp
            gdp = 0.0
            bruh = {}
            with open("data/leaderboard.json", "r") as f:
                bruh = json.load(f)
            
            for user, moneys in bruh.items():
                gdp += moneys
            
            # calculate increase/decrease in gdp
            economy_thingies = {}
            with open("data/economic_policies.json", "r") as f:
                economy_thingies = json.load(f)
            gdp_change = (gdp - (economy_thingies["previous_gdp"]+1)) / (economy_thingies["previous_gdp"]+1) * 100
            economy_thingies["previous_gdp"] = gdp
            
            # get the 10 most popular items to calculate inflation
            items = {}
            with open("data/shop.json", "r") as f:
                items = json.load(f)
            top_10_items = dict(sorted(items.items(), key=lambda x:x[1]["purchases"], reverse=True))
            if len(top_10_items) > 10:
                top_10_items = dict(itertools.islice(top_10_items.items(), 10))
            else:
                top_10_items = dict(itertools.islice(top_10_items.items(), len(top_10_items)))

            # actually calculate inflation, also top 10 items
            price_sum = 0.0
            top_10_items_of_all_times = ""
            m = 0
            for item, info in top_10_items.items():
                m += 1
                price_sum += info["price"]
                top_10_items_of_all_times += f"{m}. {item}: {info['purchases']:,} purchases\n"
            
            average_price_index = (price_sum / (economy_thingies["previous_price_sum"]+1)) / 100
            inflation = ((average_price_index - economy_thingies["previous_average_price_index"])
                         / (economy_thingies["previous_average_price_index"]+1)) * 100

            economy_thingies["previous_price_sum"] = price_sum
            economy_thingies["previous_average_price_index"] = average_price_index

            # calculate exchange rate
            exchange_rate = economy_thingies["previous_exchange_rate"] * ((inflation/100)+1)
            economy_thingies["previous_exchange_rate"] = exchange_rate

            with open("data/economic_policies.json", "w") as f:
                json.dump(economy_thingies, f)

            # send the stats
            embed = Embed(title="Daily update on the economy")
            embed.add_field(name="GDP", value=f"B$ {gdp:,.2f} • {gdp_change:,.3f}% change :money_mouth:", inline=False)
            embed.add_field(name="Inflation", value=f"{inflation:,.2f}% :money_mouth:", inline=False)
            embed.add_field(name="Exchange rate", value=f"B$ {exchange_rate:,.2f} = US$ 1", inline=False)
            embed.add_field(name="10 most popular items", value=top_10_items_of_all_times, inline=False)
            channel = self.client.get_channel(1030483261249556490)
            await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_ready(self):
        self.economy_stats.start()
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