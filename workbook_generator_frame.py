import os
import requests

from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget, QLabel, QLineEdit, QScrollArea, QGridLayout, QVBoxLayout, QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont

from parse_workbook import Parse_Meeting_WorkBook
from pdf_generator_module.service_workbook_generator import Service_Workbook_PDF_Generator



class WorkbookGenerator:
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.current_path = self.main_app.config.current_path
        self.checked_checkboxes = []
        self.data_dict = {}
        self.modifed_data_dict = {}
        self.init_ui()

    def init_ui(self):
        self.main_app.generate_workbook_button.clicked.connect(self.generate_workbook_pdf)
        self.main_app.button_parsing_workbook.clicked.connect(self.parsing_workbook)

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
            grid_layout_1.addWidget(QLineEdit(), row, 1, 1, 1)
            row += 1

            header_dict = data_dict[list_tabs[tab_index]]['header']
            for item in list(header_dict.keys())[1:]:
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
            self.main_app.work_book_content_widget.addTab(tab, list_tabs[tab_index])
        if not checked_checkboxes:
            self.add_checkboxes(list_checkboxes)

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

    def generate_workbook_pdf(self):
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

        output_path = os.path.join(self.current_path, 'file.pdf')
        congregation = 'GLODENI-SUD'

        service_schedule = Service_Schedule_PDF_Generator(output_path, congregation, self.modifed_data_dict)
        service_schedule.generate_pdf()
        QMessageBox.information(self.main_app, "PDF Generated", "PDF has been generated successfully!")

    def parsing_workbook(self):
        self.main_app.button_parsing_workbook.setEnabled(False)

        site_domain = 'https://www.jw.org'
        workbook_url = self.main_app.entry_link_workbook.text()
        self.save_link(workbook_url)

        self.worker_thread = WorkerThread(self.main_app, site_domain, workbook_url)
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


class WorkerThread(QThread):
    download_progress_signal = pyqtSignal(int)  # Add this line

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
            self.data_dict = self.parser.get_dict_data()
        except requests.exceptions.MissingSchema:
            QMessageBox.information(self.main_app, "Info Download", "Error! Please enter correct lik in link tab.")
        except requests.exceptions.ConnectionError:
            QMessageBox.information(self.main_app, "Info Download", "Connection Error! Please check your connection")

    def emit_download_progress(self, value):
        self.download_progress_signal.emit(value)

    def emit_parse_progress(self, value):
        self.parse_progress_signal.emit(value)

