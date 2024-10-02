import pdfplumber
with pdfplumber.open(r'data_preprocessor\data\acetone-acs-l.pdf') as pdf:
    data =pdf.pages[0].extract_text()
    print(data)