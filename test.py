from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit

class AutoCompleteLineEdit(QLineEdit):
    def __init__(self, word_list, parent=None):
        super().__init__(parent)
        self.word_list = word_list

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.tab_complete()
            event.accept()
        else:
            super().keyPressEvent(event)

    def complete_word(self):
        current_text = self.text().lower()
        for word in self.word_list:
            if word.lower().startswith(current_text):
                completion = word[len(current_text):]
                self.setPlaceholderText(completion)
                break
        else:
            self.setPlaceholderText("")

    def tab_complete(self):
        current_text = self.text().lower()
        for word in self.word_list:
            if word.lower().startswith(current_text):
                self.setText(word)
                self.setSelection(len(current_text), len(word))
                break


import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class WordCompletionDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Completion Demo")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.word_list = self.load_names_from_json("resources/names_dict.json")

        self.input_field = AutoCompleteLineEdit(self.word_list)
        self.input_field1 = AutoCompleteLineEdit(self.word_list)
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.input_field1)

        self.input_field.textChanged.connect(self.input_field.complete_word)
        self.input_field.returnPressed.connect(self.finish_word)
        self.input_field1.textChanged.connect(self.input_field1.complete_word)
        self.input_field1.returnPressed.connect(self.finish_word)

    def load_names_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if "names" in data:
                return data["names"]
            else:
                return []

    def finish_word(self):
        current_text = self.input_field.text().lower()
        for word in self.word_list:
            if word.lower() == current_text:
                return  # Word is already complete
        for word in self.word_list:
            if word.lower().startswith(current_text):
                self.input_field.setText(word)
                self.input_field.setSelection(len(current_text), len(word))
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = WordCompletionDemo()
    demo.show()
    sys.exit(app.exec_())
