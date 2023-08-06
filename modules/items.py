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

            tag_name = modal_inter.text_values["name"]
            tag_content = modal_inter.text_values["content"]

            embed = discord.Embed(title=f"Tag created: `{tag_name}`")
            embed.add_field(name="Content", value=tag_content)
            await modal_inter.response.send_message(embed=embed)

    @commands.command(aliases=["create-item", "add-item", "add_item", "new-item", "new_item"])
    async def create_item(self, ctx: commands.Context):
        EconomyBasics.setup_user(ctx.author.id)
        embed = Embed(color=0x008cff, description="You will answer a form to create the store item. Press the button below to continue.")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed, view=self.NewItem(client=self.client))

def setup(client: commands.Bot):
    client.add_cog(Items(client))