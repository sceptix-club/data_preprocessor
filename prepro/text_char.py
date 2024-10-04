import fitz  # PyMuPDF
import json
import tabula as tb

# Define the path to the PDF file
pdf_path = "data/acetone-acs-l.pdf"
doc = fitz.open(pdf_path)
extracted_data = []

# Define the function for extracting text properties
def flags_decomposer(flags):
    l = []
    if flags & 2 ** 0:
        l.append("superscript")
    if flags & 2 ** 1:
        l.append("italic")
    if flags & 2 ** 2:
        l.append("serifed")
    else:
        l.append("sans")
    if flags & 2 ** 3:
        l.append("monospaced")
    else:
        l.append("proportional")
    if flags & 2 ** 4:
        l.append("bold")
    return ", ".join(l)

# Extract text properties from the PDF
for page_num in range(doc.page_count):
    page = doc[page_num]
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:  # iterate through the text blocks
        for l in b["lines"]:  # iterate through the text lines
            for s in l["spans"]:  # iterate through the text spans
                span_info = {
                    "page": page_num + 1,
                    "position": s["origin"],
                    "text": s["text"],
                    "size": s["size"],
                    "font_flags": flags_decomposer(s["flags"])
                }
                extracted_data.append(span_info)

# Save the extracted data to a JSON file
output_json_file = "extracted_text_properties.json"
with open(output_json_file, "w") as json_file:
    json.dump(extracted_data, json_file, indent=4)
print(f"Text properties extracted and saved to {output_json_file}.")
