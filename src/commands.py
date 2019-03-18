import discord
import time
from functools import reduce
from src.dict import dict_search

async def search(client, message, smk_dict):
        search_q = message.content.split()[1]

        start = time.time()
        matches = dict_search(search_q, smk_dict)
        end = time.time()
        dur = end - start
        print(f'found {len(matches)} words in {dur} seconds')

        pages = [[matches[0]]]
        current_page = 0
        for i in range(1, len(matches)):
                if(reduce(lambda acc, v: acc + len(v[2]), pages[-1], 0) + len(matches[i][2]) < 200):
                        pages[-1].append(matches[i])
                else:
                        pages.append([matches[i]])

        embed = create_page(pages[current_page], search_q, current_page + 1, current_page + 1 + len(pages))

        msg = await message.channel.send(embed=embed)

        await msg.add_reaction('⬅')
        await msg.add_reaction('➡')

        return (msg.id, SearchObj(pages, search_q, msg))

class SearchObj:
        def __init__(self, pages, search_q, msg):
                self.pages = pages
                self.msg = msg
                self.search_q = search_q
                self.current_page = 0

        async def go_next(self):
                if self.current_page == len(self.pages): return
                self.current_page += 1
                embed = create_page(self.pages[self.current_page], self.search_q, self.current_page + 1, len(self.pages) + 1)
                await self.msg.edit(embed=embed)

        async def go_prev(self):
                if self.current_page == 0: return
                self.current_page -= 1
                embed = create_page(self.pages[self.current_page], self.search_q, self.current_page + 1, len(self.pages) + 1)
                await self.msg.edit(embed=embed)

def create_page(page, search_q, page_num, total_pages):
        embed=discord.Embed(description=f'{search_q} (page {page_num} of {total_pages})', color=0x62f7f7)
        embed.set_footer(text=f'use the reaction buttons to see more information!')

        for e in page:
                [kanji, reading, definition] = e
                embed.add_field(name=f'{kanji} ({reading})', value=f'{definition}', inline=False)
                
        return embed