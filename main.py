import sys
import os
import glob
import requests

from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsPixmapItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QScrollArea, QGridLayout, QVBoxLayout, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import uic

from lib import CartGenerator
from lib import WorkbookGenerator
from lib import ServideScheduleGenerator
from lib import Config


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = Config()
        uic.loadUi(self.config.ui_path, self)
        
        ## loading style file
        self.current_theme = self.config.get_item('theme')
        with open(os.path.join(self.config.styles_path, self.current_theme+'.qss'), 'r') as style_file:
            style_str = style_file.read()
        self.setStyleSheet(style_str)

        self.init_ui()

    def init_ui(self):
        icon_menu = QIcon()
        icon_menu.addFile(self.config.menu_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.menu_btn.setIcon(icon_menu)
        self.menu_btn.setIconSize(QSize(24, 24))

        icon_style = QIcon()
        icon_style.addFile(self.config.style_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.style_btn.setIcon(icon_style)
        self.style_btn.setIconSize(QSize(24, 24))

        icon_cart = QIcon()
        icon_cart.addFile(self.config.cart_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.cart_widget_btn.setIcon(icon_cart)
        self.cart_widget_btn.setIconSize(QSize(24, 24))

        icon_workbook = QIcon()
        icon_workbook.addFile(self.config.workbook_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.workbook_widget_btn.setIcon(icon_workbook)
        self.workbook_widget_btn.setIconSize(QSize(24, 24))

        icon_service_schedule = QIcon()
        icon_service_schedule.addFile(self.config.service_schedule_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.service_schedule_widget_btn.setIcon(icon_service_schedule)
        self.service_schedule_widget_btn.setIconSize(QSize(24, 24))


        self.label_version_app.setText(f"v. {self.config.get_item('version')}") 
        self.full_menu_widget.setHidden(True)
        self.default_title = 'Mărturia cu căruciorul'

        self.cart_generator = CartGenerator(self)
        self.workbook_generator = WorkbookGenerator(self)
        self.service_schedule_generator = ServideScheduleGenerator(self)
        self.set_cart_widget()

        self.style_btn.clicked.connect(self.next_theme)
        self.cart_widget_btn.clicked.connect(self.set_cart_widget)
        self.workbook_widget_btn.clicked.connect(self.set_workbook_widget)
        self.service_schedule_widget_btn.clicked.connect(self.set_service_schedule_widget)

    def next_theme(self):
        list_themes = glob.glob(os.path.join(self.config.styles_path, '*.qss'))
        current_theme_index = list_themes.index(os.path.join(self.config.styles_path, self.current_theme+'.qss'))
        current_theme_index = list_themes.index(os.path.join(self.config.styles_path, self.current_theme + '.qss'))
        next_theme_index = (current_theme_index + 1) % len(list_themes)
        next_theme = os.path.basename(list_themes[next_theme_index])
        self.current_theme = next_theme[:-4]
        self.config.set_item('theme', self.current_theme)

        with open(os.path.join(self.config.styles_path, self.current_theme+'.qss'), 'r') as style_file:
            style_str = style_file.read()
        self.setStyleSheet(style_str)


    def set_cart_widget(self):
        self.cart_widget_btn.setEnabled(False)
        self.service_schedule_widget_btn.setEnabled(True)
        self.workbook_widget_btn.setEnabled(True)
        self.stackedWidget.setCurrentIndex(0)

    def set_workbook_widget(self):
        self.workbook_widget_btn.setEnabled(False)
        self.service_schedule_widget_btn.setEnabled(True)
        self.cart_widget_btn.setEnabled(True)
        self.stackedWidget.setCurrentIndex(1)

    def set_service_schedule_widget(self):
        self.service_schedule_widget_btn.setEnabled(False)
        self.cart_widget_btn.setEnabled(True)
        self.workbook_widget_btn.setEnabled(True)
        self.stackedWidget.setCurrentIndex(2)

    def eventFilter(self, obj, event):
        self.cart_generator.eventFilter(obj, event)
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainApp()
    main_window.show()

    sys.exit(app.exec_())
