import disnake as discord
from disnake.ext import commands, tasks
import os
import asyncio
import json
import random
import dotenv

dotenv.load_dotenv(".env")

epic_cool_intents = discord.Intents.default()
epic_cool_intents.message_content = True
client = commands.Bot(command_prefix=commands.when_mentioned_or("l-"), intents=epic_cool_intents)
client.remove_command("help")

@client.event
async def on_ready():
    await suffering.start()
    print("hi")

# top tier error handling
"""@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Error", description=f"`{error}`\n\nFeel free to ping <@748560377763201185> when seeing errors like this, we need to help the bot be more stable for the good of lelclub <:lelflag:1136802749347020870> <:lelflag:1136802749347020870>", color=discord.Color(0xff4865))
    await ctx.send(embed=embed)"""

@client.command()
async def ping(ctx):
    await ctx.send(f"i'm definitely alive")

@client.command()
async def help(ctx):
    cool_embed = discord.Embed(title="Cool lelclub bot™", description="[] means it's an optional argument", color=discord.Color(0x008cff))
    cool_embed.add_field(name="Essential stuff", value="These are very important for the economy\n`l.bal [user]`: see how much money someone has\n`l.work`: easy money\n`l.pay user amount`: give moneys to someone else\n`l.lb`: see who's the richest people in our great nation", inline=False)
    cool_embed.add_field(name="Wallets", value="Useful for organizing your money and stuff\n`l.create-wallet name`: create a wallet\n`l.dep amount wallet`: put money in a wallet\n`l.with amount wallet`: remove money from a wallet and put it in cash\n`l.remove-wallet wallet`: removes a wallet", inline=False)
    cool_embed.add_field(name="Items", value="Epic goods and products\n`l.buy item [amount]`: buy an amazing item\n`l.inv [user]`: see the wonderful items you own\n`l.give-item item user [amount]`: give some of your wonderful items to someone else\n`l.new-item`: creates a new item\n`l.edit-item name`: edits an existing item\n`l.remove-item name`: makes an item unavailable for buying\n`l.item-info name`: get info about an item", inline=False)
    cool_embed.add_field(name="Economic policies", value="Useful when you're the CEO of economy\n`l.work-payout min max`: set how much l.work gives\n`l.print-money amount user`: remember that printing money can cause inflation!\n`l.remove-money amount user`: make money magically disappear from existence", inline=False)
    await ctx.send(embed=cool_embed)

cool_token = os.getenv("TOKEN")
version = os.getenv("VERSION")

# it's a loop :)
@tasks.loop(seconds = 30)
async def suffering():
    pain = [
        "Wii Are Resorting to Violence",
        "Mining & Crafting",
        "UnderCroch",
        "Overlook",
        "Galaxy Citizen",
        "Power Distance 5",
        "Pablo",
        "Squilliam Fancyson",
        "MOMAZOS DIEGO ADVENTURE 2",
        "Funcade",
        "Funcade Adventures"
    ]
    await client.change_presence(activity=discord.Game(f"{random.choice(pain)} on Is Tim"))

client.load_extensions("./modules/")
client.run(cool_token)