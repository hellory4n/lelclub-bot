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

            bruh = {}
            with open("data/leaderboard.json", "r") as f:
                bruh = json.load(f)
            
            for cool_citizen, money in bruh:
                epic_items = {}
                with open(f"data/items/{cool_citizen}", 'r') as f:
                    epic_items = epic_items
                
                save_file = False
                for cool_land in land:
                    if cool_land in epic_items:
                        save_file = True
                        if cool_land == "Fard City Coal":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 1
                            else:
                                epic_items.update({"Coal": 1})
                        
                        if cool_land == "Lelwoon Iron and Obamium":
                            if "Iron" in epic_items:
                                epic_items["Iron"] += 2
                            else:
                                epic_items.update({"Iron": 2})
                            if "Obamium" in epic_items:
                                epic_items["Obamium"] += 3
                            else:
                                epic_items.update({"Obamium": 3})
                        
                        if cool_land == "Helpimacubia Iron and Obamium":
                            if "Iron" in epic_items:
                                epic_items["Iron"] += 2
                            else:
                                epic_items.update({"Iron": 2})
                            if "Obamium" in epic_items:
                                epic_items["Obamium"] += 1
                            else:
                                epic_items.update({"Obamium": 1})
                        
                        if cool_land == "Switzerland 2.0 Obamium":
                            if "Obamium" in epic_items:
                                epic_items["Obamium"] += 1
                            else:
                                epic_items.update({"Obamium": 1})
                        
                        if cool_land == "New Soodland Iron and Obamium":
                            if "Iron" in epic_items:
                                epic_items["Iron"] += 1
                            else:
                                epic_items.update({"Iron": 1})
                            if "Obamium" in epic_items:
                                epic_items["Obamium"] += 1
                            else:
                                epic_items.update({"Obamium": 1})
                        
                        if cool_land == "New Bob Issues Rare Materials":
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
                        
                        if cool_land == "Southern BOLG Rare Materials":
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
                        
                        if cool_land == "Capital Coal and Obamium":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 1
                            else:
                                epic_items.update({"Coal": 1})
                            if "Iron" in epic_items:
                                epic_items["Iron"] += 1
                            else:
                                epic_items.update({"Iron": 1})
                        
                        if cool_land == "Thaizsanches Coal":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 1
                            else:
                                epic_items.update({"Coal": 1})
                        
                        if cool_land == "BOLG Uranium and Iron":
                            if "Iron" in epic_items:
                                epic_items["Iron"] += 3
                            else:
                                epic_items.update({"Iron": 3})
                            if "Uranium" in epic_items:
                                epic_items["Uranium"] += 3
                            else:
                                epic_items.update({"Uranium": 3})
                        
                        if cool_land == "r/lelcity Oil and Natural Gas":
                            if "Oil" in epic_items:
                                epic_items["Oil"] += 3
                            else:
                                epic_items.update({"Oil": 3})
                            if "Natural Gas" in epic_items:
                                epic_items["Natural Gas"] += 2
                            else:
                                epic_items.update({"Natural Gas": 2})
                        
                        if cool_land == "Breat Gritain Coal":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 1
                            else:
                                epic_items.update({"Coal": 1})
                        
                        if cool_land == "Breat Gritain Wood":
                            if "Wood" in epic_items:
                                epic_items["Wood"] += 1
                            else:
                                epic_items.update({"Wood": 1})
                        
                        if cool_land == "Claps Wood":
                            if "Wood" in epic_items:
                                epic_items["Wood"] += 3
                            else:
                                epic_items.update({"Wood": 3})
                        
                        if cool_land == "New Lelcity Coal":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 1
                            else:
                                epic_items.update({"Coal": 1})
                        
                        if cool_land == "Berkelium Iron and Obamium":
                            if "Iron" in epic_items:
                                epic_items["Iron"] += 2
                            else:
                                epic_items.update({"Iron": 2})
                            if "Obamium" in epic_items:
                                epic_items["Obamium"] += 1
                            else:
                                epic_items.update({"Obamium": 1})
                        
                        if cool_land == "Berkelium Southern Potatos":
                            if "Potatos" in epic_items:
                                epic_items["Potatos"] += 2
                            else:
                                epic_items.update({"Potatos": 2})

                        if cool_land == "Berkelium Northern Potatos":
                            if "Potatos" in epic_items:
                                epic_items["Potatos"] += 3
                            else:
                                epic_items.update({"Potatos": 3})
                        
                        if cool_land == "Berkelium Coal":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 3
                            else:
                                epic_items.update({"Coal": 3})
                        
                        if cool_land == "Desperatetopia Coal":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 1
                            else:
                                epic_items.update({"Coal": 1})
                        
                        if cool_land == "Soodland Coal and Oil":
                            if "Coal" in epic_items:
                                epic_items["Coal"] += 1
                            else:
                                epic_items.update({"Coal": 1})
                            if "Oil" in epic_items:
                                epic_items["Oil"] += 2
                            else:
                                epic_items.update({"Oil": 2})
                        
                        if cool_land == "Poop HQ Agonium and Oil":
                            if "Oil" in epic_items:
                                epic_items["Oil"] += 1
                            else:
                                epic_items.update({"Oil": 1})
                            if "Agonium" in epic_items:
                                epic_items["Agonium"] += 9
                            else:
                                epic_items.update({"Agonium": 9})
                        
                        if cool_land == "Haha Funni City Obamium and Potatos":
                            if "Obamium" in epic_items:
                                epic_items["Obamium"] += 2
                            else:
                                epic_items.update({"Obamium": 2})
                            if "Potatos" in epic_items:
                                epic_items["Potatos"] += 3
                            else:
                                epic_items.update({"Potatos": 3})
                        
                        if cool_land == "Ben State Potatos":
                            if "Potatos" in epic_items:
                                epic_items["Potatos"] += 4
                            else:
                                epic_items.update({"Potatos": 4})

    @commands.Cog.listener()
    async def on_ready(self):
        print("resources cog loaded")
        self.resource_thing.start()

def setup(client: commands.Bot):
    client.add_cog(Resources(client))