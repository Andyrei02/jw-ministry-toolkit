import os

from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

class MeetingSchedule:
    def __init__(self, start_time):
        self.start_time = datetime.strptime(start_time, "%H:%M")

    def calculate_times(self, data):
        for header_date, sections in data.items():
            current_time = self.start_time
            for section, items in sections.items():
                for item, item_data in items.items():
                    try:
                        next_time = int(item_data[0])
                    except:
                        print(item_data[0])
                    item_data[0] = current_time.strftime("%H:%M")
                    current_time = current_time + timedelta(minutes=next_time)
        return data

class Service_Workbook_PDF_Generator:
    def __init__(self, template_dir='templates'):
        self.schedule = MeetingSchedule("18:00")
        
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = "template.html"
        self.css_path = os.path.join(template_dir, 'styles.css')
        
    def generate_pdf(self, data, output_html="output.html", output_pdf="output.pdf"):
        template = self.env.get_template(self.template)
        processed_data = self.schedule.calculate_times(data)
        
        html_content = template.render(schedule=processed_data, css_path=self.css_path)
        
        # Save HTML file
        with open(output_html, "w") as file:
            file.write(html_content)
            
        # Generate PDF
        HTML(string=html_content, base_url=".").write_pdf(output_pdf)
