

from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

data = {'6-12 ianuarie': {'header': {'PSALMII 127-134': [0, 'Bodiu Ruslan']}, 'intro': {'Cântarea 134 și rugăciune': ['5', 'Russu Petru'], 'Cuvinte introductive ': ['1', 'Russu Petru']}, 'section_1': {'1. Părinți, continuați să vă îngrijiți de prețioasa voastră moștenire!': ['10', 'Homeacov Eugen'], '2. Nestemate spirituale': ['10', 'Bodiu Ruslan'], '3. Citirea Bibliei': ['4', 'Tulei Andrian']}, 'section_2': {'4. Începe o conversație': ['3', 'Cenusa Ana / Popovici Ana'], '5. Începe o conversație': ['4', 'Homeacov Mihaela / Popa Natalia'], '6. Fă discipoli': ['5', 'Russu Oxana / Tabaran Elena']}, 'section_3': {'Cântarea 13': ['5', ''], '7. Părinți, folosiți acest instrument eficient de predare?': ['15', 'Homeacov Eugen'], '8. Studiul Bibliei în congregație': ['30', 'Moldoveanu Vasile / Pasare Vasile'], 'Cuvinte de încheiere': ['5', 'Russu Petru'], 'Cântarea\xa073': ['5', 'Russu Petru']}}, '13-19 ianuarie': {'header': {'PSALMII 135-137': [0, '']}, 'intro': {'Cântarea 2 și rugăciune': ['5', ''], 'Cuvinte introductive ': ['1', '']}, 'section_1': {'1. „Domnul nostru este mai mare decât toți ceilalți dumnezei”': ['10', ''], '2. Nestemate spirituale': ['10', ''], '3. Citirea Bibliei': ['4', '']}, 'section_2': {'4. Începe o conversație': ['3', ''], '5. Fă vizite ulterioare': ['4', ''], '6. Explică-ți convingerile': ['5', '']}, 'section_3': {'Cântarea 10': ['5', ''], '7. Necesități locale': ['15', ''], '8. Studiul Bibliei în congregație': ['30', ''], 'Cuvinte de încheiere': ['5', ''], 'Cântarea\xa090': ['5', '']}}, '20-26 ianuarie': {'header': {'PSALMII 138, 139': [0, '']}, 'intro': {'Cântarea 93 și rugăciune': ['5', ''], 'Cuvinte introductive ': ['1', '']}, 'section_1': {'1. Nu permiteți ca emoțiile să fie un obstacol în serviciul vostru': ['10', ''], '2. Nestemate spirituale': ['10', ''], '3. Citirea Bibliei': ['4', '']}, 'section_2': {'4. Începe o conversație': ['3', ''], '5. Fă discipoli': ['4', ''], '6. Cuvântare': ['5', '']}, 'section_3': {'Cântarea 59': ['5', ''], '7. Poți avea succes în serviciul tău în pofida timidității': ['15', ''], '8. Studiul Bibliei în congregație': ['30', ''], 'Cuvinte de încheiere': ['5', ''], 'Cântarea\xa0151': ['5', '']}}, '27 ianuarie – 2 februarie': {'header': {'PSALMII 140-143': [0, '']}, 'intro': {'Cântarea 44 și rugăciune': ['5', ''], 'Cuvinte introductive ': ['1', '']}, 'section_1': {'1. Acționează în armonie cu implorările tale pentru ajutor': ['10', ''], '2. Nestemate spirituale': ['10', ''], '3. Citirea Bibliei': ['4', '']}, 'section_2': {'4. Începe o conversație': ['4', ''], '5. Fă vizite ulterioare': ['3', ''], '6. Explică-ți convingerile': ['5', '']}, 'section_3': {'Cântarea 141': ['5', ''], '7. Fii pregătit pentru situații care pretind îngrijire medicală sau o intervenție chirurgicală': ['15', ''], '8. Studiul Bibliei în congregație': ['30', ''], 'Cuvinte de încheiere': ['5', ''], 'Cântarea\xa0103': ['5', '']}}, '3-9 februarie': {'header': {'PSALMII 144-146': [0, '']}, 'intro': {'Cântarea 145 și rugăciune': ['5', ''], 'Cuvinte introductive ': ['1', '']}, 'section_1': {'1. „Fericit este poporul al cărui Dumnezeu este Iehova!”': ['10', ''], '2. Nestemate spirituale': ['10', ''], '3. Citirea Bibliei': ['4', '']}, 'section_2': {'4. Începe o conversație': ['4', ''], '5. Fă vizite ulterioare': ['4', ''], '6. Cuvântare': ['4', '']}, 'section_3': {'Cântarea 59': ['5', ''], '7. Iehova vrea să fii fericit': ['10', ''], '8. Necesități locale': ['5', ''], '9. Studiul Bibliei în congregație': ['30', ''], 'Cuvinte de încheiere': ['5', ''], 'Cântarea\xa085': ['5', '']}}, '10-16 februarie': {'header': {'PSALMII 147-150': [0, '']}, 'intro': {'Cântarea 12 și rugăciune': ['5', ''], 'Cuvinte introductive ': ['1', '']}, 'section_1': {'1. Avem multe motive să-l lăudăm pe Iah': ['10', ''], '2. Nestemate spirituale': ['10', ''], '3. Citirea Bibliei': ['4', '']}, 'section_2': {'4. Începe o conversație': ['3', ''], '5. Începe o conversație': ['4', ''], '6. Cuvântare': ['5', '']}, 'section_3': {'Cântarea 159': ['5', ''], '7. Raportul anual de serviciu': ['15', ''], '8. Studiul Bibliei în congregație': ['30', ''], 'Cuvinte de încheiere': ['5', ''], 'Cântarea\xa037': ['5', '']}}, '17-23 februarie': {'header': {'PROVERBELE 1': [0, '']}, 'intro': {'Cântarea 88 și rugăciune': ['5', ''], 'Cuvinte introductive ': ['1', '']}, 'section_1': {'1. Tineri, de cine veți asculta?': ['10', ''], '2. Nestemate spirituale': ['10', ''], '3. Citirea Bibliei': ['4', '']}, 'section_2': {'4. Începe o conversație': ['2', ''], '5. Începe o conversație': ['2', ''], '6. Fă vizite ulterioare': ['2', ''], '7. Fă discipoli': ['5', '']}, 'section_3': {'Cântarea 89': ['5', ''], '8. Necesități locale': ['15', ''], '9. Studiul Bibliei în congregație': ['30', ''], 'Cuvinte de încheiere': ['5', ''], 'Cântarea\xa080': ['5', '']}}, '24 februarie – 2 martie': {'header': {'PROVERBELE 2': [0, '']}, 'intro': {'Cântarea 35 și rugăciune': ['5', ''], 'Cuvinte introductive ': ['1', '']}, 'section_1': {'1. De ce e bine să pui suflet în studiul tău personal?': ['10', ''], '2. Nestemate spirituale': ['10', ''], '3. Citirea Bibliei': ['4', '']}, 'section_2': {'4. Începe o conversație': ['4', ''], '5. Fă vizite ulterioare': ['3', ''], '6. Cuvântare': ['5', '']}, 'section_3': {'Cântarea 96': ['5', ''], '7. Ești un căutător de comori?': ['15', ''], '8. Studiul Bibliei în congregație': ['30', ''], 'Cuvinte de încheiere': ['5', ''], 'Cântarea\xa0102': ['5', '']}}}

start_time = '18:00'
start_time_obj = datetime.strptime(start_time, "%H:%M")

for header_date, sections in data.items():
    current_time = start_time_obj
    for section, items in sections.items():
        for item, item_data in items.items():
            next_time = int(item_data[0])
            item_data[0] = current_time.strftime("%H:%M")
            current_time = current_time + timedelta(minutes=next_time)


# Load the template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')

# Render the template with data
html_content = template.render(schedule=data)

# Save the rendered HTML to a file (optional)
with open("output.html", "w") as file:
    file.write(html_content)

# Convert the rendered HTML to PDF
HTML(string=html_content, base_url=".").write_pdf("output.pdf")

print("PDF generated successfully.")
