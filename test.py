import os
from datetime import datetime, timedelta

import requests
import re
from bs4 import BeautifulSoup
# from tqdm import tqdm

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.pdfmetrics import stringWidth

class Service_Schedule_PDF_Generator:
	def __init__(self, output_path, congregation, data_dict):
		self.congregation = congregation
		self.data_dict = data_dict
		self.inv_canvas = canvas.Canvas(output_path, pagesize=A4, bottomup=0)
		self.init_pdf()

	def init_pdf(self):
		pdfmetrics.registerFont(TTFont('CalibriRegular', '/home/andreic/Documents/Congregatie/jw-ministry-toolkit/assets/font/Calibri Regular.ttf'))
		pdfmetrics.registerFont(TTFont('CalibriBold', '/home/andreic/Documents/Congregatie/jw-ministry-toolkit/assets/font/Calibri Bold.TTF'))
		pdfmetrics.registerFont(TTFont('CambriaBold', '/home/andreic/Documents/Congregatie/jw-ministry-toolkit/assets/font/Cambria-Bold.ttf'))

		self.GRAY = (86/255,86/255,86/255)
		self.BLACK = (0,0,0)
		self.WHITE = (1,1,1)
		self.YELLOW = (190/255,137/255,0)
		self.RED = (136/255,0,36/255)

		self.text_margins = (1*cm, A4[0]-(1*cm), 1*cm, A4[1])
		self.content_pos = (self.text_margins[0], self.text_margins[2]+(1.5*cm))

	def add_minutes_to_time(self, time_str, minutes_to_add):
		time_format = "%H:%M"
		time_obj = datetime.strptime(time_str, time_format)
		new_time_obj = time_obj + timedelta(minutes=minutes_to_add)
		new_time_str = new_time_obj.strftime(time_format)

		return new_time_str

	def draw_header(self):
		image_filename = "assets/image/img.jpg"  # Replace with your image file
		self.inv_canvas.drawImage(image_filename, 0, 0, width=A4[0], height=A4[1])

		left_text = self.congregation
		self.inv_canvas.setFont("CalibriBold", 11)

		# Draw congregation name
		self.inv_canvas.drawString(self.text_margins[0], self.text_margins[2]+5, left_text)
		
		# Draw title page
		right_text = 'Planificarea întrunirii din timpul săptămânii' 
		x_right_text = self.text_margins[1] - stringWidth(right_text, 'CambriaBold', 16)
		self.inv_canvas.setFont("CambriaBold", 16)
		self.inv_canvas.drawString(x_right_text, self.text_margins[2]+5, right_text)

		self.inv_canvas.line(self.text_margins[0]-5, self.text_margins[2]+11, self.text_margins[1]+5, self.text_margins[2]+11)

	def draw_content(self, header_date):
		current_row = 0
		row_height = 15
		section_title_height = 30
		center_content_x = self.text_margins[1]/2
		column_two_comment_x = self.text_margins[1] - self.content_pos[0] - 150


		start_hour = '18:00'

		
		# section_0_items = [('', '4-10 septembrie | ESTERA 1, 2', 'Președinte:', ''), ('5', 'Cântarea 137', 'Rugăciune', 'Bodiu Ruslan'), ('5', 'Cuvinte introductive:', '', 'Bodiu Ruslan')]
		# date  = '4-10 septembrie'
		# verses = 'ESTERA 1, 2'
		# chairman = ''
		# prayer_1 = 'Bodiu Ruslan'
		# intro_reader = 'Bodiu Ruslan'

		# section_1_items = [('10', 'Străduiește-te să fii modest la fel ca Estera', '', 'Bodiu Ruslan'), ('10', 'Să căutăm nestemate spirituale:', '', 'Moldovanu Vasile'), ('4', 'Citirea Bibliei', 'Cursant:', 'Bogdan Șaban')]
		# section_1_title = 'Străduiește-te să fii modest la fel ca Estera'
		# title_of_1_section_reader = 'Bodiu Ruslan'
		# spiritual_gems_reader = 'Moldovanu Vasile'
		# bible_reader = 'Bogdan Șaban'

		# section_2_items = [('5', 'Vizita inițială – Material video:', '', ''), ('3', 'Vizita inițială:', '', 'Mardarovici Elena/Cevali Iraida'), ('5', 'Cuvântare: th 14', '', 'Pasăre Vasile')]
		# section_2_title_1 = 'Vizita inițială – Material video:'
		# section_2_title_1_coursant = ''
		# section_2_title_2 = 'Vizita inițială:'
		# section_2_title_2_coursant = 'Mardarovici Elena/Cevali Iraida'
		# section_2_title_3 = 'Cuvântare: th 14'
		# section_2_title_3_coursant = 'Pasăre Vasile'

		# section_3_items = [('2', 'Cântarea 106', '', ''), ('5', 'Ce spun alți tineri – Înfățișare:', '', 'Moldovanu Vasile'), ('10', 'Realizări organizatorice:', '', 'Bodiu Ruslan'), ('30', 'Studiul Bibliei în congregație: lff lecția 56', 'Conducător/Cititor', 'Russu Petru/Spoială Leonid'), ('3', 'Cuvinte de încheiere (3 min.)', '', ''), ('0', 'Cântarea 101', 'Rugăciune:', 'Moldovanu Vasile')]

		# song_1 = '123'
		# song_2 = '101'
		# song_3 = '127'

		header_dict = self.data_dict[header_date]["header"]
		intro_dict = self.data_dict[header_date]["intro"]
		section_1_dict = self.data_dict[header_date]["section_1"]
		section_2_dict = self.data_dict[header_date]["section_2"]
		section_3_dict = self.data_dict[header_date]["section_3"]


		current_hour = start_hour
		hour_pos_x = 0
		subtitle_pos_x = 40

		# Header Row 0
		# ===============================================
		self.inv_canvas.setFont("CalibriBold", 11)
		header_verse = list(header_dict.keys())[0]
		header_content = f'{header_date} | {header_verse}'
		self.inv_canvas.drawString(0, current_row, header_content)

		self.inv_canvas.setFont("CalibriBold", 8)
		x_comment = column_two_comment_x - stringWidth(header_dict[header_verse][1], 'CalibriBold', 8)
		self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(x_comment, current_row, list_section0[0][2])

		x_name = column_two_comment_x + 10
		self.inv_canvas.setFillColorRGB(*self.BLACK)
		self.inv_canvas.setFont("CalibriBold", 11)
		self.inv_canvas.drawString(x_name, current_row, header_dict[header_verse][1])
		current_row += row_height

		#  Intro
		# ===============================================
		intro_keys = list(intro_dict.keys())
		for key in intro_keys:
			self.inv_canvas.setFont("CalibriBold", 9)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(0, current_row, current_hour)

			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

			self.inv_canvas.setFont("CalibriRegular", 11)
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

			self.inv_canvas.setFont("CalibriBold", 8)
			x_comment = column_two_comment_x - stringWidth(intro_dict[key][1], 'CalibriBold', 8)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(x_comment, current_row, intro_dict[key][1])

			x_name = column_two_comment_x + 10
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.setFont("CalibriBold", 11)
			self.inv_canvas.drawString(x_name, current_row, intro_dict[key][1])
			next_hour = int(intro_dict[key][0]) if int(intro_dict[key][0]) != 0 else 5
			current_hour = self.add_minutes_to_time(current_hour, next_hour)
			current_row += row_height
		current_row += section_title_height - row_height



		# self.inv_canvas.setFont("CalibriBold", 9)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(0, current_row, current_hour)

		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)

		# self.inv_canvas.drawString(subtitle_pos_x, current_row, list_section0[1][1])

		# self.inv_canvas.setFont("CalibriBold", 8)
		# x_comment = column_two_comment_x - stringWidth(list_section0[1][2], 'CalibriBold', 8)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(x_comment, current_row, list_section0[1][2])

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, list_section0[1][3])
		# current_hour = self.add_minutes_to_time(current_hour, int(list_section0[1][0]))
		# current_row += row_height

		# # Header Row 2
		# # ===============================================
		# self.inv_canvas.setFont("CalibriBold", 9)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(0, current_row, current_hour)

		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.drawString(subtitle_pos_x, current_row, list_section0[2][1])

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, list_section0[2][3])
		# current_hour = self.add_minutes_to_time(current_hour, int(list_section0[2][0]))
		# current_row += section_title_height


		# Section 1 Row 0
		# ===============================================
		self.inv_canvas.setFillColorRGB(*self.GRAY)
		self.inv_canvas.roundRect(-10, current_row, center_content_x, -15, 3, stroke=0, fill=1)
		self.inv_canvas.setFont("CalibriBold", 10)
		self.inv_canvas.setFillColorRGB(*self.WHITE)
		self.inv_canvas.drawString(0, current_row-4, f'COMORI DIN CUVÂNTUL LUI DUMNEZEU')
		current_row += row_height

		# # Section 1 Row 1
		# # ===============================================
		# self.inv_canvas.setFont("CalibriBold", 9)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(0, current_row, current_hour)

		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.drawString(subtitle_pos_x, current_row, f'{section_1_title}: (10 min.)')

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, title_of_1_section_reader)
		# current_hour = self.add_minutes_to_time(current_hour, 10)
		# current_row += row_height

		# # Section 1 Row 2
		# # ===============================================
		# self.inv_canvas.setFont("CalibriBold", 9)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(0, current_row, current_hour)

		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.drawString(subtitle_pos_x, current_row, 'Să căutăm nestemate spirituale: (10 min.)')

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, spiritual_gems_reader)
		# current_hour = self.add_minutes_to_time(current_hour, 8)
		# current_row += row_height

		# # Section 1 Row 3
		# # ===============================================
		# self.inv_canvas.setFont("CalibriBold", 9)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(0, current_row, current_hour)

		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.drawString(subtitle_pos_x, current_row, 'Citirea Bibliei: (cel mult 4 min.)')

		# self.inv_canvas.setFont("CalibriBold", 8)
		# x_comment = column_two_comment_x - stringWidth('Cursant:', 'CalibriBold', 8)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(x_comment, current_row, 'Cursant:')

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, bible_reader)
		# current_hour = self.add_minutes_to_time(current_hour, 5)
		# current_row += section_title_height

		section_1_keys = list(section_1_dict.keys())
		for key in section_1_keys:
			self.inv_canvas.setFont("CalibriBold", 9)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(0, current_row, current_hour)

			self.inv_canvas.setFillColorRGB(*self.RED)
			self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

			self.inv_canvas.setFont("CalibriRegular", 11)
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

			self.inv_canvas.setFont("CalibriBold", 8)
			x_comment = column_two_comment_x - stringWidth(section_1_dict[key][1], 'CalibriBold', 8)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(x_comment, current_row, section_1_dict[key][1])

			x_name = column_two_comment_x + 10
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.setFont("CalibriBold", 11)
			self.inv_canvas.drawString(x_name, current_row, section_1_dict[key][1])
			current_hour = self.add_minutes_to_time(current_hour, int(section_1_dict[key][0]))
			current_row += row_height
		current_row += section_title_height - row_height


		# Section 2 Row 0
		# ===============================================
		self.inv_canvas.setFillColorRGB(*self.YELLOW)
		self.inv_canvas.roundRect(-10, current_row, center_content_x, -15, 3, stroke=0, fill=1)
		self.inv_canvas.setFont("CalibriBold", 10)
		self.inv_canvas.setFillColorRGB(*self.WHITE)
		self.inv_canvas.drawString(0, current_row-4, f'SĂ FIM MAI EFICIENȚI ÎN PREDICARE')
		current_row += row_height

		# # Section 2 Row 1
		# # ===============================================
		# self.inv_canvas.setFont("CalibriBold", 9)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(0, current_row, current_hour)

		# self.inv_canvas.setFillColorRGB(*self.YELLOW)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.drawString(subtitle_pos_x, current_row, f'{section_2_title_1}')

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, section_2_title_1_coursant)
		# current_hour = self.add_minutes_to_time(current_hour, 10)
		# current_row += row_height

		# # Section 2 Row 2
		# # ===============================================
		# self.inv_canvas.setFillColorRGB(*self.YELLOW)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.drawString(subtitle_pos_x, current_row, f'{section_2_title_2}')

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, section_2_title_2_coursant)
		# current_row += row_height

		# # Section 2 Row 3
		# # ===============================================
		# self.inv_canvas.setFont("CalibriBold", 9)
		# self.inv_canvas.setFillColorRGB(*self.GRAY)
		# self.inv_canvas.drawString(0, current_row, current_hour)

		# self.inv_canvas.setFillColorRGB(*self.YELLOW)
		# self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

		# self.inv_canvas.setFont("CalibriRegular", 11)
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.drawString(subtitle_pos_x, current_row, f'{section_2_title_3}')

		# x_name = column_two_comment_x + 10
		# self.inv_canvas.setFillColorRGB(*self.BLACK)
		# self.inv_canvas.setFont("CalibriBold", 11)
		# self.inv_canvas.drawString(x_name, current_row, section_2_title_3_coursant)
		# current_hour = self.add_minutes_to_time(current_hour, 5)
		# current_row += section_title_height

		section_2_keys = list(section_2_dict.keys())
		for key in section_2_keys:
			self.inv_canvas.setFont("CalibriBold", 9)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(0, current_row, current_hour)

			self.inv_canvas.setFillColorRGB(*self.RED)
			self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

			self.inv_canvas.setFont("CalibriRegular", 11)
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

			self.inv_canvas.setFont("CalibriBold", 8)
			x_comment = column_two_comment_x - stringWidth(section_2_dict[key][1], 'CalibriBold', 8)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(x_comment, current_row, section_2_dict[key][1])

			x_name = column_two_comment_x + 10
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.setFont("CalibriBold", 11)
			self.inv_canvas.drawString(x_name, current_row, section_2_dict[key][1])
			current_hour = self.add_minutes_to_time(current_hour, int(section_2_dict[key][0]))
			current_row += row_height
		current_row += section_title_height - row_height


		# Section 3 Row 0
		# ===============================================
		self.inv_canvas.setFillColorRGB(*self.RED)
		self.inv_canvas.roundRect(-10, current_row, center_content_x, -15, 3, stroke=0, fill=1)
		self.inv_canvas.setFont("CalibriBold", 10)
		self.inv_canvas.setFillColorRGB(*self.WHITE)
		self.inv_canvas.drawString(0, current_row-4, f'VIAȚA DE CREȘTIN')
		current_row += row_height

		section_3_keys = list(section_3_dict.keys())
		for key in section_3_keys:
			self.inv_canvas.setFont("CalibriBold", 9)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(0, current_row, current_hour)

			self.inv_canvas.setFillColorRGB(*self.RED)
			self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

			self.inv_canvas.setFont("CalibriRegular", 11)
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

			self.inv_canvas.setFont("CalibriBold", 8)
			x_comment = column_two_comment_x - stringWidth(section_3_dict[key][1], 'CalibriBold', 8)
			self.inv_canvas.setFillColorRGB(*self.GRAY)
			self.inv_canvas.drawString(x_comment, current_row, section_3_dict[key][1])

			x_name = column_two_comment_x + 10
			self.inv_canvas.setFillColorRGB(*self.BLACK)
			self.inv_canvas.setFont("CalibriBold", 11)
			self.inv_canvas.drawString(x_name, current_row, section_3_dict[key][1])
			next_hour = int(section_3_dict[key][0]) if int(section_3_dict[key][0]) != 0 else 5
			current_hour = self.add_minutes_to_time(current_hour, next_hour)
			current_row += row_height

	def generate_pdf(self):
		# section_0_items = [('', '25 septembrie – 1 octombrie | ESTERA 9, 10', 'Președinte:', 'Russu Petru'), ('5', 'Cântarea 102', 'Rugăciune', 'Moldovanu Vasile'), ('5', 'Cuvinte introductive:', '', 'Russu Petru')]
		# section_1_items = [('10', '„El și-a folosit autoritatea în mod neegoist”', '', 'Moldovanu Vasile'), ('10', 'Să căutăm nestemate spirituale:', '', 'Russu Petru'), ('4', 'Citirea Bibliei', 'Cursant:', 'Popovici Ruslan')]
		# section_2_items = [('5', 'Vizita inițială', '', 'Ghidici Larisa/Nogai Aurica'), ('3', 'Vizita ulterioară:', '', 'Cebanu Crina/Tabaran Elena'), ('5', 'Studiu biblic', '', 'Moldovanu Galina/Șaban Tatiana')]
		# section_3_items = [('2', 'Cântarea 117', '', ''), ('15', '„Păstori care lucrează în folosul poporului lui Iehova”', '', 'Bodiu Ruslan'), ('30', 'Studiul Bibliei în congregație: lff lecția 59', 'Conducător/Cititor', 'Fanea Gheorghe/Moldovanu Vasile'), ('3', 'Cuvinte de încheiere (3 min.)', '', ''), ('0', 'Cântarea 55', 'Rugăciune:', 'Bodiu Ruslan')]
		
		i = 0
		for header_date in list(self.data_dict.keys()):

			if i == 0:
				self.draw_header()
				self.inv_canvas.translate(self.content_pos[0], self.content_pos[1])
				self.draw_content(header_date)
				self.inv_canvas.translate(-self.content_pos[0], -self.content_pos[1])
				i = 1
			else:
				self.inv_canvas.translate(self.content_pos[0], A4[1]/2)
				self.draw_content(header_date)
				self.inv_canvas.translate(-self.content_pos[0], -A4[1]/2)
				self.inv_canvas.showPage()
				i = 0

		# section_0_items = [('', '2-8 octombrie | IOV 1-3', 'Președinte:', 'Moldovanu Vasile'), ('5', 'Cântarea 141', 'Rugăciune', 'Russu Petru'), ('5', 'Cuvinte introductive:', '', 'Moldovanu Vasile')]
		# section_1_items = [('10', '„Continuă să arăți cât de mult îl iubești pe Iehova”:', '', 'Russu Petru'), ('10', 'Să căutăm nestemate spirituale:', '', 'Moldovanu Vasile'), ('4', 'Citirea Bibliei', 'Cursant:', 'Jîlenco Serghei')]
		# section_2_items = [('5', 'Vizita inițială:', '', 'Ghețu Tatiana/Tabaran Doina'), ('3', 'Vizita ulterioară:', '', 'Jîlenco Maria/Pasăre Natalia'), ('5', 'Cuvântare: th 18', '', 'Cebotari Valentin')]
		# section_3_items = [('2', 'Cântarea 21', '', ''), ('10', 'Credeam că fac totul cum trebuie:', '', 'Fanea Gheorghe'), ('5', '„Folosiți pagina principală a site-ului JW.ORG în lucrarea de predicare”:', '', 'Russu Petru'), ('30', 'Studiul Bibliei în congregație: lff lecția 59', 'Conducător/Cititor', 'Bodiu Ruslan'), ('3', 'Cuvinte de încheiere (3 min.)', '', ''), ('0', 'Cântarea 129', 'Rugăciune:', 'Plămădeală Ion A')]

		# self.draw_content()
		# self.inv_canvas.translate(-self.content_pos[0], -A4[1]/2)
		# self.inv_canvas.showPage()

		# # Next Page

		# section_0_items = [('', '9-15 octombrie | IOV 4, 5', 'Președinte:', 'Bodiu Ruslan'), ('5', 'Cântarea 121', 'Rugăciune', 'Fanea Gheorghe'), ('5', 'Cuvinte introductive:', '', 'Bodiu Ruslan')]
		# section_1_items = [('10', '„Nu te lăsa influențat de informații false”', '', 'Fanea Gheorghe'), ('10', 'Să căutăm nestemate spirituale:', '', 'Bodiu Ruslan'), ('4', 'Citirea Bibliei', 'Cursant:', 'Savițchi Damian')]
		# section_2_items = [('5', 'Vizita inițială', '', 'Popovici Eleonora/Maftuleac Stela'), ('3', 'Vizita ulterioară:', '', 'Ciulei Valentina/Popa Natalia'), ('5', 'Studiu biblic', '', 'Elade Rodica/Cenușă Ana')]
		# section_3_items = [('2', 'Cântarea 78', '', ''), ('15', 'Necesități locale', '', 'Moldovanu Vasile'), ('30', 'Studiul Bibliei în congregație: lff lecția 60', 'Conducător/Cititor', 'Russu Petru/Fanea Gheorghe'), ('3', 'Cuvinte de încheiere (3 min.)', '', ''), ('0', 'Cântarea 38', 'Rugăciune:', 'Bodiu Ruslan')]
		
		# self.draw_header()
		# self.inv_canvas.translate(self.content_pos[0], self.content_pos[1])
		# self.draw_content(section_0_items, section_1_items, section_2_items, section_3_items)
		# self.inv_canvas.translate(-self.content_pos[0], -self.content_pos[1])
		# self.inv_canvas.translate(self.content_pos[0], A4[1]/2)

		# section_0_items = [('', '16-22 octombrie | IOV 6, 7', 'Președinte:', 'Fanea Gheorghe'), ('5', 'Cântarea 33', 'Rugăciune', 'Bodiu Ruslan'), ('5', 'Cuvinte introductive:', '', 'Fanea Gheorghe')]
		# section_1_items = [('10', '„Când simți că viața nu mai are niciun rost”:', '', 'Bodiu Ruslan'), ('10', 'Să căutăm nestemate spirituale:', '', 'Fanea Gheorghe'), ('4', 'Citirea Bibliei', 'Cursant:', 'Spoială Leonid')]
		# section_2_items = [('5', 'Vizita inițială:', '', 'Savițchi Tatiana/Foleștian Viorica'), ('3', 'Vizita ulterioară:', '', 'Cevali Iraida'), ('5', 'Cuvântare: th 8', '', 'Cenușă Denis')]
		# section_3_items = [('2', 'Cântarea 144', '', ''), ('10', '„Iehova «îi salvează pe cei cu spiritul zdrobit»”:', '', 'Russu Petru'), ('30', 'Studiul Bibliei în congregație: lff recapitulare – partea a IV-a', 'Conducător/Cititor', 'Moldovanu Vasile'), ('3', 'Cuvinte de încheiere (3 min.)', '', ''), ('0', 'Cântarea 143', 'Rugăciune:', 'Pasăre Vasile')]

		# self.draw_content(section_0_items, section_1_items, section_2_items, section_3_items)
		# self.inv_canvas.translate(-self.content_pos[0], -A4[1]/2)
		# self.inv_canvas.showPage()

		self.inv_canvas.save()













class Parse_Meeting_WorkBook(QObject):
	download_progress_signal = pyqtSignal(int)
	parse_progress_signal = pyqtSignal(int)

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

















import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QWidget, QLabel, QLineEdit, QScrollArea, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
import fitz

from pdf_generator import Testimony_Cart_PDF_Generator


class MainApp(QMainWindow):
	def __init__(self):
		super().__init__()
		ui_path = os.path.join(os.getcwd(), 'assets', 'ui', 'ui.ui')
		uic.loadUi(ui_path, self)

		self.init_ui()
		## loading style file
		with open(os.path.join('assets', 'ui', 'stylesheet.qss'), 'r') as style_file:
			style_str = style_file.read()
		self.setStyleSheet(style_str)


	def init_ui(self):
		self.full_menu_widget.setHidden(True)
		self.default_title = 'Mărturia cu căruciorul'
		self.output_path = None

		self.data_dict = {}

		self.set_cart_widget()

		self.name_entry.returnPressed.connect(self.add_name)
		self.add_name_button.clicked.connect(self.add_name)
		self.name_list_widget.setSelectionMode(QListWidget.MultiSelection)
		self.remove_name_button.clicked.connect(self.remove_name)
		self.browse_img_button.clicked.connect(self.browse_image)
		self.browse_output_button.clicked.connect(self.browse_output)
		self.generate_cart_button.clicked.connect(self.generate_cart_pdf)
		self.generate_workbook_button.clicked.connect(self.generate_workbook_pdf)

		self.cart_widget_btn.clicked.connect(self.set_cart_widget)
		self.group_list_widget_btn.clicked.connect(self.set_group_list_widget)

		self.title_entry.installEventFilter(self)
		self.img_entry.installEventFilter(self)

		self.pdf_preview.setScene(QGraphicsScene())
		self.pdf_preview.setAlignment(Qt.AlignCenter)


		# self.central_widget = QWidget(self)
		# self.setCentralWidget(self.central_widget)

		# layout = QVBoxLayout()

		# self.start_button = QPushButton("Start Parsing")
		# self.progress_bar = QProgressBar()
		# self.progress_label = QLabel("Progress: 0%")

		# layout.addWidget(self.start_button)
		# layout.addWidget(self.progress_bar)
		# layout.addWidget(self.progress_label)

		# self.central_widget.setLayout(layout)

		self.button_parsing_workbook.clicked.connect(self.parsing_workbook)

	def show_workbook(self):
		data_dict = self.data_dict
		list_tabs = list(data_dict.keys())

		for tab_index in range(len(list_tabs)):
			tab = QWidget()
			tab_layout = QVBoxLayout(tab)  # QVBoxLayout to hold the QScrollArea
			scroll_area = QScrollArea()  # Create the QScrollArea
			scroll_area.setWidgetResizable(True)
			scroll_content_widget = QWidget()
			scroll_area.setWidget(scroll_content_widget)
			grid_layout_1 = QGridLayout(scroll_content_widget)


			# ADD rows
			# =========================
			row = 0
			label_width = 500

			# Section Header
			# =========================
			label = QLabel('Președinte')
			label.setWordWrap(True)
			label.setMaximumWidth(label_width)

			grid_layout_1.addWidget(label, row, 0, 1, 1)
			grid_layout_1.addWidget(QLineEdit(), row, 1, 1, 1)
			row += 1

			header_dict = data_dict[list_tabs[tab_index]]['header']
			for item in list(header_dict.keys()):
				label_item = QLabel(item)
				label_item.setWordWrap(True)
				label_item.setMaximumWidth(label_width)

				grid_layout_1.addWidget(label_item, row, 0, 1, 1)
				grid_layout_1.addWidget(QLineEdit(), row, 1, 1, 1)
				row += 1

			# Section Intro
			# =========================
			intro_dict = data_dict[list_tabs[tab_index]]['intro']
			for item in list(intro_dict.keys()):
				label_item = QLabel(item)
				label_item.setWordWrap(True)
				label_item.setMaximumWidth(label_width)

				grid_layout_1.addWidget(label_item, row, 0, 1, 1)
				grid_layout_1.addWidget(QLineEdit(), row, 1, 1, 1)
				row += 1

			section_0_label = QLabel('COMORI DIN CUVÂNTUL LUI DUMNEZEU')
			section_0_label.setStyleSheet("background-color: rgb(86,86,86);")
			grid_layout_1.addWidget(section_0_label, row, 0, 1, 1)
			row += 1

			# Section 1
			# =========================
			section_1_dict = data_dict[list_tabs[tab_index]]['section_1']
			for item in list(section_1_dict.keys()):
				label_item = QLabel(item)
				label_item.setWordWrap(True)
				label_item.setMaximumWidth(label_width)

				grid_layout_1.addWidget(label_item, row, 0, 1, 1)
				grid_layout_1.addWidget(QLineEdit(), row, 1, 1, 1)
				row += 1

			section_1_label = QLabel('SĂ FIM MAI EFICIENȚI ÎN PREDICARE')
			section_1_label.setStyleSheet("background-color: rgb(190,137,0)")
			grid_layout_1.addWidget(section_1_label, row, 0, 1, 1)
			row += 1

			# Section 2
			# =========================
			section_2_dict = data_dict[list_tabs[tab_index]]['section_2']
			for item in list(section_2_dict.keys()):
				label_item = QLabel(item)
				label_item.setWordWrap(True)
				label_item.setMaximumWidth(label_width)

				grid_layout_1.addWidget(label_item, row, 0, 1, 1)
				grid_layout_1.addWidget(QLineEdit(), row, 1, 1, 1)
				row += 1

			section_2_label = QLabel('VIAȚA DE CREȘTIN')
			section_2_label.setStyleSheet("background-color: rgb(136,0,36)")
			grid_layout_1.addWidget(section_2_label, row, 0, 1, 1)
			row += 1

			# Section 3
			# =========================
			section_3_dict = data_dict[list_tabs[tab_index]]['section_3']
			for item in list(section_3_dict.keys()):
				label_item = QLabel(item)
				label_item.setWordWrap(True)
				label_item.setMaximumWidth(label_width)

				grid_layout_1.addWidget(label_item, row, 0, 1, 1)
				grid_layout_1.addWidget(QLineEdit(), row, 1, 1, 1)
				row += 1


			tab_layout.addWidget(scroll_area)

			# Set the QVBoxLayout as the main layout of the tab
			tab.setLayout(tab_layout)

			# Add the tab to the tab widget
			self.tabWidget.addTab(tab, list_tabs[tab_index])


	def set_cart_widget(self):
		self.cart_widget_btn.setStyleSheet('#cart_widget_btn{ background-color: #3b434f;}')
		self.group_list_widget_btn.setStyleSheet('')
		self.stackedWidget.setCurrentIndex(0)

	def set_group_list_widget(self):
		self.group_list_widget_btn.setStyleSheet('#group_list_widget_btn{ background-color: #3b434f;}')
		self.cart_widget_btn.setStyleSheet('')
		self.stackedWidget.setCurrentIndex(1)

	def eventFilter(self, obj, event):
		if obj in (self.title_entry, self.img_entry):
			if event.type() == event.FocusOut:
				self.update_preview()

		return super().eventFilter(obj, event)

	def browse_image(self):
		img_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
		if img_path:
			self.img_entry.setText(img_path)

		self.update_preview()

	def browse_output(self):
		self.output_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
		if self.output_path:
			self.output_entry.setText(self.output_path)

	def add_name(self):
		name = self.name_entry.text().strip()
		if name:
			self.name_list_widget.addItem(name)
			self.name_entry.clear()

		self.update_preview()

	def remove_name(self):
		selected_items = self.name_list_widget.selectedItems()
		for item in selected_items:
			self.name_list_widget.takeItem(self.name_list_widget.row(item))

		self.update_preview()

	def generate_workbook_pdf(self):
		for tab_index in range(self.tabWidget.count()):
			# list_data = []
			tab_title = self.tabWidget.tabText(tab_index)

			tab_widget = self.tabWidget.widget(tab_index)

			label_list = tab_widget.findChildren(QLabel)
			label_list = [label.text() for label in label_list]


			if 'COMORI DIN CUVÂNTUL LUI DUMNEZEU' in label_list or 'SĂ FIM MAI EFICIENȚI ÎN PREDICARE' in label_list or 'VIAȚA DE CREȘTIN' in label_list:
				label_list = list(filter(lambda x: x not in ['COMORI DIN CUVÂNTUL LUI DUMNEZEU', 'SĂ FIM MAI EFICIENȚI ÎN PREDICARE', 'VIAȚA DE CREȘTIN'], label_list))

			line_edit_list = tab_widget.findChildren(QLineEdit)
			line_edit_list = [line_edit.text() for line_edit in line_edit_list]

			date_list = list(self.data_dict.keys())
			# for date_index in range(len(date_list)):
			header_dict = self.data_dict[date_list[tab_index]]["header"]
			intro_dict = self.data_dict[date_list[tab_index]]["intro"]
			section_1_dict = self.data_dict[date_list[tab_index]]["section_1"]
			section_2_dict = self.data_dict[date_list[tab_index]]["section_2"]
			section_3_dict = self.data_dict[date_list[tab_index]]["section_3"]
			
			header_dict[list(header_dict.keys())[0]].append(line_edit_list[label_list.index("Președinte")])
			
			for section_key in list(intro_dict.keys()):
				intro_dict[section_key].append(line_edit_list[label_list.index(section_key)])
			
			for section_key in list(section_1_dict.keys()):
				section_1_dict[section_key].append(line_edit_list[label_list.index(section_key)])
			
			for section_key in list(section_2_dict.keys()):
				section_2_dict[section_key].append(line_edit_list[label_list.index(section_key)])
			
			for section_key in list(section_3_dict.keys()):
				section_3_dict[section_key].append(line_edit_list[label_list.index(section_key)])

		output_path = 'file.pdf'
		congregation = 'GLODENI-SUD'


		print(self.data_dict)
		service_schedule = Service_Schedule_PDF_Generator(output_path, congregation, self.data_dict)
		service_schedule.generate_pdf()


				# if not label_list[row] in ['COMORI DIN CUVÂNTUL LUI DUMNEZEU', 'SĂ FIM MAI EFICIENȚI ÎN PREDICARE', 'VIAȚA DE CREȘTIN']:
				#     list_data.append([label_list[row], line_edit_list[row].text()])
		
			# data_dict[tab_title] = list_data

		#print(data_dict)


		# widgets = [self.tabWidget.tabText(index) for index in range(self.tabWidget.count())]
		# line_edits = self.tabWidget.findChildren(QLineEdit)

		# Iterate through the found labels and line edits
		# for label in labels:
		#     print("Label Text:", label.text())

		# for widget in widgets:
		#     print("Object name:", widget)


	def generate_cart_pdf(self):
		title = self.title_entry.text()
		img_path = self.img_entry.text()
		self.output_path = self.output_entry.text()
		name_list = [self.name_list_widget.item(index).text() for index in range(self.name_list_widget.count())]

		pdf_generator = Testimony_Cart_PDF_Generator(self.output_path, title, img_path, name_list)
		pdf_generator.generate_pdf()
		QMessageBox.information(self, "PDF Generated", "PDF has been generated successfully!")


	def update_preview(self):
		title = self.title_entry.text()
		img_path = self.img_entry.text()
		output_temp = os.path.join(os.getcwd(), "temp.pdf.temp")
		name_list = [self.name_list_widget.item(index).text() for index in range(self.name_list_widget.count())]

		pdf_generator = Testimony_Cart_PDF_Generator(output_temp, title, img_path, name_list)
		pdf_generator.generate_pdf()

		scene = self.pdf_preview.scene()
		scene.clear()

		# Load PDF using PyMuPDF
		pdf_document = fitz.open(output_temp)
		first_page = pdf_document[0]
		pixmap = first_page.get_pixmap()  # Adjust the scale as needed   matrix=fitz.Matrix(2, 2)

		# Convert pixmap to QImage and display in QGraphicsView
		q_image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
		
		pixmap = QPixmap.fromImage(q_image)

		targete_size = self.pdf_preview.size()
		pixmap = pixmap.scaled(targete_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

		# scene = QGraphicsScene()
		scene.addPixmap(pixmap)
		self.pdf_preview.setScene(scene)


		# Remove temp file
		try:
			os.remove(output_temp)
		except OSError as e:
			pass

	def parsing_workbook(self):
		self.button_parsing_workbook.setEnabled(False)
		self.progressbar_status_label.setText("Please wait...")

		site_domain = 'https://www.jw.org'
		meeting_workbooks_url = 'https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire'
		current_workbook_name = 'septembrie-octobrie-2023-mwb/'
		workbook_url = os.path.join(meeting_workbooks_url, current_workbook_name)


		self.worker_thread = WorkerThread(site_domain, workbook_url)
		self.worker_thread.download_progress_signal.connect(self.update_download_progress)
		self.worker_thread.parse_progress_signal.connect(self.update_parse_progress)
		self.worker_thread.finished.connect(self.parsing_finished)
		self.worker_thread.start()

	def update_download_progress(self, value):
		self.progressbar_workbook.setValue(value)
		# self.progress_label.setText(f"Downloading: {value}%")

	def update_parse_progress(self, value):
		self.progressbar_workbook.setValue(value)
		# self.progress_label.setText(f"Parsing: {value}%")

	def parsing_finished(self):
		self.button_parsing_workbook.setEnabled(True)
		self.progressbar_status_label.setText("finished!")
		print(self.worker_thread.data_dict)
		self.data_dict = self.worker_thread.data_dict
		self.show_workbook()


class WorkerThread(QThread):
	download_progress_signal = pyqtSignal(int)  # Add this line
	parse_progress_signal = pyqtSignal(int)  # Add this line

	def __init__(self, domain, url):
		super().__init__()
		self.domain = domain
		self.url = url
		self.data_dict = {}

	def run(self):
		self.parser = Parse_Meeting_WorkBook(self.domain, self.url)
		self.parser.download_progress_signal.connect(self.download_progress_signal.emit)
		self.parser.parse_progress_signal.connect(self.parse_progress_signal.emit)
		self.data_dict = self.parser.get_dict_data()


	def emit_download_progress(self, value):
		self.download_progress_signal.emit(value)

	def emit_parse_progress(self, value):
		self.parse_progress_signal.emit(value)



if __name__ == "__main__":
	app = QApplication(sys.argv)

	main_window = MainApp()
	main_window.show()

	sys.exit(app.exec_())





	# workbook_data = {
	# 	'4-10 septembrie': [['ESTERA 1, 2'], [[0, 'Cântarea 137'], [1, 'Cuvinte introductive']], [[10, '„ Străduiește-te să fii modest la fel ca Estera ”:'], [10, 'Nestemate spirituale:'], [4, 'Citirea Bibliei:']], [[5, 'Vizita inițială – Material video:'], [3, 'Vizita inițială:'], [5, 'Cuvântare:']], [[0, 'Cântarea 106'], [5, 'Ce spun alți tineri – Înfățișare:'], [10, 'Realizări organizatorice:'], [30, 'Studiul Bibliei în congregație:'], [3, 'Cuvinte de încheiere'], [0, 'Cântarea 101 și rugăciune']]],
	# 	'11-17 septembrie': [['ESTERA 3-5'], [[0, 'Cântarea 85'], [1, 'Cuvinte introductive']], [[10, '„ Ajută-i pe alții să-și folosească la maximum potențialul ”:'], [10, 'Nestemate spirituale:'], [4, 'Citirea Bibliei:']], [[5, 'Vizita ulterioară – Material video:'], [3, 'Vizita ulterioară:'], [5, 'Studiu biblic:']], [[0, 'Cântarea 65'], [5, 'Cum poți să devii prietenul lui Iehova – Vrem să fim ca Estera:'], [10, 'Necesități locale:'], [30, 'Studiul Bibliei în congregație:'], [3, 'Cuvinte de încheiere'], [0, 'Cântarea 125 și rugăciune']]]
	# }

	# label_list = ['ESTERA 1, 2', 'Cântarea 137', 'Cuvinte introductive', '„ Străduiește-te să fii modest la fel ca Estera ”:', 'Nestemate spirituale:', 'Citirea Bibliei:', 'Vizita inițială – Material video:', 'Vizita inițială:', 'Cuvântare:', 'Cântarea 106', 'Ce spun alți tineri – Înfățișare:', 'Realizări organizatorice:', 'Studiul Bibliei în congregație:', 'Cuvinte de încheiere', 'Cântarea 101 și rugăciune', 'ESTERA 3-5']
	# line_edit_list = ['Petru Russu', 'Petru Russu', 'Moldovanu Vasile', 'Petru Russu', 'Petru Russu', 'Andrei Cenusa', '', 'Fanea Natalia/Moldovanu Galina', 'Pasare Vasile', '', 'Petru Russu', 'Bodiu Ruslan', 'Fanea Gheorghe/Pasare Vasile', 'Russu Petru', 'Moldovanu Vasile', 'Fanea Gheorghe']

	# for date, items in workbook_data.items():
	# 	for item in items:
	# 		if isinstance(item, list):
	# 			for i, name in enumerate(item):
	# 				item[i] = name + ' ' + line_edit_list[label_list.index(item[0])]
	# 		else:
	# 			workbook_data[date][items] = items + ' ' + line_edit_list[label_list.index(item)]

	# print(workbook_data)




# if __name__ == '__main__':

	# data_dict = {'6-12 noiembrie': [['IOV 13, 14'], ['Cântarea 151 și rugăciune', 'Cuvinte introductive (1 min.)'], ['„Dacă omul moare, poate el trăi din nou?”: (10 min.)', 'Nestemate spirituale: (10 min.)', 'Citirea Bibliei: (4\xa0min.) Iov 13:1-28 (th lecția\xa012)'], ['Vizita inițială – Material video: (5 min.) Discuție. Se va viziona materialul Vizita inițială – Biblia (2Ti 3:16, 17). La fiecare pauză acesta va fi oprit, iar auditoriul va răspunde la întrebările afișate.', 'Vizita inițială: (3\xa0min.) Începe cu subiectul conversației-model. Oferă broșura Bucură-te pentru totdeauna de viață!. (th lecția\xa02)', 'Studiu biblic: (5\xa0min.) lff recapitulare – partea\xa0I, întrebările\xa01-5 (th lecția\xa019)'], ['Cântarea 127', '„Să punem ceva deoparte”: (15\xa0min.) Discuție și material video. Tema va fi ținută de un bătrân. Laudă congregația pentru donațiile făcute în sprijinul organizației lui Iehova.', 'Studiul Bibliei în congregație: (30\xa0min.) bt cap.\xa01 ¶16-21', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 76 și rugăciune']], '13-19 noiembrie': [['IOV 15-17'], ['Cântarea 90 și rugăciune', 'Cuvinte introductive (1\xa0min.)'], ['„Să nu-l imităm pe Elifaz când vrem să le aducem consolare altora”: (10\xa0min.)', 'Nestemate spirituale: (10\xa0min.)', 'Citirea Bibliei: (4\xa0min.) Iov 17:1-16 (th lecția\xa012)'], ['Vizita ulterioară – Material video: (5\xa0min.) Discuție. Se va viziona materialul Vizita ulterioară – Biblia (Iov 26:7). La fiecare pauză, acesta va fi oprit, iar auditoriul va răspunde la întrebările afișate.', 'Vizita ulterioară: (3\xa0min.) Începe cu subiectul conversației-model. Prezintă programul nostru de studiere a Bibliei și oferă o carte de vizită „Curs biblic gratuit”. (th lecția\xa011)', 'Studiu biblic: (5\xa0min.) lff recapitulare – partea\xa0I, întrebările\xa06-10 (th lecția\xa08)'], ['Cântarea 96', 'Necesități locale: (15\xa0min.)', 'Studiul Bibliei în congregație: (30\xa0min.) bt cap.\xa02 ¶1-7 și introducerea la partea\xa0I', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 118 și rugăciune']], '20-26 noiembrie': [['IOV 18, 19'], ['Cântarea 44 și rugăciune', 'Cuvinte introductive (1\xa0min.)'], ['„Să nu le întoarcem niciodată spatele fraților noștri creștini”: (10\xa0min.)', 'Nestemate spirituale: (10\xa0min.)', 'Citirea Bibliei: (4\xa0min.) Iov 18:1-21 (th lecția\xa05)'], ['Vizita inițială: (3\xa0min.) Începe cu subiectul conversației-model. Depășește o obiecție des întâlnită. (th lecția\xa012)', 'Vizita ulterioară: (4\xa0min.) Începe cu subiectul conversației-model. Invită persoana la o întrunire a congregației. Prezintă și analizează materialul video Ce activități se desfășoară la o sală a Regatului? (nu se va viziona materialul). (th lecția\xa03)', 'Cuvântare: (5\xa0min.) w20.10 17 ¶10,\xa011 – Tema: Încurajează-ți elevul să-și facă prieteni în congregație. (th lecția\xa020)'], ['Cântarea 90', 'Cum poți să devii prietenul lui Iehova – Ajută-i pe alții: (5\xa0min.) Discuție. Se va viziona materialul. Apoi, dacă este posibil, invită câțiva copii, aleși dinainte, să răspundă la următoarele întrebări: Cum îi pot ajuta copiii pe alții?', '„O măsură luată pentru încurajarea celor ce slujesc la Betel”: (10\xa0min.) Discuție și material video.', 'Studiul Bibliei în congregație: (30\xa0min.) bt cap.\xa02 ¶8-15', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 63 și rugăciune']], '27 noiembrie – 3 decembrie': [['IOV 20, 21'], ['Cântarea 38 și rugăciune', 'Cuvinte introductive (1\xa0min.)'], ['„Dreptatea unui om nu se reflectă în starea lui materială”: (10\xa0min.)', 'Nestemate spirituale: (10\xa0min.)', 'Citirea Bibliei: (4\xa0min.) Iov 20:1-22 (th lecția\xa05)'], ['Vizita inițială: (2\xa0min.) Folosește subiectul conversației-model. (th lecția\xa01)', 'Vizita ulterioară: (5\xa0min.) Începe cu subiectul conversației-model. Oferă broșura Bucură-te pentru totdeauna de viață! și arată cum se desfășoară un studiu biblic. (th lecția\xa06)', 'Cuvântare: (5 min.) g 5/09 12,\xa013 – Tema: Vrea Dumnezeu să fim bogați? (th lecția\xa017)'], ['Cântarea 136', '„Să fim mulțumiți cu ce avem”: (15\xa0min.) Discuție. Se va viziona materialul.', 'Studiul Bibliei în congregație: (30\xa0min.) bt cap.\xa02 ¶16-23', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 103 și rugăciune']], '4-10 decembrie': [['IOV 22-24'], ['Cântarea 49 și rugăciune', 'Cuvinte introductive (1\xa0min.)'], ['„Poate omul să-i fie de folos lui Dumnezeu?”: (10\xa0min.)', 'Nestemate spirituale: (10\xa0min.)', 'Citirea Bibliei: (4\xa0min.) Iov 22:1-22 (th lecția\xa05)'], ['Vizita inițială: (3\xa0min.) Începe cu subiectul conversației-model. Vorbește-i persoanei despre site-ul nostru și oferă-i o carte de vizită cu jw.org. (th lecția\xa011)', 'Vizita ulterioară: (4\xa0min.) Începe cu subiectul conversației-model. Prezintă și analizează materialul video De ce să studiați Biblia? (nu se va viziona materialul). (th lecția\xa02)', 'Cuvântare: (5\xa0min.) w21.05 18, 19 ¶17-20 – Tema: Păstrându-ne atitudinea pozitivă îi permitem lui Iehova să ne folosească. (th lecția\xa020)'], ['Cântarea 134', '„Părinți, ajutați-vă copiii să-l bucure pe Dumnezeu”: (10\xa0min.) Discuție și material video.', 'Necesități locale: (5\xa0min.)', 'Studiul Bibliei în congregație: (30\xa0min.) bt cap.\xa03 ¶1-3, chenarele de la pag.\xa023, 24, 25,\xa026 și\xa027', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 25 și rugăciune']], '11-17 decembrie': [['IOV 25-27'], ['Cântarea 34 și rugăciune', 'Cuvinte introductive (1\xa0min.)'], ['„A fi integri nu înseamnă a fi perfecți”: (10\xa0min.)', 'Nestemate spirituale: (10\xa0min.)', 'Citirea Bibliei: (4\xa0min.) Iov 25:1–26:14 (th lecția\xa012)'], ['Vizita inițială: (2\xa0min.) Folosește subiectul conversației-model. Depășește o obiecție des întâlnită. (th lecția\xa01)', 'Vizita ulterioară: (5\xa0min.) Începe cu subiectul conversației-model. Arată-i persoanei cum să găsească informații pe site-ul jw.org cu privire la un subiect care o interesează. (th lecția\xa017)', 'Studiu biblic: (5\xa0min.) lff lecția\xa013, introducere și punctele\xa01-3 (th lecția\xa015)'], ['Cântarea 45', '„Integritatea și gândurile noastre”: (5\xa0min.) Discuție.', 'Realizări organizatorice: (10\xa0min.) Se va viziona materialul Realizări organizatorice pentru luna decembrie.', 'Studiul Bibliei în congregație: (30\xa0min.) bt\xa0cap.\xa03 ¶4-11', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 57 și rugăciune']], '18-24 decembrie': [['IOV 28,\xa029'], ['Cântarea 39 și rugăciune', 'Cuvinte introductive (1\xa0min.)'], ['„Ai o reputație ca a lui Iov?”: (10\xa0min.)', 'Nestemate spirituale: (10\xa0min.)', 'Citirea Bibliei: (4\xa0min.) Iov 28:1-28 (th lecția\xa05)'], ['Vizita inițială: (3\xa0min.) Începe cu subiectul conversației-model. Oferă broșura Bucură-te pentru totdeauna de viață!. (th lecția\xa03)', 'Vizita ulterioară: (4\xa0min.) Începe cu subiectul conversației-model. Oferă-i persoanei broșura Bucură-te pentru totdeauna de viață! și analizează pe scurt „Cum poți trage foloase din aceste lecții biblice”. (th lecția\xa017)', 'Studiu biblic: (5\xa0min.) lff lecția\xa013, „Aprofundează” și punctul\xa04 (th lecția\xa06)'], ['Cântarea 121', '„Cum contribui eu la buna reputație a organizației noastre”: (15\xa0min.) Discuție și material video.', 'Studiul Bibliei în congregație: (30\xa0min.) bt\xa0cap.\xa03 ¶12-18', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 50 și rugăciune']], '25-31 decembrie': [['IOV 30,\xa031'], ['Cântarea 28 și rugăciune', 'Cuvinte introductive (1\xa0min.)'], ['„Cum și-a păstrat Iov castitatea”: (10\xa0min.)', 'Nestemate spirituale: (10\xa0min.)', 'Citirea Bibliei: (4\xa0min.) Iov 31:15-40 (th lecția\xa05)'], ['Vizita inițială: (4\xa0min.) Începe cu subiectul conversației-model. Prezintă programul nostru de studiere a Bibliei și oferă o carte de vizită „Curs biblic gratuit”. (th lecția\xa01)', 'Vizita ulterioară: (3\xa0min.) Începe cu subiectul conversației-model. Invită persoana la o întrunire a congregației. Prezintă și analizează materialul video Ce activități se desfășoară la o sală a Regatului? (nu se va viziona materialul). (th lecția\xa011)', 'Cuvântare: (5\xa0min.) g16.4 8,\xa09 – Tema: Cum pot să explic punctul de vedere biblic cu privire la homosexualitate? (th lecția\xa014)'], ['Cântarea 36', '„De ce este dăunătoare pornografia”: (7\xa0min.) Discuție și material video.', 'Necesități locale: (8\xa0min.)', 'Studiul Bibliei în congregație: (30\xa0min.) bt\xa0cap.\xa04 ¶1-8', 'Cuvinte de încheiere (3\xa0min.)', 'Cântarea 74 și rugăciune']]}
	
	# output_path = 'file.pdf'
	# congregation = 'GLODENI-SUD'


	# service_schedule = Service_Schedule_PDF_Generator(output_path, congregation, data_dict)
	# service_schedule.generate_pdf()


	# site_domain = 'https://www.jw.org'
	# meeting_workbook_url = 'https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire'
	# current_workbook_name = 'noiembrie-decembrie-2023-mwb/'

	# site_domain = 'https://www.jw.org'
	# meeting_workbooks_url = 'https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire'
	# current_workbook_name = 'noiembrie-decembrie-2023-mwb/'
	# workbook_url = os.path.join(meeting_workbooks_url, current_workbook_name)

	# parse_workbook = Parse_Meeting_WorkBook(site_domain, os.path.join(meeting_workbook_url, current_workbook_name))
	# data_dict = parse_workbook.get_dict_data()
	# print(data_dict)
	










# dict_data = {"6-12 noiembrie":{"header":{"IOV 13, 14":[0,""]},"intro":{"Cântarea 151":[0,""],"Cuvinte introductive":[1,""]},"TREASURES":{"„ Dacă omul moare, poate el trăi din nou? ”":[10,""],"Nestemate spirituale":[10,""],"Citirea Bibliei":[4,""]},"MINISTRY":{"Vizita inițială – Material video":[5,""],"Vizita inițială":[3,""],"Studiu biblic":[5,""]},"LIVING AS CHRISTIANS":{"Cântarea 127":[0,""],"„ Să punem ceva deoparte ”":[15,""],"Studiul Bibliei în congregație":[30,""],"Cuvinte de încheiere":[3,""],"Cântarea 76 și rugăciune":[0,""]}},"13-19 noiembrie":{"header":{"IOV 15-17":[0,""]},"intro":{"Cântarea 90":[0,""],"Cuvinte introductive":[1,""]},"TREASURES":{"„ Să nu-l imităm pe Elifaz când vrem să le aducem consolare altora ”:":[10,""],"Nestemate spirituale:":[10,""],"Citirea Bibliei":[4,""]},"MINISTRY":{"Vizita ulterioară – Material video:":[5,""],"Vizita ulterioară:":[3,""],"Studiu biblic:":[5,""]},"LIVING AS CHRISTIANS":{"Cântarea 96":[0,""],"Necesități locale":[15,""],"Studiul Bibliei în congregație:":[30,""],"Cuvinte de încheiere":[3,""],"Cântarea 118 și rugăciune":[0,""]}}}

# label_list = ['Președinte', 'Cântarea 151', 'Cuvinte introductive', '„ Dacă omul moare, poate el trăi din nou? ”', 'Nestemate spirituale', 'Citirea Bibliei', 'Vizita inițială – Material video', 'Vizita inițială', 'Studiu biblic', 'Cântarea 127', '„ Să punem ceva deoparte ”', 'Studiul Bibliei în congregație', 'Cuvinte de încheiere', 'Cântarea 76 și rugăciune']
# entry_list = ['Petru Russu', 'Gheorghe Fanea', 'Gheorghe Fanea', 'Petru Russu', 'Gheorghe Fanea', 'Andrei Cenusa', '', 'Natalia fanea/Galina Moldovanu', 'Nina Vidrasco/Elea Popovici', '', 'Petru Russu', 'Gheorghe Fanea/Vasile Pasare', 'Petru Russu', 'Ruslan Bodiu']

# date_list = list(dict_data.keys())
# print(date_list)

# for date_index in range(len(date_list)):
#     header = dict_data[date_list[date_index]]["header"]
#     intro_dict = dict_data[date_list[date_index]]["intro"]
#     section_1_dict = dict_data[date_list[date_index]]["TREASURES"]
#     section_2_dict = dict_data[date_list[date_index]]["MINISTRY"]
#     section_3_dict = dict_data[date_list[date_index]]["LIVING AS CHRISTIANS"]
	
#     header[list(header.keys())[0]].append(entry_list[label_list.index("Președinte")])
	
#     for section_key in list(intro_dict.keys()):
#         intro_dict[section_key].append(entry_list[label_list.index(section_key)])
#         print(intro_dict[section_key])
		
#     for section_key in list(section_1_dict.keys()):
#         section_1_dict[section_key].append(entry_list[label_list.index(section_key)])
#         print(section_1_dict[section_key])
	
#     for section_key in list(section_2_dict.keys()):
#         section_2_dict[section_key].append(entry_list[label_list.index(section_key)])
#         print(section_2_dict[section_key])
	
#     for section_key in list(section_3_dict.keys()):
#         section_3_dict[section_key].append(entry_list[label_list.index(section_key)])
#         print(section_3_dict[section_key])
	
#     break

# print(len(label_list))
# print(len(entry_list))

# print(dict_data)