import discord
from discord import app_commands
from discord.ext import commands
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
        self.election_stuff["started"] = True
        self.save_election()
        await inter.response.send_message("Election successfully started!", ephemeral=True)

async def setup(client: commands.Bot):
    await client.add_cog(Election(client))