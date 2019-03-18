import discord
from dotenv import load_dotenv
import os
load_dotenv()

from src.dict import init_dict
import src.commands as commands
import re

from expiringdict import ExpiringDict

smk_dict = init_dict()
search_cache = ExpiringDict(max_len=500, max_age_seconds=120)

class ShinmeikaiClient(discord.Client):
        async def on_ready(self):
                print('新明解 started', self.user)

        async def on_reaction_add(self, reaction, user):
                if user == self.user: return
                search_obj = search_cache.get(reaction.message.id)
                if search_obj:
                        if str(reaction.emoji)  == '⬅':
                                await search_obj.go_prev()
                        if str(reaction.emoji) == '➡':
                                await search_obj.go_next()
                

        async def on_message(self, message):
                if message.author == self.user: return

                if re.match(r'^(!s|ｓ|ｓ)', message.content): 
                        (msgid, search_obj) = await commands.search(self, message, smk_dict)
                        search_cache[msgid] = search_obj

client = ShinmeikaiClient()
client.run(os.getenv('TOKEN'))