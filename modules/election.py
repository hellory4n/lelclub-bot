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
        if self.election_stuff["started"]:
            await ctx.send("You can't do that while people are voting!")
        else:
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
        else:
            await ctx.send("The election hasn't started! They do on the 1st of each month tho (unless the bot breaks)")

    @commands.command(name="end-election")
    async def end_election(self, ctx: commands.Context):
        """{
            "started": true,
            "candidates":
                {"748560377763201185":
                    ["President", "Governor of Claps"],
                "928777777996505148":
                    ["President", "Governor of Claps", "Governor of Ben State", "Governor of Poop HQ", "Governor of Lelcenter", "Governor of Breat Gritain", "Governor of Builders of La Grasa", "Governor of France 2.0", "Governor of Berkelium", "Governor of The Moon\u2122", "Governor of Finger Island"]},
            "votes":
                {"928777777996505148":
                    ["president:928777777996505148", "The Moon\u2122:928777777996505148"],
                "748560377763201185":
                    ["president:748560377763201185", "Ben State:928777777996505148"]}}"""
        # only allow the founder of lelclub end the election ogmogmgogmogmgogmogkmg
        if (ctx.author.id == 748560377763201185):
            await ctx.send("Calculating results...")
            self.election_stuff["started"] = False
            self.save_election()

            # make a list of president candidates
            maybe_presidents = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "President" in roles:
                    maybe_presidents.update({user: 0})
            print(maybe_presidents)

            # calculate president results
            for voter, vote in self.election_stuff["votes"].items():
                # first item in the votes will always be the president, that's how the /vote commands saves it
                president_choice = vote[0].split(":")[1]
                maybe_presidents[president_choice] += 1
            print(maybe_presidents)
            
            states = [
                "Claps",
                "Lelcenter",
                "Poop HQ",
                "Ben State",
                "Breat Gritain",
                "Builders of La Grasa",
                "France 2.0",
                "Berkelium",
                "Finger Island",
                "The Moon™"
            ]

            # do the same for each state
            # too lazy to make this less shit it's 1 am
            # second item in the votes will always be a governor
            gclaps = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Claps" in roles:
                    gclaps.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Claps" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gclaps[governor_choice] += 1
            
            glelcenter = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Lelcenter" in roles:
                    glelcenter.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Lelcenter" in vote:
                    governor_choice = vote[0].split(":")[1]
                    glelcenter[governor_choice] += 1
            
            gpoophq = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Poop HQ" in roles:
                    gpoophq.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Poop HQ" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gpoophq[governor_choice] += 1
            
            gben = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Ben State" in roles:
                    gben.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Ben State" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gben[governor_choice] += 1
            
            gbg = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Breat Gritain" in roles:
                    gbg.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Breat Gritain" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gbg[governor_choice] += 1
            
            gbolg = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Builders of La Grasa" in roles:
                    gbolg.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Builders of La Grasa" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gbolg[governor_choice] += 1
            
            gfrance = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of France 2.0" in roles:
                    gfrance.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of France 2.0" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gfrance[governor_choice] += 1
            
            gbk = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Berkelium" in roles:
                    gbk.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Berkelium" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gbk[governor_choice] += 1
            
            gfinger = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of Finger Island" in roles:
                    gfinger.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of Finger Island" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gfinger[governor_choice] += 1
            
            gmoon = {}
            for user, roles in self.election_stuff["candidates"].items():
                if "Governor of The Moon™" in roles:
                    gmoon.update({user: 0})

            for voter, vote in self.election_stuff["votes"].items():
                if "Governor of The Moon™" in vote:
                    governor_choice = vote[0].split(":")[1]
                    gmoon[governor_choice] += 1
            
            # sort stuff :)
            # the last 100 lines were pure suffering
            maybe_presidents = sorted(maybe_presidents)
            gclaps = sorted(gclaps)
            glelcenter = sorted(glelcenter)
            gpoophq = sorted(gpoophq)
            gben = sorted(gben)
            gbg = sorted(gbg)
            gbolg = sorted(gbolg)
            gfrance = sorted(gfrance)
            gbk = sorted(gbk)
            gfinger = sorted(gfinger)
            gmoon = sorted(gmoon)

            # make cool embeds for the results :)
            president_results = discord.Embed(title="President Results")
            claps_results = discord.Embed(title="Claps Results")
            lelcenter_results = discord.Embed(title="Lelcenter Results")
            poophq_results = discord.Embed(title="Poop HQ Results")
            ben_results = discord.Embed(title="Ben State Results")
            breatgritain_results = discord.Embed(title="Breat Gritain Results")
            bolg_results = discord.Embed(title="Builders of La Grasa Results")
            france_results = discord.Embed(title="France 2.0 Results")
            berkelium_results = discord.Embed(title="Berkelium Results")
            finger_results = discord.Embed(title="Finger Island Results")
            moon_results = discord.Embed(title="The Moon™ Results")

            # more pain
            print(maybe_presidents)
            for ye, mues in maybe_presidents.values:
                president_results.description += f"<@{ye}>: {mues} votes\n"
            for ye in gclaps:
                claps_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in glelcenter:
                lelcenter_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gpoophq:
                poophq_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gben:
                ben_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gbg:
                breatgritain_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gbolg:
                bolg_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gfrance:
                france_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gbk:
                berkelium_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gfinger:
                finger_results.description += f"<@{candidate}>: {votes} votes\n"
            for ye in gmoon:
                moon_results.description += f"<@{candidate}>: {votes} votes\n"
            
            # this is really dumb
            await ctx.send(embeds=[
                claps_results,
                lelcenter_results,
                poophq_results,
                ben_results,
                breatgritain_results,
                bolg_results,
                france_results,
                berkelium_results,
                finger_results,
                moon_results
            ])
            await ctx.send(embed=president_results)

            # one final announcement
            total_votes = 0
            for candidate, votes in maybe_presidents.items():
                total_votes += votes
            
            winner_percentage = (total_votes/maybe_presidents[0])*100
            await ctx.send(f"<@{maybe_presidents[0]}> IS NOW THE PRESIDENT OF THE CAPITALIST UNITED FEDERAL DEMOCRATIC REPUBLIC STATES OF LELCLUB WITH A WHOPPING {winner_percentage}% OF VOTES (we had a total of {total_votes} votes)")

            # reset election data
            self.election_stuff = {
                "started": False,
                "candidates": {},
                "votes": {}
            }
            self.save_election()
        else:
            ctx.send("You can't manage the election!")

def setup(client: commands.Bot):
    client.add_cog(Election(client))