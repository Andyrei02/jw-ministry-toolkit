import os

from PyQt5.QtWidgets import QMessageBox
from pdf_generator_module.testimony_cart_generator import Testimony_Cart_PDF_Generator
from config import Config


class CartGenerator:
    def __init__(self):
        self.config = Config()
        self.current_path = self.config.current_path

    def generate_cart_pdf(self):
        title = self.main_window.title_entry.text()
        img_path = self.main_window.img_entry.text()
        output_path = self.main_window.output_entry.text()

        if output_path:
            name_list = [self.main_window.name_list_widget.item(index).text() for index in range(self.main_window.name_list_widget.count())]

            pdf_generator = Testimony_Cart_PDF_Generator(output_path, title, img_path, name_list)
            pdf_generator.generate_pdf()

            QMessageBox.information(self.main_window, "PDF Generated", "PDF has been generated successfully!")

    def update_preview(self):
        title = self.title_entry.text()
        img_path = self.img_entry.text()
        output_temp = os.path.join(self.current_path, "temp.pdf.temp")
        name_list = [self.name_list_widget.item(index).text() for index in range(self.name_list_widget.count())]

        pdf_generator = Testimony_Cart_PDF_Generator(output_temp, title, img_path, name_list)
        pdf_generator.generate_pdf()

        scene = self.pdf_preview.scene()
        scene.clear()

        # Load PDF using PyMuPDF
        pdf_document = fitz.open(output_temp)
        first_page = pdf_document[0]
        pixmap = first_page.get_pixmap()  # Adjust the scale as needed   matrix=fitz.Matrix(2, 2)

        # Convert pixmap to QImage and display in QGraphicsView
        q_image = QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_image)

        targete_size = self.pdf_preview.size()
        pixmap = pixmap.scaled(targete_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.pdf_preview.setScene(scene)

        # Remove temp file
        try:
            os.remove(output_temp)
        except OSError as e:
            pass
