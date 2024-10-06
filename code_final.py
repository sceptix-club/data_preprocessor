# import libraries
import os
import re
import json
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from langchain.llms import Ollama

# Extraction using PyPDF2 (even pdfplumber could be used for the purpose)
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# use of tesseract, if the pdf contains scanned images

# note that, here it works without this, because the data contains no images
def ocr_from_images(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = ""
    for img in images:
        text = pytesseract.image_to_string(img)
        extracted_text += text + "\n"
    return extracted_text.strip()

# creating chunks
def split_text_into_chunks(text, chunk_size=1000):
    """Split text into smaller chunks if it's too long for the model to handle."""
    lines = text.split('\n')
    chunks = []
    current_chunk = ""
    for line in lines:
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = line + "\n"
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# load mistral model
def load_llama_model():
    llm = Ollama(model="mistral")
    return llm

# prompting llm to generate structured json
def intelligent_structure_with_llm(text, llm):
    chunks = split_text_into_chunks(text)
    structured_data = {}

    for chunk in chunks:
        prompt = f"""
        Here is some text extracted from a PDF. Analyze it and generate structured JSON where main sections are parent keys and subsections are children.

        Text:
        {chunk}

        Now provide the structured JSON:
        """
        response = llm(prompt)
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            structured_json = response[json_start:json_end]
            chunk_data = json.loads(structured_json)
            structured_data.update(chunk_data)  # merge the structured data
        except json.JSONDecodeError:
            print(f"Error decoding JSON from chunk:\n{response}")

    return structured_data

def process_pdf_to_json_with_llama(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)

    # OCR working condition
    if not extracted_text.strip():
        print("No text found using PyPDF2. Falling back to Tesseract OCR.")
        extracted_text = ocr_from_images(pdf_path)

    if not extracted_text:
        print("No text could be recognized.")
        return


    llm = load_llama_model()

    structured_json = intelligent_structure_with_llm(extracted_text, llm)

    if not structured_json:
        print("No valid JSON could be generated.")
        return

    output_json_path = pdf_path.replace('.pdf', '.json')
    with open(output_json_path, 'w') as json_file:
        json.dump(structured_json, json_file, indent=4)

    print(f"Structured JSON saved to: {output_json_path}")

if __name__ == "__main__":
    pdf_file_path = '/content/ammonium-hydroxide-acs-lb.pdf'  # Replace with your PDF file path
    process_pdf_to_json_with_llama(pdf_file_path)

# If bulk folders are needed to be processed, do the following

# - uncomment this code
# - replace the following in the main execution part from ```pdf_file_path``` with ```folder_path```

#  def process_folder_of_pdfs(folder_path):
#     for f in os.listdir(folder_path):
#         if f.endswith('.pdf'):
#             pdf_files.append(f)
#     if not pdf_files:
#         print("No PDF files found in the folder.")
#         return

#     for pdf_file in pdf_files:
#         pdf_path = os.path.join(folder_path, pdf_file)
#         print(f"Processing {pdf_path}...")
#         process_pdf_to_json_with_llama(pdf_path)

#     print("All PDFs have been processed.")