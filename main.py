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
                await commands.handle_reaction_pagination(reaction, search_obj)

        async def on_reaction_remove(self, reaction, user):
                if user == self.user: return
                search_obj = search_cache.get(reaction.message.id)
                await commands.handle_reaction_pagination(reaction, search_obj)

        async def on_message(self, message):
                if message.author == self.user: return

                if re.match(r'^(s|ｓ|ｓ)', message.content): 
                        sres = await commands.search(self, message, smk_dict)
                        if sres:
                                (msgid, search_obj) = sres
                                search_cache[msgid] = search_obj

client = ShinmeikaiClient()
client.run(os.getenv('TOKEN'))