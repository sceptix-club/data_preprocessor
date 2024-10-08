import pdfplumber
import json



def process_main_heading(heading):
    return{heading.strip()}

def process_sub_heading(subheading):
    return{subheading.strip()}

def process_paragraph(h,paragraph):
    return{h : paragraph.strip()}

def process_table(table):
    return {"type": "table", "content": table}


def detect_structure(text):
    paragraphs = text.split('\n\n')
    structured_content = []
    
    for paragraph in paragraphs:
        clean_paragraph = paragraph.strip()
        if clean_paragraph:
            for element in clean_paragraph.extract_words():  # Each element contains text, font-size, bold, etc.
                text = element["text"]
                font_size = element["size"]   # Access font size
                is_bold = "Bold" in element["fontname"]
            if len(clean_paragraph.split()) < 5 and is_bold: 
                headd=clean_paragraph 
                structured_content.append(process_main_heading(clean_paragraph))
            elif len(clean_paragraph.split())<5:
                subhead=clean_paragraph
                structured_content.append(process_sub_heading(clean_paragraph))

            else:
                structured_content.append(process_paragraph(headd,clean_paragraph))
    
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
