import discord
import time
from functools import reduce
from src.dict import dict_search
from src.util import is_kana
from romkan import to_hiragana

async def search(client, message, smk_dict):
        search_q = message.content.split()[1]
        if not is_kana(search_q[0]):
            search_q = to_hiragana(search_q)
        start = time.time()
        matches = dict_search(search_q, smk_dict)
        end = time.time()
        dur = end - start
        print(f'found {len(matches)} words in {dur} seconds')

        if len(matches) == 0:
                embed=discord.Embed(description=f'No results found for **{search_q}**!', color=0x62f7f7)
                await message.channel.send(embed=embed)
                return None

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
                if self.current_page == len(self.pages)-1: return
                self.current_page += 1
                embed = create_page(self.pages[self.current_page], self.search_q, self.current_page + 1, len(self.pages))
                await self.msg.edit(embed=embed)

        async def go_prev(self):
                if self.current_page == 0: return
                self.current_page -= 1
                embed = create_page(self.pages[self.current_page], self.search_q, self.current_page + 1, len(self.pages))
                await self.msg.edit(embed=embed)

def create_page(page, search_q, page_num, total_pages):
        embed=discord.Embed(description=f'{search_q} (page {page_num} of {total_pages})', color=0x62f7f7)
        embed.set_footer(text=f'use the reaction buttons to see more information!')

        for e in page:
                [kanji, reading, definition] = e
                embed.add_field(name=f'{kanji} ({reading})', value=f'{definition}', inline=False)
                
        return embed

async def handle_reaction_pagination(reaction, search_obj):
        if search_obj:
                if str(reaction.emoji)  == '⬅':
                        await search_obj.go_prev()
                if str(reaction.emoji) == '➡':
                        await search_obj.go_next()

async def chart(client, message):
        await message.channel.send(file=discord.File('./src/assets/pitch_accent_chart.png'))

from selenium import webdriver
from PIL import Image
from random import getrandbits
from dotenv import load_dotenv
import os
load_dotenv()

async def ojad_index(client, message):
    search_q = message.content.split()[1]
    if not is_kana(search_q[0]):
        search_q = to_hiragana(search_q)
 
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("headless")
    options.add_argument('--lang=ja')
    options.add_argument("window-size=1600x1000")
    options.binary_location = os.getenv('CHROME_BIN')
    driver = webdriver.Chrome(options=options, executable_path=os.getenv('CHROMEDRIVER_PATH'))
     
    driver.get('http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/display:print/sortprefix:accent/narabi1:kata_asc/narabi2:accent_asc/narabi3:mola_asc/yure:visible/curve:invisible/details:invisible/limit:20/word:'+search_q)

    element = driver.find_element_by_xpath("//table[@id='word_table']");

    location = element.location;
    size = element.size;
    
    img_filename = 'tmp/' + str(getrandbits(32)) + '.png'

    driver.save_screenshot(img_filename);

    driver.close()

    x = location['x'];
    y = location['y'];
    width = location['x']+size['width'];
    height = location['y']+size['height'];
    im = Image.open(img_filename)
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(img_filename)
    print('saved image to', img_filename)

    await message.channel.send(file=discord.File(img_filename))

    os.remove(img_filename)
