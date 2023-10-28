path = '/home/andreic/Documents/Congregatie/Lista_cu_standul/Lista_cu_caruciorul.pdf'

import PyPDF2




def get_list_items(path):
	with open(path, 'rb') as pdf_file:
		pdf_reader = PyPDF2.PdfReader(pdf_file)
		page = pdf_reader.pages[0]
		text = page.extract_text()

		return text.split('\n')


list_items = get_list_items(path)

title = list_items[0]

filtered_list = [item for item in list_items if not (any(char.isdigit() for char in item) or item == "")]

print(title)

print(filtered_list)


