import discord
from discord import app_commands
from discord.ext import commands
import os
import json

class Election(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.election_stuff: dict[str, any] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        # setup election things :)
        if not os.path.isfile("../data/election.json"):
            with open("../data/election.json", "w+") as file:
                m = {
                    "started": False,
                    # Candidate example:
                    # candidates: {
                    #     james: [president, governor of claps],
                    #     fascist citizen: [all of the roles lol]
                    # }
                    "candidates": {},
                    # example:
                    # votes: {
                    #     id: [{james, president}, {fascist citizen, governor of claps}]
                    # }
                    "votes": {}
                }
                json.dump(m, file)
                self.election_stuff = m
        else:
            with open("../data/election.json", "r") as file:
                self.election_stuff = json.load(file)

        print("election cog loaded")

    @app_commands.command(name="start-election", description="Start an election, wowser")
    async def start_election(self, inter: discord.Interaction):
        await inter.response.send_message("my life be like ooooo aaaaa ooooo")

async def setup(client: commands.Bot):
    await client.add_cog(Election(client))