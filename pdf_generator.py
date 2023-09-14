from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class Testimony_Cart_PDF_Generator:
    def __init__(self, output_path, title=None, image=None, name_list=None):
        self.title = title
        self.image = image
        self.name_list = name_list
        self.inv_canvas = canvas.Canvas(output_path, pagesize=A4, bottomup=0)
        self.init_pdf()

    def init_pdf(self):
        pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuBold', 'DejaVuSans-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuOblique', 'DejaVuSans-Oblique.ttf'))

    def draw_header(self):
        self.inv_canvas.setFont("DejaVuBold", 35)
        self.inv_canvas.drawCentredString(A4[0]/2, 40, self.title)

        if self.image:
            img_scale = (350, 300)
            self.inv_canvas.translate(A4[0]/2, 350)
            self.inv_canvas.scale(1, -1)
            self.inv_canvas.drawImage(self.image, -img_scale[0]/2, 0, width=img_scale[0], height=img_scale[1])
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
                    self.inv_canvas.setFont("DejaVuOblique", 17)
                    self.inv_canvas.drawCentredString(current_column, current_row - 10, str(current_name))
                    self.inv_canvas.setFont("DejaVuBold", 20)
                    self.inv_canvas.drawString(current_column + 20, current_row - 10, str(self.name_list[current_name - 1]))

                    current_row += h_row

                current_column += w_column
                current_row = h_row

        self.inv_canvas.translate(-table_pos[0], -table_pos[1])

    def generate_pdf(self):
        self.draw_header()
        self.draw_table()
        self.inv_canvas.showPage()
        self.inv_canvas.save()
