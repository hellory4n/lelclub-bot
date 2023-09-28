import disnake as discord
from disnake import Embed
from disnake.ui import View, TextInput
from disnake import Embed, ButtonStyle, Button, TextInputStyle
from disnake.ext import commands, tasks
import os
import json
import asyncio
from .economy_basics import EconomyBasics
import re

class Lelstex(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("lelstex cog loaded")
    
    class NewCompany(View):
        def __init__(self, *, timeout: float = 1000, client: commands.Bot) -> None:
            super().__init__(timeout=timeout)
            self.client = client

        @discord.ui.button(label="Start", style=ButtonStyle.blurple)
        async def receive(self, button: Button, inter: discord.MessageInteraction):
            await inter.response.send_modal(
                title="Register Company",
                custom_id="register_company",
                components=[
                    TextInput(
                        label="Name",
                        placeholder="Unlimited Money Limited",
                        custom_id="name",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=100,
                    ),
                    TextInput(
                        label="Code",
                        placeholder="money",
                        custom_id="code",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=5,
                    ),
                    TextInput(
                        label="Description",
                        placeholder="We are an amazing company that specializes in all things scams! Our great CEO is Ryan David Fraud.",
                        custom_id="description",
                        style=TextInputStyle.paragraph,
                        min_length=1,
                        max_length=1000,
                    ),
                    TextInput(
                        label="Amount of Stocks",
                        placeholder="694201337",
                        custom_id="stock_amount",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=11,
                    ),
                    TextInput(
                        label="Initial Stock Price",
                        placeholder="420.69",
                        custom_id="stock_price",
                        style=TextInputStyle.short,
                        min_length=1,
                        max_length=5,
                    ),
                ],
            )

            try:
                modal_inter: discord.ModalInteraction = await self.client.wait_for(
                    "modal_submit",
                    check=lambda i: i.custom_id == "register_company" and i.author.id == inter.author.id,
                    timeout=1000,
                )
            except asyncio.TimeoutError:
                return

            name = modal_inter.text_values["name"]
            code = modal_inter.text_values["code"]
            description = modal_inter.text_values["description"]
            amount = modal_inter.text_values["stock_amount"]
            price_ = modal_inter.text_values["stock_price"]

            # make sure the item doesn't already exist
            code = re.sub("[^a-z0-9]", "", code) # only alphanumeric characters and spaces allowed
            if os.path.exists(f"data/stocks/{code}.json"):
                embed = Embed(title="Error",
                              description=f"Stock with code `{code}` already exists.",
                              color=discord.Color(0xff4865))
                await modal_inter.response.send_message(embed=embed)
                return
            
            # make sure things the price and stock are valid
            price = 0
            stock = 0
            try:
                price = float(price_)
                if price < 0.01 or int(amount) < 0.01:
                    raise "bruh"
                else:
                    stock = int(amount)
            except:
                embed = Embed(title="Error",
                              description="Invalid price or stock. Are you sure these are valid numbers?",
                              color=discord.Color(0xff4865))
                await modal_inter.response.send_message(embed=embed)
                return

            # now we actually add the stock thing :)
            with open(f"data/stocks/{code}.json", 'w') as f:
                pain = {
                    "name": name,
                    "description": description,
                    "amount": stock,
                    "price": price,
                    "author": inter.author.id,
                    "price_history": {},
                    "news": {}
                }
                json.dump(pain, f)

            embed = Embed(description=f"Successfully created stock for the company`{name}`", color=discord.Color(0x3eba49))
            embed.set_author(name=modal_inter.author.display_name, icon_url=modal_inter.author.display_avatar.url)
            embed.add_field(name="Description", value=description, inline=True)
            embed.add_field(name="Code", value=code, inline=True)
            embed.add_field(name="Stocks Available", value=f"{stock:,}")
            embed.add_field(name="Initial Price", value=f"B$ {price:,.2f}")
            await modal_inter.response.send_message(embed=embed)

    @commands.command(aliases=["lelstex-register", "lelstex-add", "lelstex_add", "stock-register", "stock_register", "stockregister", "stock-add", "stock_add", "stockadd"])
    async def lelstex_register(self, ctx: commands.Context):
        EconomyBasics.setup_user(ctx.author.id)
        embed = Embed(color=0x008cff, description="You will answer a form to register your company. Click on the button below to continue.\n\nNOTES:\n- Make sure the company actually exists in <#1025193492584087593> \n- If your company is owned by another company, you should merge it with the stock of the parent company, not make it a separate stock\n- It's a good idea to register your company on the stock market after it has already grown quite a bit, not right after you created the company.\n- Make sure to not commit fraud!")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed, view=self.NewCompany(client=self.client))

def setup(client: commands.Bot):
    client.add_cog(Lelstex(client))