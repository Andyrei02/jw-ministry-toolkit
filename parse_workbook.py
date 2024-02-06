import concurrent.futures
from datetime import datetime

import requests
import re
from bs4 import BeautifulSoup
from PyQt5.QtCore import pyqtSignal, QObject


class Parse_Meeting_WorkBook(QObject):
    download_progress_signal = pyqtSignal(int)

    def __init__(self, domain, url):
        super().__init__()
        self.domain = domain
        self.site_url = url

    def get_site_page(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "lxml")

    def get_article(self, soup):
        article = soup.find("article", {"id": "article"})
        return article

    def get_synopsis_list(self, soup):
        synoplis_list = soup.find_all("div", {"class": "syn-body sqs"})
        return synoplis_list

    def get_date_and_link_list(self, soup):
        date_link_list = []
        for synopsis in soup:
            date_link_list.append([(synopsis.find("a").text).strip(), synopsis.find("a")['href']])
        return date_link_list

    def get_pages_list(self):
        soup = self.get_site_page(self.site_url)
        soup_article = self.get_article(soup)
        synopsis_list = self.get_synopsis_list(soup_article)
        date_link_list = self.get_date_and_link_list(synopsis_list)
        return date_link_list

    def get_article_header(self, soup):
        header = soup.find("header")
        header_title = header.find("h1", {"id": "p1"})
        header_verses = header.find("h2", {"id": "p2"})
        return [header_title.text.strip(), header_verses.text.strip()]

    def get_section_list(self, soup):
        body = soup.find("div", {"class": "bodyTxt"})

        # Music list:
        dc_music = body.find_all("h3", {"class": "dc-icon--music"})
        dc_music.append(body.find("span", {"class": "dc-icon--music"}))
        dc_music = [i.text for i in dc_music]

        # Section 1
        # section 1 Text
        section_1_text = body.find("div", {"class": "dc-icon--gem"})
        # items
        s1_items = body.find_all("h3", {"class": "du-color--teal-700"}, recursive=True)
        s1_items = [i.text for i in s1_items]

        # Section 2
        section_2_text = body.find("div", {"class": "dc-icon--wheat"})
        # items
        s2_items = body.find_all("h3", {"class": "du-color--gold-700"})
        s2_items = [i.text for i in s2_items]

        # Section 3
        section_3_text = body.find("div", {"class": "dc-icon--sheep"})
        # items
        s3_items = body.find_all("h3", {"class": "du-color--maroon-600"})
        s3_items = [i.text for i in  s3_items]

        return body

    def increment_id(self, id_value):
        match = re.match(r'\D*(\d+)', id_value)

        if match:
            numeric_part = int(match.group(1))
            modified_id = f'p{numeric_part + 1}'
            return modified_id
        else:
            return None

    def get_data_list_section_1(self, soup):
        dc_music = soup.find("h3", {"class": "dc-icon--music"})
        dc_music = dc_music.text.split('|')
        intro_text = dc_music[1].strip()
        time = self.find_time_from_p_tag(intro_text)
        pattern = r'\(\d+\xa0min\.\)'
        format_intro = re.sub(pattern, '', intro_text)

        row_list = [["5", dc_music[0].strip()], [str(time), format_intro]]

        return row_list

    def get_data_list_section_2(self, soup):
        section_1_text = soup.find("div", {"class": "dc-icon--gem"})
        title = section_1_text.text
        # items
        s1_items = soup.find_all("h3", {"class": "du-color--teal-700"}, recursive=True)
        row_list = []
        for i in s1_items:
            current_id = i.get('id')
            time = soup.find('p', {'id': self.increment_id(current_id)})
            time = self.find_time_from_p_tag(time)
            row_list.append([str(time), i.text.strip()])

        return row_list

    def get_data_list_section_3(self, soup):
        section_2_text = soup.find("div", {"class": "dc-icon--wheat"})
        title = section_2_text.text
        # items
        s2_items = soup.find_all("h3", {"class": "du-color--gold-700"})
        row_list = []
        for i in s2_items:
            current_id = i.get('id')
            time = soup.find('p', {'id': self.increment_id(current_id)})
            time = self.find_time_from_p_tag(time)
            row_list.append([str(time), i.text.strip()])

        return row_list

    def get_data_list_section_4(self, soup):
        dc_music = soup.find_all("h3", {"class": "dc-icon--music"})
        dc_music.append(soup.find("span", {"class": "dc-icon--music"}))

        section_3_text = soup.find("div", {"class": "dc-icon--sheep"})
        title = section_3_text.text
        # items
        s3_items = soup.find_all("h3", {"class": "du-color--maroon-600"})
        row_list = []
        row_list.append(["5", dc_music[1].text])
        for i in s3_items:
            current_id = i.get('id')
            time = soup.find('p', {'id': self.increment_id(current_id)})
            time = self.find_time_from_p_tag(time)
            row_list.append([str(time), i.text.strip()])

        row_list.append(["5", "Cuvinte de încheiere"])
        row_list.append(["5", dc_music[2].text])
        return row_list

    def find_time_from_p_tag(self, text):
        if type(text) != str:
            text = text.get_text()
        match = re.search(r'\((\d+)\s+min\.\)', text)
        if match:
            time_str = match.group(1)
            return int(time_str)
        return 0

    def download_page(self, page):
        url = self.domain + page[1]
        soup = self.get_site_page(url)
        soup_article = self.get_article(soup)
        body = self.get_section_list(soup_article)
        date, header = self.get_article_header(soup_article)

        intro = {}
        for item in self.get_data_list_section_1(body):
            intro[item[1]] = [item[0], '']

        section_1 = {}
        for item in self.get_data_list_section_2(body):
            section_1[item[1]] = [item[0], '']

        section_2 = {}
        for item in self.get_data_list_section_3(body):
            section_2[item[1]] = [item[0], '']

        section_3 = {}
        for item in self.get_data_list_section_4(body):
            section_3[item[1]] = [item[0], '']

        return date, {"header": {header: [0, '']}, "intro": intro, "section_1": section_1, "section_2": section_2, "section_3": section_3}

    def sort_dict_by_dates(self, date_dict):
        def convert_month_to_number(month_word):
            month_mapping = {
                'ianuarie': '01',
                'februarie': '02',
                'martie': '03',
                'aprilie': '04',
                'mai': '05',
                'iunie': '06',
                'iulie': '07',
                'august': '08',
                'septembrie': '09',
                'octombrie': '10',
                'noiembrie': '11',
                'decembrie': '12'
            }
            return month_mapping.get(month_word, '00')

        def custom_sort(date_str):
            date_parts = date_str.split(' ')
            day, month_word = date_parts[:2]
            day = day.split('-')[0]
            month = convert_month_to_number(month_word)
            return datetime.strptime(f'{day}.{month}', '%d.%m').date()

        sorted_items = dict(sorted(date_dict.items(), key=lambda item: custom_sort(item[0])))
        return sorted_items
        
    def get_dict_data(self):
        page_list = self.get_pages_list()
        total_pages = len(page_list)
        downloaded_pages = 0
        data_dict = {}

        # Use ThreadPoolExecutor for concurrent downloads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Download pages concurrently
            future_to_page = {executor.submit(self.download_page, page): page for page in page_list}
            for future in concurrent.futures.as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    date, page_data = future.result()
                    data_dict[date] = page_data
                except Exception as e:
                    print(f"Error downloading page {page}: {e}")

                downloaded_pages += 1
                downloaded_progress = int((downloaded_pages / total_pages) * 100)
                self.download_progress_signal.emit(downloaded_progress)

        return self.sort_dict_by_dates(data_dict)
