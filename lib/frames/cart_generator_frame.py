import os

import fitz
import PyPDF2

from PyQt5.QtWidgets import QListWidget, QGraphicsScene, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon

from . import Testimony_Cart_PDF_Generator
from . import Config

class CartGenerator:
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.config = Config()
        self.init_ui()

    def init_ui(self):
        icon_upload = QIcon()
        icon_upload.addFile(self.config.upload_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.main_app.upload_pdf_button.setIcon(icon_upload)
        self.main_app.upload_pdf_button.setIconSize(QSize(24, 24))

        icon_plus = QIcon()
        icon_plus.addFile(self.config.plus_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.main_app.browse_img_button.setIcon(icon_plus)
        self.main_app.browse_img_button.setIconSize(QSize(24, 24))

        self.main_app.add_name_button.setIcon(icon_plus)
        self.main_app.add_name_button.setIconSize(QSize(24, 24))

        icon_remove = QIcon()
        icon_remove.addFile(self.config.remove_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.main_app.remove_name_button.setIcon(icon_remove)
        self.main_app.remove_name_button.setIconSize(QSize(24, 24))

        icon_save = QIcon()
        icon_save.addFile(self.config.save_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.main_app.generate_cart_button.setIcon(icon_save)
        self.main_app.generate_cart_button.setIconSize(QSize(24, 24))

        icon_folder = QIcon()
        icon_folder.addFile(self.config.folder_ico_path, QSize(), QIcon.Normal, QIcon.Off)
        self.main_app.browse_output_button.setIcon(icon_folder)
        self.main_app.browse_output_button.setIconSize(QSize(24, 24))

        self.main_app.upload_pdf_button.clicked.connect(self.upload_pdf_cart)
        self.main_app.name_entry.returnPressed.connect(self.add_name)
        self.main_app.add_name_button.clicked.connect(self.add_name)
        self.main_app.name_list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.main_app.remove_name_button.clicked.connect(self.remove_name)
        self.main_app.browse_img_button.clicked.connect(self.browse_image)
        self.main_app.browse_output_button.clicked.connect(self.browse_output)
        self.main_app.generate_cart_button.clicked.connect(self.generate_cart_pdf)
        self.main_app.title_entry.installEventFilter(self.main_app)
        self.main_app.img_entry.installEventFilter(self.main_app)
        self.main_app.pdf_preview.setScene(QGraphicsScene())
        self.main_app.pdf_preview.setAlignment(Qt.AlignCenter)

    def eventFilter(self, obj, event):
        if obj in (self.main_app.title_entry, self.main_app.img_entry):
            if event.type() == event.FocusOut:
                self.update_preview()

    def upload_pdf_cart(self):
        pdf_path, _ = QFileDialog.getOpenFileName(self.main_app, "Select pdf file", "", "pdf Files (*.pdf)")
        if pdf_path:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                page = pdf_reader.pages[0]
                text = page.extract_text()
            list_names = text.split('\n')
            list_names = [item for item in list_names if not (any(char.isdigit() for char in item) or item == "")]
            self.main_app.title_entry.setText(list_names[0])
            self.add_name(list_names[1:])

    def add_name(self, list_names=None):
        if not list_names:
            name = self.main_app.name_entry.text().strip()
            if name:
                self.main_app.name_list_widget.addItem(name)
                self.main_app.name_entry.clear()
        else:
            for name in list_names:
                if name:
                    self.main_app.name_list_widget.addItem(name)
        self.update_preview()

    def remove_name(self):
        selected_items = self.main_app.name_list_widget.selectedItems()
        for item in selected_items:
            self.main_app.name_list_widget.takeItem(self.main_app.name_list_widget.row(item))
        self.update_preview()

    def browse_image(self):
        img_path, _ = QFileDialog.getOpenFileName(self.main_app, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if img_path:
            self.main_app.img_entry.setText(img_path)
        self.update_preview()

    def browse_output(self):
        output_path, _ = QFileDialog.getSaveFileName(self.main_app, "Save PDF", "", "PDF Files (*.pdf)")
        if output_path:
            self.main_app.output_entry.setText(output_path)

    def generate_cart_pdf(self):
        title = self.main_app.title_entry.text()
        img_path = self.main_app.img_entry.text()
        output_path = self.main_app.output_entry.text()
        if output_path:
            name_list = [self.main_app.name_list_widget.item(index).text() for index in range(self.main_app.name_list_widget.count())]
            pdf_generator = Testimony_Cart_PDF_Generator(output_path, title, img_path, name_list)
            pdf_generator.generate_pdf()
            QMessageBox.information(self.main_app, "PDF Generated", "PDF has been generated successfully!")

    def update_preview(self):
        title = self.main_app.title_entry.text()
        img_path = self.main_app.img_entry.text()
        output_temp = os.path.join(self.config.temp_path, "temp.pdf.temp")
        name_list = [self.main_app.name_list_widget.item(index).text() for index in range(self.main_app.name_list_widget.count())]

        pdf_generator = Testimony_Cart_PDF_Generator(output_temp, title, img_path, name_list)
        pdf_generator.generate_pdf()

        scene = self.main_app.pdf_preview.scene()
        scene.clear()

        # Load PDF using PyMuPDF
        pdf_document = fitz.open(output_temp)
        first_page = pdf_document[0]
        pixmap = first_page.get_pixmap()  # Adjust the scale as needed   matrix=fitz.Matrix(2, 2)

        # Convert pixmap to QImage and display in QGraphicsView
        q_image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_image)

        targete_size = self.main_app.pdf_preview.size()
        pixmap = pixmap.scaled(targete_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.main_app.pdf_preview.setScene(scene)

        # Remove temp file
        try:
            os.remove(output_temp)
        except OSError as e:
            pass
