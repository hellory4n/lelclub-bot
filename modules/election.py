import disnake as discord
from disnake import app_commands, SelectOption
from disnake.ext import commands
from disnake.ui import Select, View
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

    @commands.command(name="start-election")
    async def start_election(self, ctx):
        if (ctx.author.id == 748560377763201185):
            self.election_stuff["started"] = True
            self.save_election()
            await ctx.send("Election successfully started!")
        else:
            await ctx.send("You can't manage the election!")

    async def nominate_callback(self, inter: discord.ApplicationCommandInteraction):
        # if someone is already a candidate, override roles
        if inter.author.id in self.election_stuff["candidates"]:
            del self.election_stuff["candidates"][inter.user.id]
            self.election_stuff["candidates"].update({inter.user.id: inter.values})
        else:
            self.election_stuff["candidates"].update({inter.user.id: inter.values})

        self.save_election()
        await inter.send(content="You are now a candidate.")

    @commands.command()
    async def nominate(self, ctx):
        select = Select(
            custom_id="roles",
            placeholder="Choose a role",
            max_values=11,
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
        )

        select.callback = self.nominate_callback
        view = View()
        view.timeout = 60
        view.add_item(select)
        await ctx.send("What roles do you want? You can choose more than one.", view=view)

    @commands.command()
    async def dismiss(self, ctx):
        try:
            del self.election_stuff["candidates"][ctx.author.id]
            self.save_election()
            await ctx.send("Now you're not a candidate anymore")
        except:
            await ctx.send("You're not a candidate!")
    
    async def please_help_me(self, inter: discord.ApplicationCommandInteraction):
        voter = inter.author

        # save the governor vote :)
        if inter.values[0] in self.election_stuff["votes"][inter.author.id]:
            self.election_stuff["votes"][inter.author.id].pop(inter.values[0])
        else:
            self.election_stuff["votes"][inter.author.id].append(inter.values[0])
        self.save_election()
        
        await voter.send("Thank you for voting. Results will be announced on the 3rd of this month, on the same channel you got an @ everyone ping. (unless the bot breaks or something)")

    async def choose_governor_callback(self, inter: discord.ApplicationCommandInteraction):
        voter = inter.author
        state = inter.values[0]

        # so you can't vote for the governor of all states
        if inter.author.id in self.election_stuff["votes"]:
            # the -1 index gets the last item
            ye = self.election_stuff["votes"][inter.author.id][-1]
            if len(self.election_stuff["votes"][inter.author.id]) == 2 and ye != f"Governor of {state}":
                voter.send("You can't vote for the governor of multiple states!")
            else:
                # find candidates for the governor of the user's state and make a cool dropdown
                governor_candidates = []
                for name, roles in self.election_stuff["candidates"].items():
                    if f"Governor of {state}" in roles:
                        kgksg = await self.client.fetch_user(int(name))
                        governor_candidates.append(SelectOption(label=kgksg.display_name, value=f"{state}:{name}"))
                
                select = Select(
                    placeholder=f"Choose a governor for {state}",
                    options=governor_candidates
                )
                select.callback = self.please_help_me
                view = View()
                view.add_item(select)

                if len(governor_candidates) > 0:
                    await voter.send(f"One last thing to do, please choose who you want to be the governor of {state}", view=view)
                else:
                    await voter.send(f"There's no candidates for the governor of {state}, that's weird. Anyways thanks for voting!")

    async def choose_president_callback(self, inter: discord.ApplicationCommandInteraction):
        voter = inter.author

        # register president choice
        # vote will be edited if the user votes again
        if inter.author.id in self.election_stuff["votes"]:
            del self.election_stuff["votes"][inter.user.id]
            self.election_stuff["votes"].update({inter.user.id: [inter.values[0]]})
        else:
            self.election_stuff["votes"].update({inter.user.id: [inter.values[0]]})
        self.save_election()
        
        # state dropdown
        select = Select(
            placeholder="Choose a state",
            options=[
                SelectOption(label="Claps", emoji="👏"),
                SelectOption(label="Lelcenter", emoji="<:lelcube:1025170523744903199>"),
                SelectOption(label="Poop HQ", emoji="💩"),
                SelectOption(label="Ben State", emoji="<:ben:1026507448242143293>"),
                SelectOption(label="Breat Gritain", emoji="🍵"),
                SelectOption(label="Builders of La Grasa", emoji="🏗️"),
                SelectOption(label="France 2.0", emoji="🥖"),
                SelectOption(label="Berkelium", emoji="🅱️"),
                SelectOption(label="The Moon™", emoji="🌚"),
                SelectOption(label="Finger Island", emoji="👍")
            ]
        )
        select.callback = self.choose_governor_callback
        view = View()
        view.add_item(select)

        await voter.send("That's definitely one of the options! Now, what state are you from?", view=view)

    @commands.command()
    async def vote(self, ctx: commands.Context):
        if self.election_stuff["started"]:
            # make the president dropdown
            president_candidates = []
            for name, roles in self.election_stuff["candidates"].items():
                if "President" in roles:
                    
                    kgksg = await self.client.fetch_user(int(name))
                    president_candidates.append(SelectOption(label=kgksg.display_name, value=f"president:{name}"))
            
            select = Select(
                placeholder="Choose a president candidate",
                options=president_candidates
            )
            select.callback = self.choose_president_callback
            view = View()
            view.add_item(select)

            # vote on dms :)
            try:
                voter = ctx.author
                await voter.send("Thanks for deciding to vote, this will shape the future of lelclub. Votes are secure and anonymous :)\n\nWho do you want to be the president?", view=view)
            except:
                await ctx.send(f"{ctx.author.mention} please enable DMs to be able to vote, then try again")

def setup(client: commands.Bot):
    client.add_cog(Election(client))