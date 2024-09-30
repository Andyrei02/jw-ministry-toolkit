from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QDateEdit, QPushButton, QLineEdit, QComboBox, QFileDialog
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QIcon
from PyQt5 import uic


from datetime import datetime, timedelta
import time
import os
import re

from .pdf_generator_module.service_schedule_generator import Service_Schedule_PDF_Generator
from .config import Config



class ServideScheduleGenerator:
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.config = Config()
        
        self.max_column = 15
        self.dict_rows = {}
        self.date_list = []

        self.main_app.start_date_edit.setCalendarPopup(True)
        self.main_app.start_date_edit.setDate(QDate.currentDate())

        icon_plus = QIcon()
        icon_plus.addFile(self.config.plus_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.main_app.add_new_row_btn.setIcon(icon_plus)
        self.main_app.add_new_row_btn.setIconSize(QSize(24, 24))
        
        self.main_app.update_date_btn.clicked.connect(self.select_date_range)
        self.main_app.add_new_row_btn.clicked.connect(self.add_new_row)
        self.main_app.generate_service_schedule_pdf_btn.clicked.connect(self.generate_service_schedule_pdf)
    
    def select_date_range(self):
        label_date_list = []
        for column_date in range(self.max_column):
            column_date += 1
            label_date = QLabel(self.main_app.frame_select_order)
            label_date_name = f"label_date_{column_date}"
            label_date.setObjectName(label_date_name)
            label_date.setAlignment(Qt.AlignCenter)
            self.main_app.gridLayout_5.addWidget(label_date, 0, column_date, 1, 1, Qt.AlignTop)
            label_date_list.append(label_date_name)

        start_date = self.main_app.start_date_edit.date()
        end_date = start_date.addDays(98)
        current_date = start_date
        date_list = []

        while current_date <= end_date:
            if current_date.dayOfWeek() == 2 or current_date.dayOfWeek() == 7:
                date_list.append(current_date.toString("dd.MM"))
            current_date = current_date.addDays(1)
        
        for label_index in range(len(label_date_list)):
            label = self.main_app.frame_select_order.findChild(QLabel, label_date_list[label_index-1])
            if label is not None:
                label.setText(date_list[label_index-1])
        self.date_list = date_list

    def add_new_row(self):
        if self.dict_rows:
            row = len(self.dict_rows.items())+1
        else:
            row = 1
        line_name = f'line_{row}'
        name = QLineEdit(self.main_app.names_list)
        name.setObjectName(line_name)
        self.main_app.verticalLayout_18.addWidget(name)

        frame_list_comboboxes = QFrame(self.main_app.scrollAreaWidgetContents_4)
        frame_list_comboboxes.setObjectName(f'frame_{row}')
        h_layout = QHBoxLayout(frame_list_comboboxes)

        combo_box = QComboBox(frame_list_comboboxes)
        h_layout.addWidget(combo_box)


        self.main_app.verticalLayout_19.addWidget(frame_list_comboboxes, 0, Qt.AlignTop)
        # new_line = QLineEdit(self.main_app.frame_select_order)
        # 
        # new_line.setObjectName(line_name)
        # self.main_app.gridLayout_5.addWidget(new_line, row, 0, 1, 1)

        # list_columns = []
        # for column in range(self.max_column):
        #     column += 1
        #     combo_item = QComboBox(self.main_app.frame_select_order)
        #     combo_item.addItem("")
        #     combo_item.addItem("")
        #     combo_item.addItem(QIcon(self.config.microphone_ico_path), "")
        #     combo_item.addItem(QIcon(self.config.equalizer_ico_path), "")
        #     combo_name = f"combo_{row}_{column}"
        #     combo_item.setObjectName(combo_name)
        #     self.main_app.gridLayout_5.addWidget(combo_item, row, column, 1, 1)
        #     combo_item.setItemText(0, "None")
        #     combo_item.setItemText(1, "man of order")
        #     combo_item.setItemText(2, "microphone")
        #     combo_item.setItemText(3, "equalizer")

        #     list_columns.append(combo_item)
        # self.dict_rows[new_line] = list_columns

    def generate_service_schedule_pdf(self):
        final_dict = {}
        for line_edit, combo_boxes in self.dict_rows.items():
            text = line_edit.text()
            if text:
                final_dict[text] = [cb.currentText() for cb in combo_boxes]

        title = "Grafic de Serviciu"
        subtitle = "Microfon / Om de ordine / Sistem de sonorizare"
        output_path = self.browse_output()

        if output_path:
            serv_sched_Gen = Service_Schedule_PDF_Generator(output_path, title, subtitle, self.date_list, final_dict)
            serv_sched_Gen.generate_pdf()

    def browse_output(self):
        output_path, _ = QFileDialog.getSaveFileName(self.main_app, "Save PDF", "", "PDF Files (*.pdf)")
        return output_path
