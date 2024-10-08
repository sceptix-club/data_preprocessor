import PyPDF2
import json

# Open and read the PDF file
pdf_file_path = 'data/acetone-acs-l.pdf'
with open(pdf_file_path, 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(reader.pages)

    # Initialize the structure
    structured_data = {}
    
    current_section = None
    current_subsection = None

    # Loop through each page of the PDF
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text = page.extract_text()

        # Process each line of text
        for line in text.split('\n'):
            # Detect main sections
            if line.strip().isdigit() and int(line.strip()) in range(1, 20):  # Assuming sections are numbered
                current_section = line.strip()
                structured_data[current_section] = {}
            elif line.strip().startswith('•'):  # Detect subsections by bullet points or specific patterns
                current_subsection = line.strip()
                if current_section:
                    structured_data[current_section][current_subsection] = []
            elif current_section and current_subsection:
                structured_data[current_section][current_subsection].append(line.strip())
            elif current_section:
                structured_data[current_section].setdefault('content', []).append(line.strip())

# Convert to JSON format
json_data = json.dumps(structured_data, indent=4)

# Save the JSON data to a file
output_json_path = 'structured_data.json'
with open(output_json_path, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON data has been saved to {output_json_path}")
