#!/usr/bin/env python3

from modules.connections import bot_token as bot_token
from modules.connections import database_file as database_file
from discord.ext import commands
import sys
import os
import aiosqlite
import sqlite3

from modules import first_run

user_extensions_directory = "user_extensions"
bridged_extensions_directory = "bridged_extensions"

if not os.path.exists("data"):
    print("Please configure this bot according to readme file.")
    sys.exit("data folder and it's contents are missing")
if not os.path.exists(user_extensions_directory):
    os.makedirs(user_extensions_directory)
if not os.path.exists(bridged_extensions_directory):
    os.makedirs(bridged_extensions_directory)

if os.environ.get('MOMIJI_PREFIX'):
    command_prefix = os.environ.get('MOMIJI_PREFIX')
else:
    command_prefix = ";"

first_run.create_tables()

initial_extensions = [
    "cogs.AIMod",
    "cogs.BotManagement",
    "cogs.ChannelExporting", 
    "cogs.COVID19",
    "cogs.CRPair",
    "cogs.Fun",
    "cogs.Img",
    "cogs.InspiroBot", 
    "cogs.MessageStats", 
    "cogs.Misc",
    "cogs.GoodbyeMessage",
    "cogs.Moderation", 
    "cogs.MomijiChannelImporting", 
    "cogs.MomijiCommands", 
    "cogs.MomijiSpeak", 
    "cogs.Music", 
    "cogs.Pinning", 
    "cogs.RegularRole",
    "cogs.RSSFeed",
    "cogs.SelfAssignableRoles",
    "cogs.StatsBuilder", 
    "cogs.TraceMoe",
    "cogs.Utilities",
    "cogs.VoiceLogging",
    "cogs.VoiceRoles", 
    "cogs.Waifu",
    "cogs.Wasteland",
    "cogs.WastelandConfiguration",
    "cogs.WelcomeMessage",
]


class Momiji(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_tasks = []
        self.app_version = (open(".version", "r+").read()).strip()
        self.description = f"Momiji {self.app_version}"
        self.database_file = database_file

        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()
        self.bridged_extensions = tuple(c.execute("SELECT extension_name FROM bridged_extensions"))
        conn.close()

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(e)
        for bridged_extension in self.bridged_extensions:
            try:
                self.load_extension(f"{bridged_extensions_directory}.{bridged_extension[0]}")
                print(f"Bridged extension {bridged_extension[0]} loaded")
            except Exception as e:
                print(e)
        for user_extension in os.listdir(user_extensions_directory):
            if not user_extension.endswith(".py"):
                continue
            extension_name = user_extension.replace(".py", "")
            try:
                self.load_extension(f"{user_extensions_directory}.{extension_name}")
                print(f"User extension {extension_name} loaded")
            except Exception as e:
                print(e)

    async def start(self, *args, **kwargs):
        self.db = await aiosqlite.connect(self.database_file)

        await super().start(*args, **kwargs)

    async def close(self):
        # Cancel all Task object generated by cogs.
        # This prevents any task still running due to having long sleep time.
        for task in self.background_tasks:
            task.cancel()

        # Close connection to the database
        await self.db.close()

        # Run actual discord.py close.
        await super().close()

    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")
        await first_run.add_admins(self)


client = Momiji(command_prefix=command_prefix)
client.run(bot_token)
