import os
import json


class Config:
    def __init__(self):
        self.config_file_path = os.path.join('assets', 'config.json')
        self.config_data = self.load_config()

    def load_config(self):
        with open(self.config_file_path, 'r') as file:
            return json.load(file)

    def save_config(self):
        with open(self.config_file_path, 'w') as file:
            json.dump(self.config_data, file, indent=4)

    def get_item(self, key):
        return self.config_data.get(key)

    def set_item(self, key, value):
        self.config_data[key] = value
        self.save_config()
