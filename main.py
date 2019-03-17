import discord
from dotenv import load_dotenv
import os
load_dotenv()

from src.dict import init_dict
import src.commands as commands
import re

smk_dict = init_dict()

class ShinmeikaiClient(discord.Client):
        async def on_ready(self):
                print('新明解 started', self.user)

        async def on_message(self, message):
                if message.author == self.user:
                        return

                if re.match(r'^(!s|ｓ|ｓ)', message.content): 
                        await commands.search(message, smk_dict)

client = ShinmeikaiClient()
client.run(os.getenv('TOKEN'))