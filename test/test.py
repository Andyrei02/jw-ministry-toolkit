from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDateEdit, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QDate
from PyQt5 import uic

from datetime import datetime, timedelta
import time
from test.pdf_generate import ServideScheduleGenerator

from config import Config

import os
import re


class DateRangeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Date Range Selector")
        self.config = Config()
        self.current_path = self.config.current_path
        ui_path = os.path.join(self.current_path, 'test', 'ui.ui')
        uic.loadUi(ui_path, self)
        
        self.max_column = 15
        self.dict_rows = {}
        self.date_list = []

        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        
        self.update_date_btn.clicked.connect(self.select_date_range)
        self.add_new_row_btn.clicked.connect(self.add_new_row)
        self.generate_service_schedule_pdf_btn.clicked.connect(self.generate_service_schedule_pdf)
    
    def select_date_range(self):
        label_date_list = []
        for column_date in range(self.max_column):
            column_date += 1
            label_date = QLabel(self.frame_select_order)
            label_date_name = f"label_date_{column_date}"
            label_date.setObjectName(label_date_name)
            label_date.setAlignment(Qt.AlignCenter)
            self.gridLayout.addWidget(label_date, 0, column_date, 1, 1, Qt.AlignTop)
            label_date_list.append(label_date_name)

        start_date = self.start_date_edit.date()
        end_date = start_date.addDays(98)
        current_date = start_date
        date_list = []

        while current_date <= end_date:
            if current_date.dayOfWeek() == 2 or current_date.dayOfWeek() == 7:
                date_list.append(current_date.toString("dd.MM.yy"))
            current_date = current_date.addDays(1)
        
        for label_index in range(len(label_date_list)):
            label = self.frame_select_order.findChild(QLabel, label_date_list[label_index-1])
            if label is not None:
                label.setText(date_list[label_index-1])
        self.date_list = date_list

    def add_new_row(self):
        if self.dict_rows:
            row = len(self.dict_rows.items())+1
        else:
            row = 1

        new_line = QLineEdit(self.frame_select_order)
        line_name = f'line_{row}'
        new_line.setObjectName(line_name)
        self.gridLayout.addWidget(new_line, row, 0, 1, 1)

        list_columns = []
        for column in range(self.max_column):
            column += 1
            combo_item = QComboBox(self.frame_select_order)
            combo_item.addItem("")
            combo_item.addItem("")
            combo_item.addItem("")
            combo_item.addItem("")
            combo_name = f"combo_{row}_{column}"
            combo_item.setObjectName(combo_name)
            self.gridLayout.addWidget(combo_item, row, column, 1, 1)
            combo_item.setItemText(0, "None")
            combo_item.setItemText(1, "man of order")
            combo_item.setItemText(2, "microphone")
            combo_item.setItemText(3, "equalizer")

            list_columns.append(combo_item)
        self.dict_rows[new_line] = list_columns

    def generate_service_schedule_pdf(self):
        final_dict = {}
        for line_edit, combo_boxes in self.dict_rows.items():
            text = line_edit.text()
            if text:
                final_dict[text] = [cb.currentText() for cb in combo_boxes]

        title = "Grafic de Serviciu"
        subtitle = "Microfon / Om de ordine / Sistem de sonorizare"
        output_path = os.path.join(self.current_path, 'test.pdf')
        serv_sched_Gen = ServideScheduleGenerator(output_path, title, subtitle, self.date_list, final_dict)
        serv_sched_Gen.generate_pdf()
        print(self.date_list)
        print(final_dict)


def main():
    app = QApplication([])
    date_range_selector = DateRangeSelector()
    date_range_selector.show()
    app.exec_()
