from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDateEdit, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QDate
from PyQt5 import uic

from datetime import datetime, timedelta
import time

import os
import re


class DateRangeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Date Range Selector")

        self.current_path = os.path.dirname(__file__)
        ui_path = os.path.join(self.current_path, 'ui.ui')
        uic.loadUi(ui_path, self)
        
        self.max_column = 15

        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        
        self.update_date_btn.clicked.connect(self.select_date_range)
        self.add_new_row_btn.clicked.connect(self.add_new_row)
    
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

    def add_new_row(self):
        print('add row to frame_select_order')
        for row in range(12):
            row += 1
            new_line = QLineEdit(self.frame_select_order)
            line_name = f'line_{row}'
            new_line.setObjectName(line_name)
            self.gridLayout.addWidget(new_line, row, 0, 1, 1)

            for column in range(self.max_column):
                column += 1
                combo_item = QComboBox(self.frame_select_order)
                combo_item.addItem("")
                combo_item.addItem("")
                combo_item.addItem("")
                combo_name = f"combo_{row}_{column}"
                combo_item.setObjectName(combo_name)
                self.gridLayout.addWidget(combo_item, row, column, 1, 1)
                combo_item.setItemText(0, "None")
                combo_item.setItemText(1, "man of order")
                combo_item.setItemText(2, "microphone")


if __name__ == "__main__":
    app = QApplication([])
    date_range_selector = DateRangeSelector()
    date_range_selector.show()
    app.exec_()
