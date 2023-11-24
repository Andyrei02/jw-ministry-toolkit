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
		synoplis_list = soup.find_all("div", {"class": "syn-body textOnly accordionHandle"})
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
		return [header_title.text, header_verses.text]

	def get_section_list(self, soup):
		body = soup.find("div", {"class": "bodyTxt"})
		return body.find_all("div", {"class": "section"})

	def get_data_list_section_1(self, soup):
		row_list = []
		pGroup = soup.find("div", {"class": "pGroup"})
		li_list = pGroup.find_all("li")
		for li in li_list:
			p_tag = li.find("p")

			time = self.find_time_from_p_tag(p_tag)
			strong_text = p_tag.find("strong").text
			row_list.append([time, strong_text])

		return row_list

	def get_data_list_section_2(self, soup):
		title = soup.find("div", {"class": "mwbHeadingIcon"}).text
		print(title)

		row_list = []
		pGroup = soup.find("div", {"class": "pGroup"})
		ul = pGroup.find("ul")
		li_list = ul.find_all("li", recursive=False)
		for li in li_list:
			p_tag = li.find("p")

			time = self.find_time_from_p_tag(p_tag)
			strong_texts = [p_tag.get_text()]

			strong_text = ' '.join(strong_texts)
			row_list.append([time, strong_text])


		return row_list

	def get_data_list_section_3(self, soup):
		title = soup.find("div", {"class": "mwbHeadingIcon"}).text

		row_list = []
		pGroup = soup.find("div", {"class": "pGroup"})
		ul = pGroup.find("ul")
		li_list = ul.find_all("li", recursive=False)
		for li in li_list:
			p_tag = li.find("p")
			print(p_tag.get_text())
			
			time = self.find_time_from_p_tag(p_tag)
			strong_texts = p_tag.get_text()#[strong.get_text() for strong in p_tag.find_all('strong', recursive=True)]
			strong_text = ' '.join(strong_texts)
			row_list.append([time, strong_text])

		return row_list

	def get_data_list_section_4(self, soup):
		title = soup.find("div", {"class": "mwbHeadingIcon"}).text

		row_list = []
		pGroup = soup.find("div", {"class": "pGroup"})
		ul = pGroup.find("ul")
		li_list = ul.find_all("li", recursive=False)
		for li in li_list:
			p_tag = li.find("p")
			
			time = self.find_time_from_p_tag(p_tag)
			strong_texts = [strong.get_text() for strong in p_tag.find_all('strong', recursive=True)]
			strong_text = ' '.join(strong_texts)
			row_list.append([time, strong_text])

		return row_list

	def find_time_from_p_tag(self, p_tag):
		text = p_tag.get_text()
		match = re.search(r'\((\d+)\s+min\.\)', text)
		if match:
			time_str = match.group(1)
			return int(time_str)
		return 0

	def download_page(self, page):
		url = self.domain + page[1]
		
		soup = self.get_site_page(url)
		soup_article = self.get_article(soup)
		section_list = self.get_section_list(soup_article)
		date, header = self.get_article_header(soup_article)
		
		intro = {}
		for item in self.get_data_list_section_1(section_list[0]):
			intro[item[1]] = [item[0], '']

		section_1 = {}
		for item in self.get_data_list_section_2(section_list[1]):
			section_1[item[1]] = [item[0], '']

		section_2 = {}
		for item in self.get_data_list_section_3(section_list[2]):
			section_2[item[1]] = [item[0], '']

		section_3 = {}
		for item in self.get_data_list_section_4(section_list[3]):
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


if __name__ == "__main__":
	p = Parse_Meeting_WorkBook('https://www.jw.org', 'https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire/noiembrie-decembrie-2023-mwb')

	p.download_page(['', "/ro/biblioteca/caiet-pentru-intrunire/noiembrie-decembrie-2023-mwb/Programul-%C3%AEntrunirii-Via%C8%9Ba-cre%C8%99tin%C4%83-%C8%99i-predicarea-6-12-noiembrie-2023/"])

