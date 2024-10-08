#file location: data_preprocessor/data/acetone-acs-l (1).pdf

import PyPDF2
import os

# Data extraction function
def pdf_to_text(pdf_path):
    # Extract the base name of the PDF file (without extension)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]   
    # Create the output text file name by appending ".txt"
    output_txt = f"{base_name}.txt"
    
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Initialize an empty string to store the text
        text = ''
        
        # Iterate through all pages and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:  # Ensure text was extracted
                text += page_text + "\n"  # Add a newline for page separation
                
    # Write the extracted text to a text file (output_txt)
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
        
    print(f"PDF converted to text successfully! Text saved as: {output_txt}")

# Usage example
pdf_to_text('data/acetone-acs-l (1).pdf')

#pdf_to_text('data_preprocessor/data/acetone-acs-l (1).pdf') 

#cleaning up
def exclude_lines_with_keyword(input_file_path):
    # Create the output file name by appending '_modified' to the original file name
    base_name = os.path.basename(input_file_path)
    file_name, file_extension = os.path.splitext(base_name)
    output_file_path = os.path.join(os.path.dirname(input_file_path), f"{file_name}_modified{file_extension}")

    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
        for line in input_file:
            # Check if the specific keyword is NOT in the line
            if "Page" not in line and "____" not in line:
                output_file.write(line)  # Write the line to the output file

    print(f"Lines excluding the keywords have been written to '{output_file_path}'.")

exclude_lines_with_keyword("acetone-acs-l (1).txt")