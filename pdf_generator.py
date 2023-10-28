import os
from datetime import datetime, timedelta

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth

from config import Config


class Testimony_Cart_PDF_Generator:
    def __init__(self, output_path, title=None, image=None, name_list=None):
        self.config = Config()
        self.current_path = self.config.current_path

        self.title = title
        self.image = image
        self.name_list = sorted(name_list, key=self.custom_sort)
        self.inv_canvas = canvas.Canvas(output_path, pagesize=A4, bottomup=0)
        self.init_pdf()

    def custom_sort(self, name):
        # Split the name into first and last names
        return name.split()

    def init_pdf(self):
        calibri_regular_path = os.path.join(self.current_path, "assets", "font", "Calibri Regular.ttf")
        calibri_bold_path = os.path.join(self.current_path, "assets", "font", "Calibri Bold.TTF")
        cambria_bold_path = os.path.join(self.current_path, "assets", "font", "Cambria-Bold.ttf")
        pdfmetrics.registerFont(TTFont('CalibriRegular', calibri_regular_path))
        pdfmetrics.registerFont(TTFont('CalibriBold', calibri_bold_path))
        pdfmetrics.registerFont(TTFont('CambriaBold', cambria_bold_path))

    def draw_header(self):
        self.inv_canvas.setFont("CalibriBold", 35)
        self.inv_canvas.drawCentredString(A4[0]/2, 40, self.title)

        if self.image:
            img_scale = (350, 300)
            self.inv_canvas.translate(A4[0]/2, 350)
            self.inv_canvas.scale(1, -1)
            self.inv_canvas.drawImage(self.image, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1], mask='auto')
            self.inv_canvas.scale(1, -1)
            self.inv_canvas.translate(-A4[0]/2, -350)

    def draw_table(self):
        table_pos = (25, (A4[1]/2)-50)
        self.inv_canvas.translate(table_pos[0], table_pos[1])

        w_table = A4[0] - 50
        h_table = (A4[1]/2)

        self.inv_canvas.roundRect(0, 0, w_table, h_table, 15, fill=0)

        if self.name_list:
            max_rows = 13
            n_rows = min(max_rows, len(self.name_list))
            h_row = (h_table / n_rows)
            w_column = w_table / 2

            current_row = h_row
            for _ in range(int(n_rows - 1)):
                self.inv_canvas.line(0, current_row, w_table, current_row)
                current_row += h_row

            current_row = h_row
            current_column = 15
            current_name = 0
            max_columns = 2

            for column in range(max_columns):
                for row in range(int(n_rows)):
                    if current_name >= len(self.name_list):
                        break

                    current_name += 1
                    self.inv_canvas.setFont("CalibriRegular", 17)
                    self.inv_canvas.drawCentredString(current_column, current_row - 10, str(current_name))
                    self.inv_canvas.setFont("CalibriBold", 20)
                    self.inv_canvas.drawString(current_column + 20, current_row - 10, str(self.name_list[current_name - 1]))

                    current_row += h_row

                self.inv_canvas.drawCentredString(current_column, current_row - 10, '')
                current_column += w_column
                current_row = h_row

        self.inv_canvas.translate(-table_pos[0], -table_pos[1])

    def generate_pdf(self):
        self.draw_header()
        self.draw_table()
        self.inv_canvas.showPage()
        self.inv_canvas.save()


class Service_Schedule_PDF_Generator:
    def __init__(self, output_path, congregation, data_dict):
        self.congregation = congregation
        self.data_dict = data_dict
        self.inv_canvas = canvas.Canvas(output_path, pagesize=A4, bottomup=0)
        self.config = Config()
        self.current_path = self.config.current_path
        self.init_pdf()

    def init_pdf(self):
        calibri_regular_path = os.path.join(self.current_path, "assets", "font", "Calibri Regular.ttf")
        calibri_bold_path = os.path.join(self.current_path, "assets", "font", "Calibri Bold.TTF")
        cambria_bold_path = os.path.join(self.current_path, "assets", "font", "Cambria-Bold.ttf")
        pdfmetrics.registerFont(TTFont('CalibriRegular', calibri_regular_path))
        pdfmetrics.registerFont(TTFont('CalibriBold', calibri_bold_path))
        pdfmetrics.registerFont(TTFont('CambriaBold', cambria_bold_path))

        self.GRAY = (86/255,86/255,86/255)
        self.BLACK = (0,0,0)
        self.WHITE = (1,1,1)
        self.YELLOW = (190/255,137/255,0)
        self.RED = (136/255,0,36/255)

        self.text_margins = (1*cm, A4[0]-(1*cm), 1*cm, A4[1])
        self.content_pos = (self.text_margins[0], self.text_margins[2]+(1.5*cm))

    def add_minutes_to_time(self, time_str, minutes_to_add):
        time_format = "%H:%M"
        time_obj = datetime.strptime(time_str, time_format)
        new_time_obj = time_obj + timedelta(minutes=minutes_to_add)
        new_time_str = new_time_obj.strftime(time_format)

        return new_time_str

    def draw_header(self):
        image_filename = os.path.join(self.current_path, "assets", "image", "img.jpg")  # Replace with your image file
        self.inv_canvas.drawImage(image_filename, 0, 0, width=A4[0], height=A4[1])

        left_text = self.congregation
        self.inv_canvas.setFont("CalibriBold", 11)

        # Draw congregation name
        self.inv_canvas.drawString(self.text_margins[0], self.text_margins[2]+5, left_text)
        
        # Draw title page
        right_text = 'Planificarea întrunirii din timpul săptămânii' 
        x_right_text = self.text_margins[1] - stringWidth(right_text, 'CambriaBold', 16)
        self.inv_canvas.setFont("CambriaBold", 16)
        self.inv_canvas.drawString(x_right_text, self.text_margins[2]+5, right_text)

        self.inv_canvas.line(self.text_margins[0]-5, self.text_margins[2]+11, self.text_margins[1]+5, self.text_margins[2]+11)

    def draw_content(self, header_date):
        current_row = 0
        row_height = 15
        section_title_height = 35
        center_content_x = self.text_margins[1]/2
        column_two_comment_x = self.text_margins[1] - self.content_pos[0] - 150


        start_hour = '18:00'
        header_dict = self.data_dict[header_date]["header"]
        intro_dict = self.data_dict[header_date]["intro"]
        section_1_dict = self.data_dict[header_date]["section_1"]
        section_2_dict = self.data_dict[header_date]["section_2"]
        section_3_dict = self.data_dict[header_date]["section_3"]


        current_hour = start_hour
        hour_pos_x = 0
        subtitle_pos_x = 40

        # Header Row
        # ===============================================
        self.inv_canvas.setFont("CalibriBold", 11)
        header_verse = list(header_dict.keys())[0]
        header_content = f'{header_date} | {header_verse}'
        self.inv_canvas.drawString(0, current_row, header_content)

        self.inv_canvas.setFont("CalibriBold", 8)
        x_comment = column_two_comment_x - stringWidth(header_dict[header_verse][1], 'CalibriBold', 8)
        self.inv_canvas.setFillColorRGB(*self.GRAY)
        # self.inv_canvas.drawString(x_comment, current_row, list_section0[0][2])

        x_name = column_two_comment_x + 10
        self.inv_canvas.setFillColorRGB(*self.BLACK)
        self.inv_canvas.setFont("CalibriBold", 11)
        self.inv_canvas.drawString(x_name, current_row, header_dict[header_verse][1])
        current_row += row_height

        #  Intro
        # ===============================================
        intro_keys = list(intro_dict.keys())
        for key in intro_keys:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

            self.inv_canvas.setFont("CalibriRegular", 11)
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(intro_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x + 10
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, current_row, intro_dict[key][1])
            next_hour = int(intro_dict[key][0]) if int(intro_dict[key][0]) != 0 else 5
            current_hour = self.add_minutes_to_time(current_hour, next_hour)
            current_row += row_height
        current_row += section_title_height - row_height

        # Section 1
        # ===============================================
        self.inv_canvas.setFillColorRGB(*self.GRAY)
        self.inv_canvas.roundRect(-10, current_row, self.text_margins[1]-5, -25, 3, stroke=0, fill=1)

        img_scale = (16, 16)
        image_path = os.path.join(self.current_path, "assets", "image", "section_1_icon.png")
        self.inv_canvas.translate(2, current_row-4)
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.drawImage(image_path, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1], mask='auto')
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.translate(-2, -(current_row-4))

        self.inv_canvas.setFont("CalibriBold", 14)
        self.inv_canvas.setFillColorRGB(*self.WHITE)
        self.inv_canvas.drawString(15, current_row-7, f'COMORI DIN CUVÂNTUL LUI DUMNEZEU')
        current_row += row_height

        section_1_keys = list(section_1_dict.keys())
        for key in section_1_keys:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

            available_width = column_two_comment_x  # Set this to the appropriate value
            lines = self.split_text_into_lines(key, available_width)
            for line in lines:
                self.inv_canvas.setFont("CalibriRegular", 11)
                self.inv_canvas.setFillColorRGB(*self.BLACK)
                self.inv_canvas.drawString(subtitle_pos_x, current_row, line)
                current_row += row_height
            current_row -= row_height

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(section_1_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x + 10
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, current_row, section_1_dict[key][1])
            current_hour = self.add_minutes_to_time(current_hour, int(section_1_dict[key][0]))
            current_row += row_height
        current_row += section_title_height - row_height


        # Section 2
        # ===============================================
        self.inv_canvas.setFillColorRGB(*self.YELLOW)
        self.inv_canvas.roundRect(-10, current_row, self.text_margins[1]-5, -25, 3, stroke=0, fill=1)

        img_scale = (16, 16)
        image_path = os.path.join(self.current_path, "assets", "image", "section_2_icon.png")
        self.inv_canvas.translate(2, current_row-4)
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.drawImage(image_path, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1], mask='auto')
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.translate(-2, -(current_row-4))

        self.inv_canvas.setFont("CalibriBold", 14)
        self.inv_canvas.setFillColorRGB(*self.WHITE)
        self.inv_canvas.drawString(15, current_row-7, f'SĂ FIM MAI EFICIENȚI ÎN PREDICARE')
        current_row += row_height

        section_2_keys = list(section_2_dict.keys())
        for key in section_2_keys:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.YELLOW)
            self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

            self.inv_canvas.setFont("CalibriRegular", 11)
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(section_2_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x + 10
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, current_row, section_2_dict[key][1])
            current_hour = self.add_minutes_to_time(current_hour, int(section_2_dict[key][0]))
            current_row += row_height
        current_row += section_title_height - row_height

        # Section 3
        # ===============================================
        self.inv_canvas.setFillColorRGB(*self.RED)
        self.inv_canvas.roundRect(-10, current_row, self.text_margins[1]-5, -25, 3, stroke=0, fill=1)

        img_scale = (16, 16)
        image_path = os.path.join(self.current_path, "assets", "image", "section_3_icon.png")
        self.inv_canvas.translate(2, current_row-4)
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.drawImage(image_path, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1], mask='auto')
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.translate(-2, -(current_row-4))
        
        self.inv_canvas.setFont("CalibriBold", 14)
        self.inv_canvas.setFillColorRGB(*self.WHITE)
        self.inv_canvas.drawString(15, current_row-7, f'VIAȚA DE CREȘTIN')
        current_row += row_height

        section_3_keys = list(section_3_dict.keys())
        for key in section_3_keys:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.RED)
            self.inv_canvas.circle(35, current_row-3, 2, stroke=0, fill=1)

            self.inv_canvas.setFont("CalibriRegular", 11)
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(section_3_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x + 10
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, current_row, section_3_dict[key][1])
            next_hour = int(section_3_dict[key][0]) if int(section_3_dict[key][0]) != 0 else 5
            current_hour = self.add_minutes_to_time(current_hour, next_hour)
            current_row += row_height

    def split_text_into_lines(self, text, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and self.inv_canvas.stringWidth(line + words[0], 'CalibriRegular', 11) <= max_width:
                if line:
                    line += ' '
                line += words.pop(0)
            lines.append(line)
        return lines

    def generate_pdf(self):
        
        i = 0
        now_list = ['23-29 octombrie', '30 octombrie – 5 noiembrie']
        # print(list(self.data_dict.keys()))
        # print(list(self.data_dict.keys())[-2:])

        for header_date in list(self.data_dict.keys()):
        # for header_date in now_list:

            if i == 0:
                self.draw_header()
                self.inv_canvas.translate(self.content_pos[0], self.content_pos[1])
                self.draw_content(header_date)
                self.inv_canvas.translate(-self.content_pos[0], -self.content_pos[1])
                i = 1
            else:
                self.inv_canvas.translate(self.content_pos[0], (A4[1]/2)+10)
                self.draw_content(header_date)
                self.inv_canvas.translate(-self.content_pos[0], -(A4[1]/2)+10)
                self.inv_canvas.showPage()
                i = 0

        self.inv_canvas.save()
