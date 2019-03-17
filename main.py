import discord
from dotenv import load_dotenv
import os
load_dotenv()

from src.dict import init_dict, dict_search
import time
import re

smk_dict = init_dict()

class ShinmeikaiClient(discord.Client):
        async def on_ready(self):
                print('新明解 started', self.user)

        async def on_message(self, message):
                if message.author == self.user:
                        return

                if re.match(r'^(!s|ｓ|ｓ)', message.content): 
                        search_q = message.content.split()[1]

                        start = time.time()
                        matches = dict_search(search_q, smk_dict)
                        end = time.time()
                        dur = end - start
                        print(f'found {len(matches)} words in {dur} seconds')
                        await message.channel.send(str(matches)[:2000])

client = ShinmeikaiClient()
client.run(os.getenv('TOKEN'))