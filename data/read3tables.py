import pdfplumber
import json

file_path = r"C:\Users\HP\OneDrive\Desktop\data_preprocessor\data\acetone-acs-l (1).pdf"



with pdfplumber.open(file_path) as pdf:
    
    for page_num, page in enumerate(pdf.pages):
        tables = page.extract_tables()  # Use extract_tables() instead of extract_table()
        print(f"Tables from page {page_num + 1}:")
        for table in tables:
            for row in table:
                print(row)