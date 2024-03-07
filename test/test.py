from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QDateEdit, QPushButton
from PyQt5.QtCore import Qt, QDate
from PyQt5 import uic

from datetime import datetime, timedelta

import os
import re


class DateRangeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Date Range Selector")

        self.current_path = os.path.dirname(__file__)
        ui_path = os.path.join(self.current_path, 'ui.ui')
        uic.loadUi(ui_path, self)
        
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())

        self.update_date_button.clicked.connect(self.select_date_range)
    
    def select_date_range(self):
        label_list = self.frame_select_order.findChildren(QLabel)
        label_date_list = []
        for label in label_list:
            if re.match(r"label_date_\d+", label.objectName()):
                label_date_list.append(label)
                print(label.objectName())
        label_date_list = sorted(label_date_list, key=lambda x: x.objectName())

        start_date = self.start_date_edit.date()
        end_date = start_date.addDays(14)
        current_date = start_date
        date_list = []

        while current_date <= end_date:
            if current_date.dayOfWeek() == 2 or current_date.dayOfWeek() == 7:
                date_list.append(current_date.toString("dd.MM.yy"))
            current_date = current_date.addDays(1)
        
        for label_index in range(len(label_date_list)):
            label = self.frame_select_order.findChild(QLabel, label_date_list[label_index-1].objectName())
            if label is not None:
                label.setText(date_list[label_index-1])

        print(date_list)
        print("Selected Date Range:")
        print("Start Date:", self.start_date_edit.date().toString(Qt.ISODate))
        print("End Date:", self.end_date_edit.date().toString(Qt.ISODate))

if __name__ == "__main__":
    app = QApplication([])
    date_range_selector = DateRangeSelector()
    date_range_selector.show()
    app.exec_()

