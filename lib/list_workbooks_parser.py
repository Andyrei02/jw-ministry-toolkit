import logging

import aiohttp
import asyncio
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Parse_List_Meeting_WorkBooks:
    def __init__(self, domain, url):
        super().__init__()
        self.domain = domain
        self.site_url = url

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_site_page(self, session, url):
        html = await self.fetch(session, url)
        return BeautifulSoup(html, "lxml")

    async def get_article(self, soup):
        article = soup.find("article", {"id": "article"})
        return article

    async def get_synopsis_list(self, soup):
        section = soup.find("div", {"id": "pubsViewResults"})
        divs = section.find_all("div", {"class": "synopsis"})
        return divs

    async def get_syn_img(self, div):
        syn_img = div.find("div", {"class": "syn-img"})
        img = syn_img.find("img")['src']
        return img

    async def get_byte_img(self, session, url):
        async with session.get(url) as response:
            return await response.read()

    async def get_syn_body(self, div):
        syn_body = div.find("div", {"class": "syn-body"})
        pub_desc = syn_body.find("div", {"class": "publicationDesc"})
        title = pub_desc.find("h3").text
        link = pub_desc.find("a")['href']
        return [title.strip(), link]

    async def get_dict_data(self):
        data_dict = {}
        logging.info(f"Parse Workbook list: {self.site_url}\n")
        async with aiohttp.ClientSession() as session:
            soup = await self.get_site_page(session, self.site_url)
            syn_list = await self.get_synopsis_list(soup)

            for publication in syn_list:
                try:
                    syn_img_link = await self.get_syn_img(publication)
                    syn_img_byte = await self.get_byte_img(session, syn_img_link)
                    title, link = await self.get_syn_body(publication)
                    data_dict[title] = [self.domain+link, syn_img_byte]
                except:
                    pass
        logging.info(f"Successfully Parsed Workbook list: {self.site_url}\n")

        return data_dict
