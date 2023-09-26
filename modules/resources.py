import disnake as discord
from disnake import Embed
from disnake.ext import commands, tasks
import os
import json
from .economy_basics import EconomyBasics
from datetime import datetime, timezone;

class Resources(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @tasks.loop(minutes=60.0)
    async def resource_thing(self):
        if datetime.now(timezone.utc).hour == 15:
            land = [
                "Fard City Coal",
                "Lelwoon Iron and Obamium",
                "Helpimacubia Iron and Obamium",
                "Switzerland 2.0 Obamium",
                "New Soodland Iron and Obamium",
                "New Bob Issues Rare Materials",
                "Southern BOLG Rare Materials"
                "Capital Coal and Obamium",
                "Thaizsanches Coal",
                "BOLG Uranium and Iron",
                "r/lelcity Oil and Natural Gas",
                "Breat Gritain Coal",
                "Breat Gritain Wood",
                "Claps Wood",
                "New Lelcity Coal",
                "Berkelium Iron and Obamium",
                "Berkelium Southern Potatos",
                "Berkelium Northern Potatos",
                "Berkelium Coal",
                "Desperatetopia Coal",
                "Soodland Coal and Oil",
                "Poop HQ Agonium and Oil",
                "Haha Funni City Obamium and Potatos",
                "Ben State Potatos"
            ]

            bruh: dict = {}
            with open("data/leaderboard.json", "r") as f:
                bruh = json.load(f)
            
            for cool_citizen, money in bruh.items():
                epic_items: dict = {}
                with open(f"data/items/{cool_citizen}.json", 'r') as f:
                    epic_items = json.load(f)

                save_file = False
                if "Fard City Coal" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 1
                    else:
                        epic_items.update({"Coal": 1})
                
                if "Lelwoon Iron and Obamium" in epic_items.keys():
                    save_file = True
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 2
                    else:
                        epic_items.update({"Iron": 2})
                    if "Obamium" in epic_items:
                        epic_items["Obamium"] += 3
                    else:
                        epic_items.update({"Obamium": 3})
                
                if "Helpimacubia Iron and Obamium" in epic_items.keys():
                    save_file = True
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 2
                    else:
                        epic_items.update({"Iron": 2})
                    if "Obamium" in epic_items:
                        epic_items["Obamium"] += 1
                    else:
                        epic_items.update({"Obamium": 1})
                
                if "Switzerland 2.0 Obamium" in epic_items.keys():
                    save_file = True
                    if "Obamium" in epic_items:
                        epic_items["Obamium"] += 1
                    else:
                        epic_items.update({"Obamium": 1})
                
                if "New Soodland Iron and Obamium" in epic_items.keys():
                    save_file = True
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 1
                    else:
                        epic_items.update({"Iron": 1})
                    if "Obamium" in epic_items:
                        epic_items["Obamium"] += 1
                    else:
                        epic_items.update({"Obamium": 1})
                
                if "New Bob Issues Rare Materials" in epic_items.keys():
                    save_file = True
                    if "Diamonds" in epic_items:
                        epic_items["Diamonds"] += 1
                    else:
                        epic_items.update({"Diamonds": 1})
                    if "Gold" in epic_items:
                        epic_items["Gold"] += 1
                    else:
                        epic_items.update({"Gold": 1})
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 1
                    else:
                        epic_items.update({"Iron": 1})
                
                if "Southern BOLG Rare Materials" in epic_items.keys():
                    save_file = True
                    if "Diamonds" in epic_items:
                        epic_items["Diamonds"] += 1
                    else:
                        epic_items.update({"Diamonds": 1})
                    if "Gold" in epic_items:
                        epic_items["Gold"] += 1
                    else:
                        epic_items.update({"Gold": 1})
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 1
                    else:
                        epic_items.update({"Iron": 1})
                
                if "Capital Coal and Obamium" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 1
                    else:
                        epic_items.update({"Coal": 1})
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 1
                    else:
                        epic_items.update({"Iron": 1})
                
                if "Thaizsanches Coal" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 1
                    else:
                        epic_items.update({"Coal": 1})
                
                if "BOLG Uranium and Iron" in epic_items.keys():
                    save_file = True
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 3
                    else:
                        epic_items.update({"Iron": 3})
                    if "Uranium" in epic_items:
                        epic_items["Uranium"] += 3
                    else:
                        epic_items.update({"Uranium": 3})
                
                if "r/lelcity Oil and Natural Gas" in epic_items.keys():
                    save_file = True
                    if "Oil" in epic_items:
                        epic_items["Oil"] += 3
                    else:
                        epic_items.update({"Oil": 3})
                    if "Natural Gas" in epic_items:
                        epic_items["Natural Gas"] += 2
                    else:
                        epic_items.update({"Natural Gas": 2})
                
                if "Breat Gritain Coal" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 1
                    else:
                        epic_items.update({"Coal": 1})
                
                if "Breat Gritain Wood":
                    save_file = True
                    if "Wood" in epic_items:
                        epic_items["Wood"] += 1
                    else:
                        epic_items.update({"Wood": 1})
                
                if "Claps Wood" in epic_items.keys():
                    save_file = True
                    if "Wood" in epic_items:
                        epic_items["Wood"] += 3
                    else:
                        epic_items.update({"Wood": 3})
                
                if "New Lelcity Coal" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 1
                    else:
                        epic_items.update({"Coal": 1})
                
                if "Berkelium Iron and Obamium" in epic_items.keys():
                    save_file = True
                    if "Iron" in epic_items:
                        epic_items["Iron"] += 2
                    else:
                        epic_items.update({"Iron": 2})
                    if "Obamium" in epic_items:
                        epic_items["Obamium"] += 1
                    else:
                        epic_items.update({"Obamium": 1})
                
                if "Berkelium Southern Potatos" in epic_items.keys():
                    save_file = True
                    if "Potatos" in epic_items:
                        epic_items["Potatos"] += 2
                    else:
                        epic_items.update({"Potatos": 2})

                if "Berkelium Northern Potatos" in epic_items.keys():
                    save_file = True
                    if "Potatos" in epic_items:
                        epic_items["Potatos"] += 3
                    else:
                        epic_items.update({"Potatos": 3})
                
                if "Berkelium Coal" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 3
                    else:
                        epic_items.update({"Coal": 3})
                
                if "Desperatetopia Coal" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 1
                    else:
                        epic_items.update({"Coal": 1})
                
                if "Soodland Coal and Oil" in epic_items.keys():
                    save_file = True
                    if "Coal" in epic_items:
                        epic_items["Coal"] += 1
                    else:
                        epic_items.update({"Coal": 1})
                    if "Oil" in epic_items:
                        epic_items["Oil"] += 2
                    else:
                        epic_items.update({"Oil": 2})
                
                if "Poop HQ Agonium and Oil" in epic_items.keys():
                    save_file = True
                    if "Oil" in epic_items:
                        epic_items["Oil"] += 1
                    else:
                        epic_items.update({"Oil": 1})
                    if "Agonium" in epic_items:
                        epic_items["Agonium"] += 9
                    else:
                        epic_items.update({"Agonium": 9})
                
                if "Haha Funni City Obamium and Potatos" in epic_items.keys():
                    save_file = True
                    if "Obamium" in epic_items:
                        epic_items["Obamium"] += 2
                    else:
                        epic_items.update({"Obamium": 2})
                    if "Potatos" in epic_items:
                        epic_items["Potatos"] += 3
                    else:
                        epic_items.update({"Potatos": 3})
                
                if "Ben State Potatos" in epic_items.keys():
                    save_file = True
                    if "Potatos" in epic_items:
                        epic_items["Potatos"] += 4
                    else:
                        epic_items.update({"Potatos": 4})
                
                if save_file:
                    with open(f"data/items/{cool_citizen}.json", "w") as f:
                        json.dump(epic_items, f)

    @commands.Cog.listener()
    async def on_ready(self):
        self.resource_thing.start()
        print("resources cog loaded")

def setup(client: commands.Bot):
    client.add_cog(Resources(client))