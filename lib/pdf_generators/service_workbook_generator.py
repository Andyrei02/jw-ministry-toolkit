import os
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth

from . import Config


class Service_Workbook_PDF_Generator:
    def __init__(self, output_path, congregation, data_dict):
        self.congregation = congregation
        self.data_dict = data_dict
        self.inv_canvas = canvas.Canvas(output_path, pagesize=A4, bottomup=0)
        self.config = Config()
        self.init_pdf()

    def init_pdf(self):
        pdfmetrics.registerFont(TTFont('CalibriRegular', self.config.calibri_regular_path))
        pdfmetrics.registerFont(TTFont('CalibriBold', self.config.calibri_bold_path))
        pdfmetrics.registerFont(TTFont('CambriaBold', self.config.cambria_bold_path))

        self.GRAY = (86/255,86/255,86/255) 
        self.GREEN = (48/255, 102/255, 111/255)
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
        self.inv_canvas.drawImage(self.config.bg_workbook_ico_path, 0, 0, width=A4[0], height=A4[1], mask='auto')

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
        dot_size = 3.5
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
        subtitle_pos_x = 42

        # Header Row
        # ===============================================
        self.inv_canvas.setFont("CalibriBold", 13)
        header_verse = list(header_dict.keys())[0]
        header_content = f'{header_date} | {header_verse}'
        self.inv_canvas.drawString(0, current_row, header_content)

        self.inv_canvas.setFont("CalibriBold", 8)
        x_comment = column_two_comment_x - stringWidth(header_dict[header_verse][1], 'CalibriBold', 8)
        self.inv_canvas.setFillColorRGB(*self.GRAY)
        # self.inv_canvas.drawString(x_comment, current_row, list_section0[0][2])

        x_name = column_two_comment_x - 15
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
            self.inv_canvas.circle(35, current_row-3, dot_size, stroke=0, fill=1)

            self.inv_canvas.setFont("CalibriRegular", 13)
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(intro_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x - 15
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, current_row, intro_dict[key][1])
            next_hour = int(intro_dict[key][0]) if int(intro_dict[key][0]) != 0 else 5
            current_hour = self.add_minutes_to_time(current_hour, next_hour)
            current_row += row_height
        current_row += section_title_height - row_height

        # Section 1
        # ===============================================
        self.inv_canvas.setFillColorRGB(*self.GREEN)
        self.inv_canvas.roundRect(-7, current_row, 25, -25, 5, stroke=0, fill=1)

        img_scale = (20, 20)
        self.inv_canvas.translate(6, current_row-2)
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.drawImage(self.config.section_1_ico_path, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1], mask='auto')
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.translate(-6, -(current_row-2))

        self.inv_canvas.setFont("CalibriBold", 25)
        self.inv_canvas.setFillColorRGB(*self.GREEN)
        self.inv_canvas.drawString(23, current_row-3, f'COMORI DIN CUVÂNTUL LUI DUMNEZEU')
        current_row += row_height

        section_1_keys = list(section_1_dict.keys())
        for key in section_1_keys:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.GREEN)
            self.inv_canvas.circle(35, current_row-3, dot_size, stroke=0, fill=1)

            available_width = column_two_comment_x - 120
            lines = self.split_text_into_lines(key, available_width)
            name_row = current_row
            for line in lines:
                self.inv_canvas.setFont("CalibriRegular", 13)
                self.inv_canvas.setFillColorRGB(*self.BLACK)
                self.inv_canvas.drawString(subtitle_pos_x, current_row, line)
                current_row += row_height
            current_row -= row_height

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(section_1_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x - 15
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, name_row, section_1_dict[key][1])
            current_hour = self.add_minutes_to_time(current_hour, int(section_1_dict[key][0]))
            current_row += row_height
        current_row += section_title_height - row_height


        # Section 2
        # ===============================================
        self.inv_canvas.setFillColorRGB(*self.YELLOW)
        self.inv_canvas.roundRect(-7, current_row, 25, -25, 5, stroke=0, fill=1)

        img_scale = (20, 20)
        self.inv_canvas.translate(6, current_row-2)
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.drawImage(self.config.section_2_ico_path, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1], mask='auto')
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.translate(-6, -(current_row-2))

        self.inv_canvas.setFont("CalibriBold", 25)
        self.inv_canvas.setFillColorRGB(*self.YELLOW)
        self.inv_canvas.drawString(23, current_row-3, f'SĂ FIM MAI EFICIENȚI ÎN PREDICARE')
        current_row += row_height

        section_2_keys = list(section_2_dict.keys())
        for key in section_2_keys:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.YELLOW)
            self.inv_canvas.circle(35, current_row-3, dot_size, stroke=0, fill=1)

            available_width = column_two_comment_x - 150
            lines = self.split_text_into_lines(key, available_width)
            name_row = current_row
            for line in lines:
                self.inv_canvas.setFont("CalibriRegular", 13)
                self.inv_canvas.setFillColorRGB(*self.BLACK)
                self.inv_canvas.drawString(subtitle_pos_x, current_row, line)
                current_row += row_height
            current_row -= row_height

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(section_2_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x - 15
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            list_names = section_2_dict[key][1].split('/')
            self.inv_canvas.drawString(x_name, name_row, section_2_dict[key][1])
            current_hour = self.add_minutes_to_time(current_hour, int(section_2_dict[key][0]))
            current_row += row_height
        current_row += section_title_height - row_height

        # Section 3
        # ===============================================
        self.inv_canvas.setFillColorRGB(*self.RED)
        self.inv_canvas.roundRect(-7, current_row, 25, -25, 5, stroke=0, fill=1)

        img_scale = (20, 20)
        self.inv_canvas.translate(6, current_row-2)
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.drawImage(self.config.section_3_ico_path, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1], mask='auto')
        self.inv_canvas.scale(1, -1)
        self.inv_canvas.translate(-6, -(current_row-2))
        
        self.inv_canvas.setFont("CalibriBold", 25)
        self.inv_canvas.setFillColorRGB(*self.RED)
        self.inv_canvas.drawString(23, current_row-3, f'VIAȚA DE CREȘTIN')
        current_row += row_height

        section_3_keys = list(section_3_dict.keys())
        for key in section_3_keys[:-2]:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.RED)
            self.inv_canvas.circle(35, current_row-3, dot_size, stroke=0, fill=1)

            available_width = column_two_comment_x - 150
            lines = self.split_text_into_lines(key, available_width)
            name_row = current_row
            for line in lines:
                self.inv_canvas.setFont("CalibriRegular", 13)
                self.inv_canvas.setFillColorRGB(*self.BLACK)
                self.inv_canvas.drawString(subtitle_pos_x, current_row, line)
                current_row += row_height
            current_row -= row_height

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(section_3_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x - 15
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, name_row, section_3_dict[key][1])
            next_hour = int(section_3_dict[key][0]) if int(section_3_dict[key][0]) != 0 else 5
            current_hour = self.add_minutes_to_time(current_hour, next_hour)
            current_row += row_height

        current_row += row_height/2
        
        for key in section_3_keys[-2:]:
            self.inv_canvas.setFont("CalibriBold", 9)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(0, current_row, current_hour)

            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.circle(35, current_row-3, dot_size, stroke=0, fill=1)

            self.inv_canvas.setFont("CalibriRegular", 13)
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.drawString(subtitle_pos_x, current_row, key)

            self.inv_canvas.setFont("CalibriBold", 8)
            x_comment = column_two_comment_x - stringWidth(section_3_dict[key][1], 'CalibriBold', 8)
            self.inv_canvas.setFillColorRGB(*self.GRAY)
            self.inv_canvas.drawString(x_comment, current_row, '')

            x_name = column_two_comment_x - 15
            name_row = current_row
            self.inv_canvas.setFillColorRGB(*self.BLACK)
            self.inv_canvas.setFont("CalibriBold", 11)
            self.inv_canvas.drawString(x_name, name_row, section_3_dict[key][1])
            next_hour = int(section_3_dict[key][0]) if int(section_3_dict[key][0]) != 0 else 5
            current_hour = self.add_minutes_to_time(current_hour, next_hour)
            current_row += row_height

        return current_row + row_height*2

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
        next_row = None

        for header_date in list(self.data_dict.keys()):
            if i == 0:
                self.draw_header()
                self.inv_canvas.translate(self.content_pos[0], self.content_pos[1])
                next_row = self.draw_content(header_date)
                self.inv_canvas.translate(-self.content_pos[0], -self.content_pos[1])
                i = 1
            else:
                self.inv_canvas.translate(self.content_pos[0], self.content_pos[1]+next_row)
                self.draw_content(header_date)
                self.inv_canvas.translate(-self.content_pos[0], -(A4[1]/2)+10)
                self.inv_canvas.showPage()
                i = 0

        self.inv_canvas.save()
