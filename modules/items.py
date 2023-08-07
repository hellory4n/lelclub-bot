from typing import Optional
import disnake as discord
from disnake.ui import View, TextInput
from disnake import Embed, ButtonStyle, Button, TextInputStyle
from disnake.ext import commands
import os
import json
from .economy_basics import EconomyBasics
import asyncio

class Items(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("item cog loaded")
    
    class NewItem(View):
        def __init__(self, *, timeout: float | None = 180, client: commands.Bot) -> None:
            super().__init__(timeout=timeout)
            self.client = client

        @discord.ui.button(label="Start", style=ButtonStyle.blurple)
        async def receive(self, button: Button, inter: discord.MessageInteraction):
            await inter.response.send_modal(
                title="Create Item",
                custom_id="create_item",
                components=[
                    TextInput(
                        label="Name",
                        placeholder="Cool Item™",
                        custom_id="name",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=50,
                    ),
                    TextInput(
                        label="Price",
                        placeholder="69.42",
                        custom_id="price",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=25
                    ),
                    TextInput(
                        label="Description",
                        placeholder="This is one of the items of all time.",
                        custom_id="description",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=100
                    ),
                    TextInput(
                        label="Stock",
                        placeholder="Leave empty if there's unlimited stock",
                        custom_id="stock",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=25,
                        required=False
                    ),
                    TextInput(
                        label="Wallet",
                        placeholder="Use if you have a wallet for your company",
                        custom_id="wallet",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=100,
                        required=False
                    )
                ],
            )

            try:
                modal_inter: discord.ModalInteraction = await self.client.wait_for(
                    "modal_submit",
                    check=lambda i: i.custom_id == "create_item" and i.author.id == inter.author.id,
                    timeout=1000,
                )
            except asyncio.TimeoutError:
                return

            name = modal_inter.text_values["name"]
            price_ = modal_inter.text_values["price"]
            description = modal_inter.text_values["description"]
            stock_ = modal_inter.text_values["stock"]
            wallet = modal_inter.text_values["wallet"]

            # make sure things the price and stock are valid
            price = 0
            stock = 0
            try:
                price = float(price_)
                if (stock_ == ""):
                    stock = -1
                else:
                    stock = int(stock_)
            except:
                embed = Embed(title="Error",
                              description="Invalid price or stock. Are you sure these are valid numbers?",
                              color=discord.Color(0xff4865))
                await modal_inter.response.send_message(embed=embed)
                return

            # make sure the wallet exists and stuff
            if wallet != "":
                bruh = {}
                with open(f"data/money/{modal_inter.author.id}.json", "r") as f:
                    bruh = json.load(f)
                
                if not wallet in bruh["wallets"]:
                    embed = Embed(title="Error",
                                description=f"Wallet `{wallet}` not found. (remember to leave it empty for the cash wallet)",
                                color=discord.Color(0xff4865))
                    await modal_inter.response.send_message(embed=embed)
                    return
            else:
                wallet = ""

            stock_but_the_user_sees_it = ""
            if stock == -1:
                stock_but_the_user_sees_it = "unlimited"
            else:
                stock_but_the_user_sees_it = f"{stock:,.2f}"
            
            wallet_but_the_user_sees_it = ""
            if wallet == "":
                wallet_but_the_user_sees_it = "Cash"
            else:
                wallet_but_the_user_sees_it = wallet

            # now we actually add the item :)
            with open(f"data/shop.json", "r+") as f:
                pain = json.load(f)
                pain.update({
                    name: {
                        "author": modal_inter.author.id,
                        "price": price,
                        "description": description,
                        "stock": stock,
                        "wallet": wallet
                    }
                })
                f.seek(0)
                f.write(json.dumps(pain))
                f.truncate()

            embed = Embed(description=f"Successfully created item `{name}`", color=discord.Color(0x3eba49))
            embed.set_author(name=modal_inter.author.display_name, icon_url=modal_inter.author.display_avatar.url)
            embed.add_field(name="Price", value=f"B$ {price:,.2f}", inline=True)
            embed.add_field(name="Description", value=description, inline=True)
            embed.add_field(name="Stock", value=stock_but_the_user_sees_it, inline=True)
            embed.add_field(name="Wallet", value=wallet_but_the_user_sees_it, inline=True)
            await modal_inter.response.send_message(embed=embed)

    @commands.command(aliases=["create-item", "add-item", "add_item", "new-item", "new_item"])
    async def create_item(self, ctx: commands.Context):
        EconomyBasics.setup_user(ctx.author.id)
        embed = Embed(color=0x008cff, description="You will answer a form to create the store item. Press the button below to continue.")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed, view=self.NewItem(client=self.client))
    


    class EditItem(View):
        def __init__(self, *, timeout: float | None = 180, client: commands.Bot, name: str) -> None:
            super().__init__(timeout=timeout)
            self.client = client
            self.name = name

        @discord.ui.button(label="Start", style=ButtonStyle.blurple)
        async def receive(self, button: Button, inter: discord.MessageInteraction):
            await inter.response.send_modal(
                title="Edit Item",
                custom_id="edit_item",
                components=[
                    TextInput(
                        label="Price",
                        placeholder="69.42",
                        custom_id="price",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=25,
                        required=False
                    ),
                    TextInput(
                        label="Description",
                        placeholder="This is one of the items of all time.",
                        custom_id="description",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=100,
                        required=False
                    ),
                    TextInput(
                        label="Stock",
                        placeholder="Leave empty if there's unlimited stock",
                        custom_id="stock",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=25,
                        required=False
                    ),
                    TextInput(
                        label="Wallet",
                        placeholder="Use if you have a wallet for your company",
                        custom_id="wallet",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=100,
                        required=False
                    )
                ],
            )

            try:
                modal_inter: discord.ModalInteraction = await self.client.wait_for(
                    "modal_submit",
                    check=lambda i: i.custom_id == "edit_item" and i.author.id == inter.author.id,
                    timeout=1000,
                )
            except asyncio.TimeoutError:
                return

            price_ = modal_inter.text_values["price"]
            description = modal_inter.text_values["description"]
            stock_ = modal_inter.text_values["stock"]
            wallet = modal_inter.text_values["wallet"]

            # make sure things the price and stock are valid
            price = 0
            stock = 0
            try:
                if price_ == "":
                    price = -1
                else:
                    price = float(price_)

                if stock_ == "":
                    stock = -1
                else:
                    stock = int(stock_)
            except:
                embed = Embed(title="Error",
                              description="Invalid price or stock. Are you sure these are valid numbers?",
                              color=discord.Color(0xff4865))
                await modal_inter.response.send_message(embed=embed)
                return

            # make sure the wallet exists and stuff
            if wallet != "":
                bruh = {}
                with open(f"data/money/{modal_inter.author.id}.json", "r") as f:
                    bruh = json.load(f)
                
                if not wallet in bruh["wallets"]:
                    embed = Embed(title="Error",
                                description=f"Wallet `{wallet}` not found. (remember to leave it empty for the cash wallet)",
                                color=discord.Color(0xff4865))
                    await modal_inter.response.send_message(embed=embed)
                    return
            else:
                wallet = ""

            # now we actually edit the item :)
            with open(f"data/shop.json", "r+") as f:
                pain = json.load(f)
                if description != "":
                    pain[self.name]["description"] = description
                if price != -1:
                    pain[self.name]["price"] = price
                if stock != -1:
                    pain[self.name]["stock"] = stock
                if wallet != "":
                    pain[self.name]["wallet"] = wallet
                f.seek(0)
                f.write(json.dumps(pain))
                f.truncate()

            embed = Embed(description=f"Successfully edited item `{self.name}`", color=discord.Color(0x3eba49))
            embed.set_author(name=modal_inter.author.display_name, icon_url=modal_inter.author.display_avatar.url)
            await modal_inter.response.send_message(embed=embed)

    @commands.command(aliases=["edit-item"])
    async def edit_item(self, ctx: commands.Context, *, name: str):
        EconomyBasics.setup_user(ctx.author.id)

        pain = {}
        with open("data/shop.json", "r") as f:
            pain = json.load(f)
        
        if not name in pain:
            embed = Embed(title="Error",
                          description=f"Item `{name}` not found.",
                          color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            embed = Embed(color=0x008cff,
                          description="You will answer a form to edit the item. Leave empty anything you don't want to change. Press the button below to continue.\n\nNOTE: The name can't be changed due to technical limitations.")
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed, view=self.EditItem(client=self.client, name=name))
    


    @commands.command(aliases=["remove-item", "delete-item", "remove_item"])
    async def delete_item(self, ctx, *, item):
        EconomyBasics.setup_user(ctx.author.id)

        pain = {}
        with open(f"data/shop.json", "r") as f:
            pain = json.load(f)
        
        # find item
        if not item in pain:
            embed = Embed(title="Error", description=f"Item `{item}` not found.", 
                            color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            # we need to ask the user to confirm cuz yes
            embed = Embed(description=f"Are you sure you want to delete {item}? Keep in mind that some users might still own this item.\n\nSend \"y\" to confirm.",
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
                del pain[item]
                with open(f"data/shop.json", "w") as f:
                    json.dump(pain, f)

                await ctx.send(f"{item} is now gone.")
    


    @commands.command(aliases=["item-info"])
    async def item_info(self, ctx: commands.Context, *, item: str):
        pain = {}
        with open(f"data/shop.json", "r") as f:
            pain = json.load(f)
        
        # find item
        if not item in pain:
            embed = Embed(title="Error", description=f"Item `{item}` not found.", 
                            color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
        else:
            stock_but_the_user_sees_it = ""
            if pain[item]["stock"] == -1:
                stock_but_the_user_sees_it = "unlimited"
            else:
                stock_but_the_user_sees_it = f"{pain[item]['stock']:,.2f}"
            
            wallet_but_the_user_sees_it = ""
            if pain[item]["wallet"] == "":
                wallet_but_the_user_sees_it = "Cash"
            else:
                wallet_but_the_user_sees_it = pain[item]["wallet"]

            embed = Embed(title=item, color=discord.Color(0x008cff))
            embed.add_field(name="Author", value=f"<@{pain[item]['author']}>", inline=True)
            embed.add_field(name="Price", value=f"B$ {pain[item]['price']:,.2f}", inline=True)
            embed.add_field(name="Description", value=pain[item]['description'], inline=True)
            embed.add_field(name="Stock", value=stock_but_the_user_sees_it, inline=True)
            embed.add_field(name="Wallet", value=wallet_but_the_user_sees_it, inline=True)
            await ctx.send(embed=embed)
    


    @commands.command(aliases=["purchase", "get"])
    async def buy(self, ctx: commands.Context, item: str, amount: int = 1):
        EconomyBasics.setup_user(ctx.author.id)

        # does the item exist?
        pain = {}
        with open(f"data/shop.json", "r") as f:
            pain = json.load(f)
        
        if not item in pain:
            embed = Embed(title="Error", description=f"Item `{item}` not found.\n (If the name has spaces then put it in quotes, example: `l.buy \"cool item\"`)", 
                            color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
            return

        # make sure there's enough stock
        if not pain[item]["stock"] == -1:
            if amount > pain[item]["stock"]:
                embed = Embed(title="Error", description=f"The stock available for this item is only {pain[item]['stock']:,.2f}", 
                              color=discord.Color(0xff4865))
                await ctx.send(embed=embed)
                return

        # make sure the payment info is valid and stuff
        seller = {}
        
        try:
            with open(f"data/money/{pain[item]['author']}.json", "r") as f:
                seller = json.load(f)
            if pain[item]["wallet"] != "":
                if pain[item]["wallet"] not in seller["wallets"]:
                    raise "bruh"
        except:
            embed = Embed(title="Error", description="Payment info from the seller seems incorrect.",
                          color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
            return

        # make sure the user can actually afford this item
        price = pain[item]["price"] * amount
        buyer = {}
        with open(f"data/money/{ctx.author.id}.json", "r") as f:
            buyer = json.load(f)
        
        if price > buyer["money"]:
            embed = Embed(title="Error", description="Not enough money in cash!",
                          color=discord.Color(0xff4865))
            await ctx.send(embed=embed)
            return
        
        # ok everything is right, we can actually buy the product now
        # first update the moneys
        if pain[item]["wallet"] != "":
            seller["wallets"][pain[item]["wallet"]] += price
        else:
            seller["money"] += price

        seller["total"] += price
        buyer["money"] -= price
        buyer["total"] -= price

        with open(f"data/money/{pain[item]['author']}.json", "w") as f:
            json.dump(seller, f)
        with open(f"data/money/{ctx.author.id}.json", "w") as f:
            json.dump(buyer, f)
        
        EconomyBasics.update_leaderboard(pain[item]["author"])
        EconomyBasics.update_leaderboard(ctx.author.id)

        # now add the item to the user's inventory
        with open(f"data/items/{ctx.author.id}.json", "r+") as f:
            bruh = json.load(f)
            bruh.update({item: amount})
            f.seek(0)
            f.write(json.dumps(bruh))
            f.truncate()
        
        # update the stock
        # -1 means unlimited stock
        if pain[item]["stock"] != -1:
            with open(f"data/shop.json", "r+") as f:
                bruh = json.load(f)
                bruh[item]["stock"] -= amount
                f.seek(0)
                f.write(json.dumps(pain))
                f.truncate()
        
        embed = Embed(description=f"Successfully bought {amount:,} {item}s", color=discord.Color(0x3eba49))
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(Items(client))