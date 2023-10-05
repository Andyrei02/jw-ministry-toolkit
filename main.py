import sys
import os
import glob

import fitz

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QScrollArea, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import uic

from config import Config
from pdf_generator import Testimony_Cart_PDF_Generator, Service_Schedule_PDF_Generator
from parse_workbook import Parse_Meeting_WorkBook


class MainApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.config = Config()
		self.current_path = self.config.current_path
		ui_path = os.path.join(self.current_path, 'assets', 'ui', 'ui.ui')
		uic.loadUi(ui_path, self)
		
		## loading style file
		self.current_theme = self.config.get_item('theme')
		with open(os.path.join(self.current_path, 'assets', 'ui', 'stylesheets', self.current_theme+'.qss'), 'r') as style_file:
			style_str = style_file.read()
		self.setStyleSheet(style_str)

		self.init_ui()

	def init_ui(self):
		self.label_version_app.setText(f"v. {self.config.get_item('version')}")
		self.full_menu_widget.setHidden(True)
		self.default_title = 'Mărturia cu căruciorul'
		self.output_path = None
		self.data_dict = {}

		self.set_cart_widget()

		self.style_btn.clicked.connect(self.next_theme)

		self.name_entry.returnPressed.connect(self.add_name)
		self.add_name_button.clicked.connect(self.add_name)
		self.name_list_widget.setSelectionMode(QListWidget.MultiSelection)
		self.remove_name_button.clicked.connect(self.remove_name)
		self.browse_img_button.clicked.connect(self.browse_image)
		self.browse_output_button.clicked.connect(self.browse_output)
		self.generate_cart_button.clicked.connect(self.generate_cart_pdf)
		self.generate_workbook_button.clicked.connect(self.generate_workbook_pdf)

		self.cart_widget_btn.clicked.connect(self.set_cart_widget)
		self.workbook_widget_btn.clicked.connect(self.set_group_list_widget)

		self.title_entry.installEventFilter(self)
		self.img_entry.installEventFilter(self)

		self.pdf_preview.setScene(QGraphicsScene())
		self.pdf_preview.setAlignment(Qt.AlignCenter)

		self.button_parsing_workbook.clicked.connect(self.parsing_workbook)

	def next_theme(self):
		styles_path = os.path.join(self.current_path, 'assets', 'ui', 'stylesheets')
		list_themes = glob.glob(os.path.join(styles_path, '*.qss'))
		current_theme_index = list_themes.index(os.path.join(styles_path, self.current_theme+'.qss'))
		current_theme_index = list_themes.index(os.path.join(styles_path, self.current_theme + '.qss'))
		next_theme_index = (current_theme_index + 1) % len(list_themes)
		next_theme = os.path.basename(list_themes[next_theme_index])
		self.current_theme = next_theme[:-4]
		self.config.set_item('theme', self.current_theme)

		with open(os.path.join(styles_path, self.current_theme+'.qss'), 'r') as style_file:
			style_str = style_file.read()
		self.setStyleSheet(style_str)

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
			self.work_book_content_widget.addTab(tab, list_tabs[tab_index])

	def set_cart_widget(self):
		self.cart_widget_btn.setEnabled(False)
		self.workbook_widget_btn.setEnabled(True)
		self.stackedWidget.setCurrentIndex(0)

	def set_group_list_widget(self):
		self.workbook_widget_btn.setEnabled(False)
		self.cart_widget_btn.setEnabled(True)
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
		for tab_index in range(self.work_book_content_widget.count()):
			# list_data = []
			tab_title = self.work_book_content_widget.tabText(tab_index)

			tab_widget = self.work_book_content_widget.widget(tab_index)

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

		output_path = os.path.join(self.current_path, 'file.pdf')
		congregation = 'GLODENI-SUD'

		service_schedule = Service_Schedule_PDF_Generator(output_path, congregation, self.data_dict)
		service_schedule.generate_pdf()

	def generate_cart_pdf(self):
		title = self.title_entry.text()
		img_path = self.img_entry.text()
		self.output_path = self.output_entry.text()
		if self.output_path:
			name_list = [self.name_list_widget.item(index).text() for index in range(self.name_list_widget.count())]

			pdf_generator = Testimony_Cart_PDF_Generator(self.output_path, title, img_path, name_list)
			pdf_generator.generate_pdf()
			QMessageBox.information(self, "PDF Generated", "PDF has been generated successfully!")

	def update_preview(self):
		title = self.title_entry.text()
		img_path = self.img_entry.text()
		output_temp = os.path.join(self.current_path, "temp.pdf.temp")
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
