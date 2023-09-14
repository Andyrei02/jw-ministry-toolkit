import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QMessageBox, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
import fitz

from pdf_generator import Testimony_Cart_PDF_Generator


class PDFGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.getcwd(), 'assets', 'ui', 'ui.ui')
        uic.loadUi(ui_path, self)

        self.init_ui()
        ## loading style file
        with open(os.path.join('assets', 'ui', 'stylesheet.qss'), 'r') as style_file:
            style_str = style_file.read()
        self.setStyleSheet(style_str)


    def init_ui(self):
        self.full_menu_widget.setHidden(True)
        self.default_title = 'Mărturia cu căruciorul'
        self.output_path = None

        self.set_cart_widget()

        self.name_entry.returnPressed.connect(self.add_name)
        self.add_name_button.clicked.connect(self.add_name)
        self.name_list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.remove_name_button.clicked.connect(self.remove_name)
        self.browse_img_button.clicked.connect(self.browse_image)
        self.browse_output_button.clicked.connect(self.browse_output)
        self.generate_cart_button.clicked.connect(self.generate_pdf)

        self.cart_widget_btn.clicked.connect(self.set_cart_widget)
        self.group_list_widget_btn.clicked.connect(self.set_group_list_widget)

        self.title_entry.installEventFilter(self)
        self.img_entry.installEventFilter(self)

        self.pdf_preview.setScene(QGraphicsScene())
        self.pdf_preview.setAlignment(Qt.AlignCenter)

    def set_cart_widget(self):
        self.cart_widget_btn.setStyleSheet('#cart_widget_btn{ background-color: #3b434f;}')
        self.group_list_widget_btn.setStyleSheet('')
        self.stackedWidget.setCurrentIndex(0)

    def set_group_list_widget(self):
        self.group_list_widget_btn.setStyleSheet('#group_list_widget_btn{ background-color: #3b434f;}')
        self.cart_widget_btn.setStyleSheet('')
        self.stackedWidget.setCurrentIndex(1)

    def eventFilter(self, obj, event):
        if obj in (self.title_entry, self.img_entry):
            if event.type() == event.FocusOut:
                self.update_preview()

        return super().eventFilter(obj, event)

    def browse_image(self):
        img_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if img_path:
            self.img_entry.setText(img_path)

        self.update_preview()

    def browse_output(self):
        self.output_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if self.output_path:
            self.output_entry.setText(self.output_path)

    def add_name(self):
        name = self.name_entry.text().strip()
        if name:
            self.name_list_widget.addItem(name)
            self.name_entry.clear()

        self.update_preview()

    def remove_name(self):
        selected_items = self.name_list_widget.selectedItems()
        for item in selected_items:
            self.name_list_widget.takeItem(self.name_list_widget.row(item))

        self.update_preview()



    def generate_pdf(self):
        title = self.title_entry.text()
        img_path = self.img_entry.text()
        self.output_path = self.output_entry.text()
        name_list = [self.name_list_widget.item(index).text() for index in range(self.name_list_widget.count())]

        pdf_generator = Testimony_Cart_PDF_Generator(self.output_path, title, img_path, name_list)
        pdf_generator.generate_pdf()
        QMessageBox.information(self, "PDF Generated", "PDF has been generated successfully!")


    def update_preview(self):
        title = self.title_entry.text()
        img_path = self.img_entry.text()
        output_temp = os.path.join(os.getcwd(), "temp.pdf.temp")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = PDFGeneratorApp()
    main_window.show()

    sys.exit(app.exec_())


# Change theme