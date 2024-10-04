import pdfplumber
import re
import json

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

def parse_content_with_regex(text):
    section_regex = re.compile(r"^\d+\.\s[A-Za-z()]+.*$")
    key_value_regex = re.compile(r"^(.*?):\s*(.*)$")
    
    structured_data = {}
    current_section = None
    current_subsection = None
    section_data = {}

    for line in text.splitlines():
        line = line.strip()
        
        if section_regex.match(line):
            if current_section:
                structured_data[current_section] = section_data
            current_section = line
            section_data = {}
        
        elif key_value_regex.match(line):
            key, value = key_value_regex.findall(line)[0]
            section_data[key.strip()] = value.strip()
        
        elif current_subsection:
            section_data[current_subsection] += " " + line.strip()

        else:
            if current_section:
                if line:
                    section_data[len(section_data)] = line.strip()

    if current_section:
        structured_data[current_section] = section_data

    return structured_data

def create_json_output(parsed_data):
    return json.dumps(parsed_data, indent=4)

pdf_path = r'data\chloroform-certified-acs-l.pdf'

pdf_text = extract_text_from_pdf(pdf_path)

parsed_content = parse_content_with_regex(pdf_text)

json_output = create_json_output(parsed_content)

print(json_output)

with open('output.json', 'w') as json_file:
    json_file.write(json_output)
