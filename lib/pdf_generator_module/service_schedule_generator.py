import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from . import Config


class Service_Schedule_PDF_Generator:
    def __init__(self, output_path, title=None, subtitle=None, date_list=None, names_dict=None):
        self.config = Config()
        self.page_size = landscape(A4)

        self.title = title
        self.subtitle = subtitle
        self.date_list = date_list
        self.names_dict = names_dict
        self.inv_canvas = canvas.Canvas(output_path, pagesize=self.page_size, bottomup=0)
        self.init_pdf()

    def custom_sort(self, name):
        # Split the name into first and last names
        return name.split()

    def init_pdf(self):
        pdfmetrics.registerFont(TTFont('CalibriRegular', self.config.calibri_regular_path))
        pdfmetrics.registerFont(TTFont('CalibriBold', self.config.calibri_bold_path))
        pdfmetrics.registerFont(TTFont('CambriaBold', self.config.cambria_bold_path))

    def draw_header(self):
        self.inv_canvas.setFont("CalibriBold", 35)
        self.inv_canvas.drawCentredString(self.page_size[0]/2, 40, self.title)
        self.inv_canvas.setFont("CalibriBold", 25)
        self.inv_canvas.drawCentredString(self.page_size[0]/2, 70, self.subtitle)

    def draw_table(self):
        names_list = list(self.names_dict.keys())
        max_rows = 12
        margin_table = 10
        table_pos = (margin_table, 100)
        self.inv_canvas.translate(table_pos[0], table_pos[1])

        w_table = self.page_size[0] - (margin_table * 2)
        h_table = self.page_size[1] - (table_pos[1] + margin_table)

        self.inv_canvas.roundRect(0, 0, w_table, h_table, 15, fill=0)

        if names_list:
            n_rows = min(max_rows, len(names_list))
            h_row = (h_table / n_rows)
            w_column = 100

            current_row = h_row
            for _ in range(int(n_rows - 1)):
                self.inv_canvas.line(0, current_row, w_table, current_row)
                current_row += h_row

            current_row = h_row
            current_column = 5
            current_name = 0
            longest_name_width = 0

            for row in range(int(n_rows)):
                if current_name >= len(names_list):
                    break

                current_name += 1
                self.inv_canvas.setFont("CalibriBold", 20)
                names = str(names_list[current_name - 1])
                names_group = names.split("/")
                for name in names_group:
                    name = name.strip()
                    name_width = self.inv_canvas.stringWidth(name, "CalibriBold", 20)
                    name_height = 10
                    if name_width > longest_name_width:
                        longest_name_width = name_width + 10
                    center_x = current_column
                    center_y = current_row - (h_row / 2) + 5
                    if len(names_group) > 1:
                        if name != names_group[-1].strip():
                            center_y -= name_height
                            current_row += 10
                        else:
                            current_row -= 10
                    self.inv_canvas.drawString(center_x, center_y, name)
                current_row += h_row

            self.inv_canvas.line(longest_name_width, h_table, longest_name_width, 0)

            remaining_width = w_table - (longest_name_width)  # Remaining space after longest name column
            column_width = remaining_width / 15

            self.inv_canvas.setFont("CalibriBold", 12)
            for i in range(15):
                x_start = longest_name_width + i * column_width
                self.inv_canvas.drawString(x_start, -5, self.date_list[i])
                self.inv_canvas.line(x_start, h_table, x_start, 0)

            self.inv_canvas.setFont("CalibriBold", 16)
            icon_size = min(column_width, h_row) -2
            current_row = h_row
            current_column = longest_name_width
            for name in names_list:
                cells_list = self.names_dict[name]
                for cell in cells_list:
                    cell_x = current_column
                    cell_y = current_row - h_row / 2 + 10
                    text = cell
                    if cell == "None":
                        pass
                    elif cell == "man of order":
                        text = "Om de ordine"
                        wrapped_text = self.wrap_text(text, column_width)
                        for line in wrapped_text:
                            width_line = self.inv_canvas.stringWidth(line, "CalibriBold", 16)
                            x = (cell_x + (column_width / 2) - (width_line / 2))
                            self.inv_canvas.drawString(x, cell_y, line)
                            cell_y -= 15
                    elif cell == "microphone":
                        png_image = ImageReader(self.config.microphone_ico_path)
                        self.inv_canvas.saveState()
                        self.inv_canvas.translate(cell_x, current_row-h_row)  # Translate to center of the cell
                        self.inv_canvas.rotate(180)  # Rotate the canvas 180 degrees
                        self.inv_canvas.drawImage(png_image, -(column_width/2)-(icon_size/2), -(h_row/2)-(icon_size/2), icon_size, height=icon_size, mask="auto")
                        self.inv_canvas.restoreState()
                    elif cell == "equalizer":
                        png_image = ImageReader(self.config.equalizer_ico_path)
                        self.inv_canvas.saveState()
                        self.inv_canvas.translate(cell_x, current_row-h_row)  # Translate to center of the cell
                        self.inv_canvas.rotate(180)  # Rotate the canvas 180 degrees
                        self.inv_canvas.drawImage(png_image, -(column_width/2)-(icon_size/2), -(h_row/2)-(icon_size/2), icon_size, height=icon_size, mask="auto")
                        self.inv_canvas.restoreState()
                    current_column += column_width
                current_column = longest_name_width
                current_row += h_row

        self.inv_canvas.translate(-table_pos[0], -table_pos[1])

    def wrap_text(self, text, width):
        lines = []
        words = text.split()
        current_line = ''
        for word in words:
            if not current_line:
                current_line = word
            elif self.inv_canvas.stringWidth(current_line + ' ' + word, "CalibriBold", 16) <= width:
                current_line += ' ' + word
            else:
                lines.insert(0, current_line)
                current_line = word
        if current_line:
            lines.insert(0, current_line)
        return lines

    def generate_pdf(self):
        self.draw_header()
        self.draw_table()
        self.inv_canvas.showPage()
        self.inv_canvas.save()
