import time
from src.dict import dict_search

async def search(message, smk_dict):
        search_q = message.content.split()[1]

        start = time.time()
        matches = dict_search(search_q, smk_dict)
        end = time.time()
        dur = end - start
        print(f'found {len(matches)} words in {dur} seconds')
        await message.channel.send(str(matches)[:2000]) #need to format into embed