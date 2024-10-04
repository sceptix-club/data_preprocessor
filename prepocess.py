import fitz 
import json
import re

def extract_text_with_structure(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_data = []
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")['blocks'] 
        
        for block in blocks:
            if 'lines' in block:
                for line in block['lines']:
              
                    text_line = ''.join([span['text'] for span in line['spans']])
                    font_size = line['spans'][0]['size']
                    bold = line['spans'][0]['flags'] & 2  
                
                    extracted_data.append({
                        "text": text_line.strip(),
                        "font_size": font_size,
                        "bold": bool(bold),
                        "page": page_num + 1
                    })
    
    return extracted_data

def process_extracted_text_with_subheadings(extracted_data):
    json_output = {}
    current_section = None
    current_subheading = None

    for item in extracted_data:
        text = item['text']
   
        if re.match(r'^\d+\.\s+[A-Za-z\s]+$', text):
            current_section = text
            json_output[current_section] = {}
            current_subheading = None 

        elif current_section:
            if item['bold']: 
                current_subheading = text
                json_output[current_section][current_subheading] = []
            else:
    
                if current_subheading:
                    json_output[current_section][current_subheading].append(text)
                else:
                    if "content" not in json_output[current_section]:
                        json_output[current_section]["content"] = []
                    json_output[current_section]["content"].append(text)

    return json_output

def save_json_to_file(json_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(json_data, f, indent=4)

def process_pdf_to_json_with_subheadings(pdf_path, output_file):
  
    extracted_data = extract_text_with_structure(pdf_path)
 
    json_data = process_extracted_text_with_subheadings(extracted_data)

    save_json_to_file(json_data, output_file)
    
    print(f"PDF data successfully converted to JSON with subheadings and saved to {output_file}")


pdf_path = "acetonitrile-hplc-grade-l (1).pdf"  
output_file = "acetonitrile_sds_with_subheadings.json"

process_pdf_to_json_with_subheadings(pdf_path, output_file)
