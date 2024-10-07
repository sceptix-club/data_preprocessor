import pdfplumber
import json
import re

def process_main_heading(heading):
    main_head=heading.strip()
    return{heading.strip()}

#def process_sub_heading1(heading):
 #   sub_head=heading.strip()
 #   return{heading.strip()}

#def process_paragraph(h,paragraph):
 #   return{h : paragraph.strip()}

def process_paragraph(paragraph): 
    return {"type": "paragraph", "content": paragraph.strip()}

def process_heading(heading):
    return {"type": "heading", "content": heading.strip()}

def process_table(table):
    return {"type": "table", "content": table}

def detect_structure(text):
    paragraphs=text.split('\n\n')                      #to split the paras ig
    structured_content=[]                              #to store the structred content ...empty list is initialised

    sentences_per_paragraph = [paragraph.split('.') for paragraph in paragraphs]
    cleaned_sentences_per_paragraph = [[sentence.strip() for sentence in sentences if sentence.strip()] for sentences in sentences_per_paragraph]
    
    for i, sentences in enumerate(cleaned_sentences_per_paragraph):
        #print(f"Paragraph {i + 1}:")
        for sentence in sentences:
            match = re.search("ThermoFisher",sentence) or re.search("SCIENTIFIC",sentence) or re.search("SAFETY DATA SHEET",sentence) or re.search("Creation Date\s+\d+-[a-zA-Z]{3}-\d+\s+Revision Date\s+\d+-[a-zA-Z]{3}-\d+\s+Revision Number\s+\d",sentence)
            print(f"  {sentence}.") 

''' for paragraph in paragraphs:
        clean_paragraph = paragraph.strip()            #to remove leading or trailing whitespaces

        if clean_paragraph:
            
            if len(clean_paragraph.split()) < 5:       # include logic for headers of different font sizes
                headd=clean_paragraph
                structured_content.append(process_main_heading(clean_paragraph))
                
            else:
                structured_content.append(process_paragraph(headd,clean_paragraph))

    return structured_content'''


def extract_tables(page):
    tables = page.extract_tables()
    table_list = []
    for table in tables:
        table_list.append(process_table(table))
    return table_list


def main():
    #file_path=input(r"Enter the file path: ")
    file_path = r"C:\Users\HP\OneDrive\Desktop\data_preprocessor\data\acetone-acs-l (1).pdf"

    document_structure=[] #empty list to storee doc structure??

    with pdfplumber.open(file_path) as pdf:

        for page_num,page in enumerate(pdf.pages):
            print(f"Processing page {page_num + 1}:")

            text=page.extract_text()



    json_output = json.dumps(document_structure, indent=4)
    with open('output.json', 'w') as json_file:
        json_file.write(json_output)
    print("PDF content has been converted to JSON.")

if __name__ == "__main__":
    main()