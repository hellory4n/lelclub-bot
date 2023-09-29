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
        if datetime.now(timezone.utc).hour == 15:
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
            exchange_rate = economy_thingies["previous_exchange_rate"] * ((inflation/100))
            economy_thingies["previous_exchange_rate"] = exchange_rate

            with open("data/economic_policies.json", "w") as f:
                json.dump(economy_thingies, f)

            # send the stats
            embed = Embed(title="Daily update on the economy", color=discord.Color(0x008cff))
            embed.add_field(name="GDP", value=f"B$ {gdp:,.2f} • {gdp_change:,.3f}% change :money_mouth:", inline=False)
            embed.add_field(name="Inflation", value=f"{inflation:,.2f}% :money_mouth:", inline=False)
            embed.add_field(name="Exchange rate", value=f"B$ {exchange_rate:,.2f} = US$ 1", inline=False)
            embed.add_field(name="10 most popular items", value=top_10_items_of_all_times, inline=False)
            channel = self.client.get_channel(1030483261249556490)
            await channel.send(embed=embed)



    @tasks.loop(minutes=60.0)
    async def salary_stuff(self):
        if datetime.utcnow().hour == 4 and datetime.utcnow().isoweekday() == 2:
            # first get a list of people that exist
            citizens: dict = {}
            with open("data/leaderboard.json", 'r') as f:
                citizens = json.load(f)
            
            total_salaries = 0
            for citizen, money in citizens.items():
                lelclub: discord.Guild = self.client.get_guild(1025162922797826059)
                cool_citizen: discord.Member = await lelclub.getch_member(citizen)
                epic_salary: int = 0
                if cool_citizen != None:
                    for role in cool_citizen.roles:
                        # executive branch
                        if role.name == "President" or role.name == "Vice President":
                            epic_salary += 10000
                            total_salaries += 10000
                        
                        if role.name.startswith("CEO of"):
                            epic_salary += 3000
                            total_salaries += 3000
                        
                        # legislative branch
                        if role.name == "Representative":
                            epic_salary += 2000
                            total_salaries += 2000
                        
                        # judiciary branch
                        if role.name == "Supreme Court":
                            epic_salary += 4000
                            total_salaries += 4000
                        
                        # governors
                        if role.name.startswith("Governor"):
                            epic_salary += 6000
                            total_salaries += 6000
                        
                        # all the other roles
                        # the code ever made
                        if (role.name == "Judge" or
                            role.name == "Soldier" or
                            role.name == "Doctor" or
                            role.name == "Farmer" or
                            role.name == "Astronaut"):
                            epic_salary += 6000
                            total_salaries += 6000
                        
                        if epic_salary > 0:
                            with open(f"data/money/{citizen}.json", "r+") as file:
                                pain = json.load(file)
                                pain["money"] += epic_salary
                                file.seek(0)
                                file.write(json.dumps(pain))
                                file.truncate()
            
            # make the government go into crippling debt
            # that account is the national gofundme
            with open("data/money/928777777996505148.json", 'r+') as f:
                suffer = json.load(f)
                suffer["money"] -= total_salaries
                f.seek(0)
                f.write(json.dumps(suffer))
                f.truncate()

            embed = Embed(
                title="Salaries from the Government",
                description=f"- <:gillbates:1027053227709042688> President and Vice President: B$ 10,000\n- :office_worker: CEOs (government): B$ 3,000\n- :sleeping: Representatives: B$ 2,000\n- :judge: Supreme Court: B$ 4,000\n- :moyai: Governors: B$ 6,000\n- :judge: Judges: B$ 6,000\n- :military_helmet: Soldiers: B$ 6,000\n- :health_worker: Doctors: B$ 6,000\n- :astronaut: Astronauts: B$ 6,000\n- :money_mouth: All of the salaries: B$ {total_salaries:,}", color=0x3eba49
            )
            client = self.client.get_channel(1126291049795559585)
            await client.send("<@&1026921409945014322> <@&1026921523493208095> <@&1025546848196378714> <@&1026919529953107970> <@&1048676462183592026> <@&1066500643830907000> <@&1048676880531861564> <@&1133512191107145818> <@&1134552621697466488> <@&1033442688034426971> <@&1133774757242871818> <@&1062399595017162852> <@&1139670263479414904> <@&1127489107178836038> <@&1026920056409563158> <@&1048677194051895397> <@&1059928836189474866> <@&1136807025720959016> <@&1141399771697926306> <@&1026909725297754184> <@&1025198958487806022> <@&1051890694698053703> <@&1049022180958154752> <@&1125516217642397766> <@&1125524660889595926> You got salaries!", embed=embed)



    @commands.Cog.listener()
    async def on_ready(self):
        self.economy_stats.start()
        self.salary_stuff.start()
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
                if new_percentage > 100 or new_percentage < 0 or new_threshold < 0:
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
    


    @commands.command(aliases=["print-money", "add-money", "add_money"])
    async def print_money(self, ctx: commands.Context, moneys, user: discord.User):
        # only the ceo of economy can use this
        role = discord.utils.get(ctx.message.guild.roles, name='CEO of economy')
        if role not in ctx.author.roles:
            embed = Embed(title="Error", description="You're not the CEO of economy!", color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            try:
                new_moneys = float(moneys)

                # indeed
                if new_moneys < 0:
                    embed = Embed(title="Error", description="The values provided seem very wrong.",
                                color=discord.Color(0xff4865))
                    await ctx.send(embed=embed)
                else:
                    # add the amount :)
                    EconomyBasics.setup_user(user.id)
                    with open(f"data/money/{user.id}.json", "r+") as f:
                        pain = json.load(f)
                        pain["money"] += new_moneys
                        pain["total"] += new_moneys
                        f.seek(0)
                        f.write(json.dumps(pain))
                        f.truncate()
                    EconomyBasics.update_leaderboard(user.id)
                    
                    embed = Embed(title="Success", description=f"{user.mention} now has more money.",
                            color=discord.Color(0x3eba49))
                    await ctx.send(embed=embed)
            except:
                embed = Embed(title="Error", description="Are you sure the arguments are numbers?",
                            color=discord.Color(0xff4865))
                await ctx.send(embed=embed)
    


    @commands.command(aliases=["remove-money", "delete-money", "delete_money"])
    async def remove_money(self, ctx: commands.Context, moneys, user: discord.User):
        # only the ceo of economy can use this
        role = discord.utils.get(ctx.message.guild.roles, name='CEO of economy')
        if role not in ctx.author.roles:
            embed = Embed(title="Error", description="You're not the CEO of economy!", color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            try:
                new_moneys = float(moneys)

                # indeed
                if new_moneys < 0:
                    embed = Embed(title="Error", description="The values provided seem very wrong.",
                                color=discord.Color(0xff4865))
                    await ctx.send(embed=embed)
                else:
                    # add the amount :)
                    EconomyBasics.setup_user(user.id)
                    with open(f"data/money/{user.id}.json", "r+") as f:
                        pain = json.load(f)
                        pain["money"] -= new_moneys
                        pain["total"] -= new_moneys
                        f.seek(0)
                        f.write(json.dumps(pain))
                        f.truncate()
                    EconomyBasics.update_leaderboard(user.id)
                    
                    embed = Embed(title="Success", description=f"{user.mention} now has less money.",
                            color=discord.Color(0x3eba49))
                    await ctx.send(embed=embed)
            except:
                embed = Embed(title="Error", description="Are you sure the arguments are numbers?",
                            color=discord.Color(0xff4865))
                await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(EconomicPolicies(client))