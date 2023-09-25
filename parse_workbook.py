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

	def get_data_list_section_3(self, soup):
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

	def get_dict_data(self):
		page_list = self.get_pages_list()
		total_pages = len(page_list)
		downloaded_pages = 0

		data_dict = {}

		for page in page_list:
			url = self.domain + page[1]

			soup = self.get_site_page(url)
			soup_article = self.get_article(soup)
			section_list = self.get_section_list(soup_article)

			# Add date in dict:
			date, header = self.get_article_header(soup_article)

			intro = {}
			for item in self.get_data_list_section_1(section_list[0]):
				intro[item[1]] = [item[0]]

			section_1 = {}
			for item in self.get_data_list_section_2(section_list[1]):
				section_1[item[1]] = [item[0]]

			section_2 = {}
			for item in self.get_data_list_section_3(section_list[2]):
				section_2[item[1]] = [item[0]]

			section_3 = {}
			for item in self.get_data_list_section_4(section_list[3]):
				section_3[item[1]] = [item[0]]

			data_dict[date] = {"header": {header: [0]}, "intro": intro, "section_1": section_1, "section_2": section_2, "section_3": section_3}

			downloaded_pages += 1
			downloaded_progress = int((downloaded_pages / total_pages) * 100)
			self.download_progress_signal.emit(downloaded_progress)

		return data_dict
