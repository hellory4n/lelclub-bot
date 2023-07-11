import discord
from discord import app_commands, SelectOption
from discord.ext import commands
from discord.ui import Select, View
import json

class Election(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.election_stuff: dict[str, any] = {}

        with open("data/election.json", "r") as file:
            self.election_stuff = json.load(file)

    @commands.Cog.listener()
    async def on_ready(self):
        print("election cog loaded")
    
    def save_election(self):
        with open("data/election.json", "w") as file:
            json.dump(self.election_stuff, file)

    @app_commands.command(name="start-election", description="Start an election, wowser")
    async def start_election(self, inter: discord.Interaction):
        if (inter.user.id == 748560377763201185):
            self.election_stuff["started"] = True
            self.save_election()
            await inter.response.send_message("Election successfully started!", ephemeral=True)
        else:
            await inter.response.send_message("You can't manage the election!", ephemeral=True)
    
    class CoolRoleDropdown(Select):
        def __init__(self):
            options=[
                SelectOption(label="President", emoji="🧑‍💼"),
                SelectOption(label="Governor of Claps", emoji="👏"),
                SelectOption(label="Governor of Lelcenter", emoji="<:lelcube:1025170523744903199>"),
                SelectOption(label="Governor of Poop HQ", emoji="💩"),
                SelectOption(label="Governor of Ben State", emoji="<:ben:1026507448242143293>"),
                SelectOption(label="Governor of Breat Gritain", emoji="🍵"),
                SelectOption(label="Governor of Builders of La Grasa", emoji="🏗️"),
                SelectOption(label="Governor of France 2.0", emoji="🥖"),
                SelectOption(label="Governor of Berkelium", emoji="🅱️"),
                SelectOption(label="Governor of The Moon™", emoji="🌚"),
                SelectOption(label="Governor of Finger Island", emoji="👍")
            ]
            super().__init__(
                custom_id="roles",
                placeholder="Epic roles",
                max_values=11,
                options=options
            )
        
        async def callback(self, inter: discord.Interaction):
            self.election_stuff["candidates"][inter.user.id] == self.values
            self.save_election()
            print("this works?")
            await inter.edit_original_message(content="Now people will be able to vote for you in the next election! Remember that elections start on the 1st of every month", view=None)

    @app_commands.command(name="nominate", description="Become a candidate in the next election!")
    async def nominate(self, inter: discord.Interaction):
        view = View()
        view.timeout = 180
        view.add_item(self.CoolRoleDropdown)
        await inter.response.send_message("What roles do you want? You can choose more than one.", ephemeral=True, view=view)

async def setup(client: commands.Bot):
    await client.add_cog(Election(client))