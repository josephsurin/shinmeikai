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

        reaction, user = await client.wait_for('reaction_add', check = lambda r,u: u == message.author)
        print(reaction, str(reaction), user, message.author)
        if str(reaction) == '⬅': current_page -= 1
        if str(reaction) == '➡': current_page += 1
        embed = create_page(pages[current_page], search_q, current_page + 1, current_page + 1 + len(pages))
        await msg.edit(embed=embed)

def create_page(page, search_q, page_num, total_pages):
        embed=discord.Embed(description=f'{search_q} (page {page_num} of {total_pages})', color=0x62f7f7)
        embed.set_footer(text=f'use the reaction buttons to see more information!')

        for e in page:
                [kanji, reading, definition] = e
                embed.add_field(name=f'{kanji} ({reading})', value=f'{definition}', inline=False)
                
        return embed