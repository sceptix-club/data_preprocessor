import pdfplumber
import json



def process_main_heading(heading):
    main_head=heading.strip()
    return{heading.strip()}

#def process_sub_heading1(heading):
 #   sub_head=heading.strip()
 #   return{heading.strip()}

def process_paragraph(h,paragraph):
    return{h : paragraph.strip()}



#def process_paragraph(paragraph): 
   # return {"type": "paragraph", "content": paragraph.strip()}

#def process_heading(heading):
    #return {"type": "heading", "content": heading.strip()}

def process_table(table):
    return {"type": "table", "content": table}



def detect_structure(text):
    paragraphs=text.split('\n\n')                      #to split the paras ig
    structured_content=[]                              #to store the structred content ...empty list is initialised

    for paragraph in paragraphs:
        clean_paragraph = paragraph.strip()            #to remove leading or trailing whitespaces

        if clean_paragraph:

            if len(clean_paragraph.split()) < 5:       # include logic for headers of different font sizes
                headd=clean_paragraph
                structured_content.append(process_main_heading(clean_paragraph))
                
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
    #file_path=input(r"Enter the file path: ")
    file_path = r"C:\Users\HP\OneDrive\Desktop\data_preprocessor\data\acetone-acs-l (1).pdf"

    document_structure=[] #empty list to storee doc structure??

    with pdfplumber.open(file_path) as pdf:

        for page_num,page in enumerate(pdf.pages):
            print(f"Processing page {page_num + 1}:")

            text=page.extract_text()

# Convert the structure to JSON
    json_output = json.dumps(document_structure, indent=4)
    
    # Save to file or print
    with open('output.json', 'w') as json_file:
        json_file.write(json_output)
    
    print("PDF content has been converted to JSON.")

if __name__ == "__main__":
    main()