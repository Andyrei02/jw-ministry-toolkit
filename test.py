import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal


import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QWidget, QLabel, QLineEdit, QScrollArea, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
import fitz

from pdf_generator import Testimony_Cart_PDF_Generator, Service_Schedule_PDF_Generator
from parse_workbook import Parse_Meeting_WorkBook


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
		self.worker_thread.finished.connect(self.parsing_finished)
		self.worker_thread.start()

	def update_download_progress(self, value):
		self.progressbar_workbook.setValue(value)
		# self.progress_label.setText(f"Downloading: {value}%")

	def parsing_finished(self):
		self.button_parsing_workbook.setEnabled(True)
		self.progressbar_status_label.setText("finished!")
		print(self.worker_thread.data_dict)
		self.data_dict = self.worker_thread.data_dict
		self.show_workbook()


class WorkerThread(QThread):
	download_progress_signal = pyqtSignal(int)  # Add this line

	def __init__(self, domain, url):
		super().__init__()
		self.domain = domain
		self.url = url
		self.data_dict = {}

	def run(self):
		self.parser = Parse_Meeting_WorkBook(self.domain, self.url)
		self.parser.download_progress_signal.connect(self.download_progress_signal.emit)
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