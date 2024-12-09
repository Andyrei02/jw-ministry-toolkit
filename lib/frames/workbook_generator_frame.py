import os
import requests
import aiohttp
import asyncio
import base64

from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget, QFrame, QLabel, QPushButton, QLineEdit, QScrollArea, QGridLayout, QVBoxLayout, QCheckBox, QFileDialog, QCompleter
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, pyqtSignal, QObject, Qt, QSize, QByteArray
from PyQt5.QtGui import QFont, QPixmap

from . import Parse_Meeting_WorkBook
from . import Service_Workbook_PDF_Generator
from . import Parse_List_Meeting_WorkBooks
from . import Config


class WorkbookGenerator:
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.config = Config()
        self.jw_domain = 'https://www.jw.org'
        self.checked_checkboxes = []
        self.data_dict = {}
        self.data_dict_workbooks_list = self.config.load_json(self.config.workbooks_dict_json_path)
        self.modifed_data_dict = {}
        self.Show_tabs_value = True


        for title in list(self.data_dict_workbooks_list.keys()):
            self.show_workbooks_list(title, self.data_dict_workbooks_list)

        self.init_ui()
        self.names_list = self.config.names_dict

    def init_ui(self):
        self.main_app.generate_workbook_button.clicked.connect(self.generate_workbook_pdf)
        self.main_app.button_parsing_workbook.clicked.connect(self.parsing_workbook)
        self.main_app.update_workbook_list_btn.clicked.connect(self.update_workbook_list)
        self.main_app.hiden_tabs_button.clicked.connect(self.show_hide_tabs)

    def show_hide_tabs(self):
        self.main_app.frame_tabs_workbook.setHidden(self.Show_tabs_value)
        if self.Show_tabs_value:
            self.Show_tabs_value = False 
        else:
            self.Show_tabs_value = True

    def update_workbook_list(self):
        url = "https://www.jw.org/ro/biblioteca/caiet-pentru-intrunire/?contentLanguageFilter=ro&pubFilter=mwb&yearFilter="
        self.worker_thread = WorkerThreadList_Meeting_WorkBooks(self.main_app, domain=self.jw_domain, url=url)
        self.worker_thread.finished.connect(self.on_update_workbook_list_finished)
        self.worker_thread.start()
        self. worker_thread.startProgress()

    def on_update_workbook_list_finished(self):
        self.main_app.progressbar_parse_workbook_list.setRange(0, 1)
        self.main_app.progressbar_parse_workbook_list.setValue(1)
        self.data_dict_workbooks_list = dict(self.worker_thread.data_dict)
        self.save_workbooks_dict(self.data_dict_workbooks_list)
        
        for title in list(self.data_dict_workbooks_list.keys()):
            self.show_workbooks_list(title, self.data_dict_workbooks_list)

    def save_workbooks_dict(self, data):
        self.config.write_json(self.config.workbooks_dict_json_path, data)

    def show_workbooks_list(self, title, data_dict_workbooks_list):
        frame = QFrame(self.main_app.workbooks_list_frame)
        x = 80
        y = 75
        frame.setMinimumSize(QSize(x, y))
        frame.setStyleSheet(u"background-color: rgb(68, 68, 68);")
        frame.setFrameShape(QFrame.StyledPanel)
        self.main_app.horizontalLayout_12.addWidget(frame)

        img = QLabel()
        byte_img = base64.b64decode(data_dict_workbooks_list[title][1])
        byte_array = QByteArray(byte_img)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        img.setPixmap(pixmap.scaled(x, y, Qt.KeepAspectRatio))

        label = QLabel(title, alignment=Qt.AlignCenter)
        label.setWordWrap(True)
        label.setFont(QFont('Arial', 10))

        title_btn = QPushButton("Select")
        title_btn.setStyleSheet(u"text-align: center; background-color: rgb(42, 42, 42);")
        title_btn.clicked.connect(lambda: self.select_workbook(title))

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(5,5,5,0)
        layout.addWidget(img, 0, Qt.AlignCenter|Qt.AlignTop)
        layout.addWidget(label, 0, Qt.AlignBottom)
        layout.addWidget(title_btn, 0, Qt.AlignBottom)

    def select_workbook(self, title):
        self.main_app.entry_link_workbook.setText(self.data_dict_workbooks_list[title][0])
        self.main_app.workbook_selected_label.setText(title)

    def show_workbook(self, checked_checkboxes=None):
        self.main_app.work_book_content_widget.clear()
        if not checked_checkboxes:
            data_dict = self.data_dict
        else:
            data_dict = {key: value for key, value in self.data_dict.items() if key in checked_checkboxes}
        self.modifed_data_dict = data_dict
        list_checkboxes = list(self.data_dict)
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
            line_edit = QLineEdit()
            grid_layout_1.addWidget(line_edit, row, 1, 1, 1)
            self.add_completion(line_edit)
            row += 1

            header_dict = data_dict[list_tabs[tab_index]]['header']
            for item in list(header_dict.keys())[1:]:
                label_item = QLabel(item)
                label_item.setWordWrap(True)
                label_item.setMaximumWidth(label_width)

                grid_layout_1.addWidget(label_item, row, 0, 1, 1)
                line_edit = QLineEdit()
                grid_layout_1.addWidget(line_edit, row, 1, 1, 1)
                self.add_completion(line_edit)
                row += 1

            # Section Intro
            # =========================
            intro_dict = data_dict[list_tabs[tab_index]]['intro']
            for item in list(intro_dict.keys()):
                label_item = QLabel(item)
                label_item.setWordWrap(True)
                label_item.setMaximumWidth(label_width)

                grid_layout_1.addWidget(label_item, row, 0, 1, 1)
                line_edit = QLineEdit()
                grid_layout_1.addWidget(line_edit, row, 1, 1, 1)
                self.add_completion(line_edit)
                row += 1

            section_0_label = QLabel('COMORI DIN CUVÂNTUL LUI DUMNEZEU')
            section_0_label.setStyleSheet("background-color: rgb(48, 102, 111);")
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
                line_edit = QLineEdit()
                grid_layout_1.addWidget(line_edit, row, 1, 1, 1)
                self.add_completion(line_edit)
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
                line_edit = QLineEdit()
                grid_layout_1.addWidget(line_edit, row, 1, 1, 1)
                self.add_completion(line_edit)
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
                line_edit = QLineEdit()
                grid_layout_1.addWidget(line_edit, row, 1, 1, 1)
                self.add_completion(line_edit)
                row += 1

            tab_layout.addWidget(scroll_area)

            # Set the QVBoxLayout as the main layout of the tab
            tab.setLayout(tab_layout)

            # Add the tab to the tab widget
            self.main_app.work_book_content_widget.addTab(tab, list_tabs[tab_index])
        if not checked_checkboxes:
            self.add_checkboxes(list_checkboxes)

    def add_completion(self, line_edit):
        completer = QCompleter(self.names_list, line_edit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        line_edit.setCompleter(completer)

    def add_checkboxes(self, list_weeks):
        font = QFont()
        font.setFamily(u'Open Sans')
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.grid_layout_check = QGridLayout(self.main_app.frame_select_out_week)
        def create_checkbox(row, cols, name, font):
            checkBox = QCheckBox(self.main_app.frame_select_out_week)
            checkBox.setChecked(True)
            checkBox.stateChanged.connect(self.get_checked_checkboxes)
            checkBox.setObjectName(name)
            checkBox.setFont(font)
            checkBox.setText(name)
            checkBox.setStyleSheet("QCheckBox { spacing: 5px; color: white; }\
                                QCheckBox::indicator { width: 20px; height: 20px; border: 2px solid #666; border-radius: 4px; background-color: #333333; }\
                                QCheckBox::indicator:checked { background-color: #4e4c48; border: 2px solid #007BFF; }\
                                QCheckBox::hover { border: 2px solid #4e4c48; }")
            self.grid_layout_check.addWidget(checkBox, row, cols, 1, 1)
            self.checked_checkboxes.append(name)

        len_weeks = len(list_weeks)
        list_num_weeks = list(range(0, len_weeks))
        matrix_weeks = [list_num_weeks[i:i + 2] for i in range(0, len_weeks, 2)]

        for row_index in range(len(matrix_weeks)):
            create_checkbox(row_index, 0, list_weeks[matrix_weeks[row_index][0]], font)
            if len(matrix_weeks[row_index]) == 2:
                create_checkbox(row_index, 1, list_weeks[matrix_weeks[row_index][1]], font)

    def get_checked_checkboxes(self, state):
        sender = self.main_app.sender()

        if state == 2:
            self.checked_checkboxes.append(sender.text())
            # Call your function here
        else:
            self.checked_checkboxes.remove(sender.text())
            # Call your function here

        self.checked_checkboxes = self.sort_list_by_dates(self.checked_checkboxes)
        self.show_workbook(self.checked_checkboxes)

    def sort_list_by_dates(self, date_list):
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

        sorted_list = sorted(date_list, key=custom_sort)
        return sorted_list

    def update_names_list(self, line_edit_list):
        updated_list = list(set(self.names_list + line_edit_list))
        final_dict = {'names': updated_list}
        self.config.write_json(self.config.names_path, final_dict)

    def generate_workbook_pdf(self):
        names_list = []
        for tab_index in range(self.main_app.work_book_content_widget.count()):
            # list_data = []
            tab_title = self.main_app.work_book_content_widget.tabText(tab_index)

            tab_widget = self.main_app.work_book_content_widget.widget(tab_index)

            label_list = tab_widget.findChildren(QLabel)
            label_list = [label.text() for label in label_list]

            if 'COMORI DIN CUVÂNTUL LUI DUMNEZEU' in label_list or 'SĂ FIM MAI EFICIENȚI ÎN PREDICARE' in label_list or 'VIAȚA DE CREȘTIN' in label_list:
                label_list = list(filter(lambda x: x not in ['COMORI DIN CUVÂNTUL LUI DUMNEZEU', 'SĂ FIM MAI EFICIENȚI ÎN PREDICARE', 'VIAȚA DE CREȘTIN'], label_list))

            line_edit_list = tab_widget.findChildren(QLineEdit)
            line_edit_list = [line_edit.text() for line_edit in line_edit_list]
            names_list += line_edit_list

            date_list = list(self.modifed_data_dict.keys())
            # for date_index in range(len(date_list)):
            header_dict = self.modifed_data_dict[date_list[tab_index]]["header"]
            intro_dict = self.modifed_data_dict[date_list[tab_index]]["intro"]
            section_1_dict = self.modifed_data_dict[date_list[tab_index]]["section_1"]
            section_2_dict = self.modifed_data_dict[date_list[tab_index]]["section_2"]
            section_3_dict = self.modifed_data_dict[date_list[tab_index]]["section_3"]
            
            header_dict[list(header_dict.keys())[0]][1] = line_edit_list[label_list.index("Președinte")]
            for section_key in list(intro_dict.keys()):
                intro_dict[section_key][1] = (line_edit_list[label_list.index(section_key)])
            
            for section_key in list(section_1_dict.keys()):
                section_1_dict[section_key][1] = (line_edit_list[label_list.index(section_key)])
            
            for section_key in list(section_2_dict.keys()):
                section_2_dict[section_key][1] = (line_edit_list[label_list.index(section_key)])
            
            for section_key in list(section_3_dict.keys()):
                section_3_dict[section_key][1] = (line_edit_list[label_list.index(section_key)])

        self.update_names_list(names_list)

        output_path = self.browse_output() # self.config.out_workbook_path

        if output_path:
            service_schedule = Service_Workbook_PDF_Generator(template_dir=self.config.templates_path)
            data = self.modifed_data_dict.copy()
            service_schedule.generate_pdf(data, output_pdf=output_path)
            print(self.modifed_data_dict)
            QMessageBox.information(self.main_app, "PDF Generated", "PDF has been generated successfully!")

    def browse_output(self):
        output_path, _ = QFileDialog.getSaveFileName(self.main_app, "Save PDF", "", "PDF Files (*.pdf)")
        return output_path

    def parsing_workbook(self):
        self.main_app.button_parsing_workbook.setEnabled(False)

        site_domain = 'https://www.jw.org'
        workbook_url = self.main_app.entry_link_workbook.text()
        self.save_link(workbook_url)

        self.worker_thread = WorkerThreadMeeting_WorkBook(self.main_app, self.jw_domain, workbook_url)
        self.worker_thread.download_progress_signal.connect(self.update_download_progress)
        self.worker_thread.finished.connect(self.parsing_finished)
        self.worker_thread.start()

    def save_link(self, url):
        pass

    def update_download_progress(self, value):
        self.main_app.progressbar_workbook.setValue(value)
        # self.progress_label.setText(f"Downloading: {value}%")

    def parsing_finished(self):
        self.main_app.button_parsing_workbook.setEnabled(True)
        self.data_dict = self.worker_thread.data_dict
        self.show_workbook()


class WorkerThreadList_Meeting_WorkBooks(QThread):
    finished = pyqtSignal()  # Define a custom signal

    def __init__(self, main_app, domain, url):
        super().__init__()
        self.main_app = main_app
        self.domain = domain
        self.url = url
        self.data_dict = {}

    def run(self):
        parser = Parse_List_Meeting_WorkBooks(self.domain, self.url)
        try:
            self.data_dict = asyncio.run(parser.get_dict_data())
        except aiohttp.client_exceptions.InvalidURL:
            print("Error! Please enter correct link in link tab.")
            QMessageBox.information(self.main_app, "Info Download", "Error! Please enter correct lik in link tab.")
        except aiohttp.client_exceptions.ClientConnectorError:
            print("Connection Error! Please check your connection")
            QMessageBox.information(self.main_app, "Info Download", "Connection Error! Please check your connection")
        self.finished.emit()  # Emit the finished signal when done

    def startProgress(self):
        self.main_app.progressbar_parse_workbook_list.setRange(0, 0)  # Indeterminate mode


class WorkerThreadMeeting_WorkBook(QThread):
    download_progress_signal = pyqtSignal(int)

    def __init__(self, main_app, domain, url):
        super().__init__()
        self.main_app = main_app
        self.domain = domain
        self.url = url
        self.data_dict = {}

    def run(self):
        self.parser = Parse_Meeting_WorkBook(self.domain, self.url)
        self.parser.download_progress_signal.connect(self.download_progress_signal.emit)

        try:
            self.data_dict = asyncio.run(self.parser.get_dict_data())
        except aiohttp.client_exceptions.InvalidURL:
            QMessageBox.information(self.main_app, "Info Download", "Error! Please enter correct lik in link tab.")
        except aiohttp.client_exceptions.ClientConnectorError:
            QMessageBox.information(self.main_app, "Info Download", "Connection Error! Please check your connection")

    def emit_download_progress(self, value):
        self.download_progress_signal.emit(value)

    def emit_parse_progress(self, value):
        self.parse_progress_signal.emit(value)

