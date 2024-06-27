import configparser
import json
import os
import sys


class Config:
    def __init__(self):
        if getattr(sys, "frozen", False):
            self.main_path = os.path.dirname(os.path.dirname(sys.executable))
        else:
            self.main_path = os.path.dirname(os.path.dirname(__file__))

        self.temp_path = os.path.join(self.main_path, "temp_files")
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)
        self.names_path = os.path.join(
            self.main_path, "resources", "names_dict.json"
        )

        try:
            self.names_dict = self.load_names_from_json(self.names_path)
        except  FileNotFoundError:
            self.write_json(self.names_path, {"names": []})
            self.names_dict = self.load_names_from_json(self.names_path)

        self.workbooks_dict_json_path = os.path.join(
            self.main_path, "resources", "workbooks_dict.json"
        )
        try:
            self.workbooks_dict_json = self.load_workbook_from_json(
                self.workbooks_dict_json_path
            )
        except FileNotFoundError:
            self.write_json(self.workbooks_dict_json_path, {})

        self.ui_path = os.path.join(
            self.main_path, "resources", "ui_design", "user_interface.ui"
        )
        self.styles_path = os.path.join(
            self.main_path, "resources", "ui_design", "stylesheets"
        )
        self.config_file_path = os.path.join(
            self.main_path, "resources", "config.ini"
        )
        self.out_workbook_path = os.path.join(self.temp_path, "workbook.pdf")
        self.out_service_chedule_path = os.path.join(
            self.temp_path, "service_chedule.pdf"
        )

        self.bg_workbook_ico_path = os.path.join(
            self.main_path, "resources", "images", "bg_workbook.png"
        )
        self.section_1_ico_path = os.path.join(
            self.main_path, "resources", "images", "section_1_icon.png"
        )
        self.section_2_ico_path = os.path.join(
            self.main_path, "resources", "images", "section_2_icon.png"
        )
        self.section_3_ico_path = os.path.join(
            self.main_path, "resources", "images", "section_3_icon.png"
        )

        self.calibri_regular_path = os.path.join(
            self.main_path, "resources", "font", "Calibri_Regular.ttf"
        )
        self.calibri_bold_path = os.path.join(
            self.main_path, "resources", "font", "Calibri_Bold.TTF"
        )
        self.cambria_bold_path = os.path.join(
            self.main_path, "resources", "font", "Cambria_Bold.ttf"
        )

        self.upload_ico_path = os.path.join(
            self.main_path, "resources", "images", "upload.png"
        )
        self.plus_ico_path = os.path.join(
            self.main_path, "resources", "images", "plus.png"
        )
        self.remove_ico_path = os.path.join(
            self.main_path, "resources", "images", "remove.png"
        )
        self.folder_ico_path = os.path.join(
            self.main_path, "resources", "images", "folder.png"
        )
        self.save_ico_path = os.path.join(
            self.main_path, "resources", "images", "save.png"
        )

        self.menu_ico_path = os.path.join(
            self.main_path, "resources", "images", "menu.png"
        )
        self.style_ico_path = os.path.join(
            self.main_path, "resources", "images", "style.png"
        )
        self.cart_ico_path = os.path.join(
            self.main_path, "resources", "images", "cart.png"
        )
        self.workbook_ico_path = os.path.join(
            self.main_path, "resources", "images", "workbook.png"
        )
        self.service_schedule_ico_path = os.path.join(
            self.main_path, "resources", "images", "timetable.png"
        )

        self.microphone_ico_path = os.path.join(
            self.main_path, "resources", "images", "microphone.png"
        )
        self.equalizer_ico_path = os.path.join(
            self.main_path, "resources", "images", "equalizer.png"
        )

        self.config_data = self.load_config()

    def load_workbook_from_json(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data

    def load_names_from_json(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            if "names" in data:
                return data["names"]
            else:
                return []

    def write_json(self, path, dict_items):
        with open(path, "w") as file:
            json.dump(dict_items, file)

    def load_config(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_file_path)
        return config_parser["settings"]

    def save_config(self):
        config_parser = configparser.ConfigParser()
        config_parser["settings"] = self.config_data
        with open(self.config_file_path, "w") as config_file:
            config_parser.write(config_file)

    def get_item(self, key):
        return self.config_data.get(key)

    def set_item(self, key, value):
        self.config_data[key] = value
        self.save_config()
