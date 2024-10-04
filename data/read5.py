import pdfplumber
import json

def process_paragraph(paragraph): 
    return {"type": "paragraph", "content": paragraph.strip()}

def process_heading(heading):
    return {"type": "heading", "content": heading.strip()}

def process_table(table):
    return {"type": "table", "content": table}

def detect_structure(text):
    paragraphs = text.split('\n\n')
    structured_content = []
    
    for paragraph in paragraphs:
        clean_paragraph = paragraph.strip()
        if clean_paragraph:
            if len(clean_paragraph.split()) < 5:  
                structured_content.append(process_heading(clean_paragraph))
            else:
                structured_content.append(process_paragraph(clean_paragraph))
    
    return structured_content

def extract_tables(page):
    tables = page.extract_tables()
    table_list = []
    for table in tables:
        table_list.append(process_table(table))
    return table_list

def main():
    #filepath = input(r"Enter the file path: ")
    filepath = r"C:\Users\HP\OneDrive\Desktop\data_preprocessor\data\acetone-acs-l (1).pdf"

    document_structure = []

    with pdfplumber.open(filepath) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"Processing page {page_num + 1}:")
            
            text = page.extract_text()
            if text:
                structured_text = detect_structure(text)
                document_structure.extend(structured_text)

            tables = extract_tables(page)
            document_structure.extend(tables)
    
    # Convert the structure to JSON
    json_output = json.dumps(document_structure, indent=4)
    
    # Save to file or print
    with open('output.json', 'w') as json_file:
        json_file.write(json_output)
    
    print("PDF content has been converted to JSON.")

if __name__ == "__main__":
    main()
