import sys
import os
import glob
import requests

from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsPixmapItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QScrollArea, QGridLayout, QVBoxLayout, QCheckBox
from PyQt5 import uic

from cart_generator_frame import CartGenerator
from workbook_generator_frame import WorkbookGenerator
from config import Config


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

        self.cart_generator = CartGenerator(self)
        self.workbook_generator = WorkbookGenerator(self)
        self.set_cart_widget()

        self.style_btn.clicked.connect(self.next_theme)
        self.cart_widget_btn.clicked.connect(self.set_cart_widget)
        self.workbook_widget_btn.clicked.connect(self.set_workbook_widget)

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


    def set_cart_widget(self):
        self.cart_widget_btn.setEnabled(False)
        self.workbook_widget_btn.setEnabled(True)
        self.stackedWidget.setCurrentIndex(0)

    def set_workbook_widget(self):
        self.workbook_widget_btn.setEnabled(False)
        self.cart_widget_btn.setEnabled(True)
        self.stackedWidget.setCurrentIndex(1)

    def eventFilter(self, obj, event):
        self.cart_generator.eventFilter(obj, event)
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainApp()
    main_window.show()

    sys.exit(app.exec_())
