import fitz  # PyMuPDF
import json
import re

# Function to extract and clean PDF content
def extract_pdf_content(pdf_path):
    pdf_document = fitz.open(pdf_path)
    pdf_content = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        cleaned_text = clean_content(text)
        pdf_content.append({
            "page_number": page_num + 1,
            "content": cleaned_text
        })

    return pdf_content

# Function to clean the content
def clean_content(content):
    # Remove page numbers and other unnecessary information
    cleaned_content = re.sub(r'Page\s+\d+\s+/\s+\d+', '', content)
    cleaned_content = re.sub(r'______________________________________________________________________________________________', '', cleaned_content)
    return cleaned_content.strip()

# Function to structure the content into a JSON format
def structure_content(pdf_content):
    structured_data = {
        "Identification": "",
        "Hazard_Identification": "",
        "Composition": "",
        "First_Aid_Measures": "",
        "Fire_Fighting_Measures": "",
        "Accidental_Release_Measures": "",
        "Handling_and_Storage": "",
        "Exposure_Controls_Personal_Protection": "",
        "Physical_and_Chemical_Properties": "",
        "Stability_and_Reactivity": "",
        "Toxicological_Information": "",
        "Ecological_Information": "",
        "Disposal_Considerations": "",
        "Transport_Information": "",
        "Regulatory_Information": "",
        "Other_Information": ""
    }

    section_titles = {
        "1. Identification": "Identification",
        "2. Hazard(s) identification": "Hazard_Identification",
        "3. Composition/information on ingredients": "Composition",
        "4. First-aid measures": "First_Aid_Measures",
        "5. Fire-fighting measures": "Fire_Fighting_Measures",
        "6. Accidental release measures": "Accidental_Release_Measures",
        "7. Handling and storage": "Handling_and_Storage",
        "8. Exposure controls/personal protection": "Exposure_Controls_Personal_Protection",
        "9. Physical and chemical properties": "Physical_and_Chemical_Properties",
        "10. Stability and reactivity": "Stability_and_Reactivity",
        "11. Toxicological information": "Toxicological_Information",
        "12. Ecological information": "Ecological_Information",
        "13. Disposal considerations": "Disposal_Considerations",
        "14. Transport information": "Transport_Information",
        "15. Regulatory information": "Regulatory_Information",
        "16. Other information": "Other_Information"
    }

    current_section = None
    for page in pdf_content:
        lines = page["content"].split('\n')
        for line in lines:
            line = line.strip()
            if line in section_titles:
                current_section = section_titles[line]
            elif current_section:
                structured_data[current_section] += line + ' '

    return structured_data

# Function to convert the structured data to JSON
def convert_to_json(data):
    return json.dumps(data, indent=4)

# Function to save the JSON data to a file
def save_json_to_file(json_data, output_path):
    with open(output_path, 'w') as json_file:
        json_file.write(json_data)

# Main function to execute the steps
def main(pdf_path, output_json_path):
    pdf_content = extract_pdf_content(pdf_path)
    structured_data = structure_content(pdf_content)
    json_data = convert_to_json(structured_data)
    save_json_to_file(json_data, output_json_path)

# Example usage
pdf_path = 'data/acetone-acs-l (1).pdf'
output_json_path = 'structured_output.json'
main(pdf_path, output_json_path)