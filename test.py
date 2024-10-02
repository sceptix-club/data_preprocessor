import pdfplumber

with pdfplumber.open(r'data\acetone-acs-l.pdf') as pdf:
    
    text1 = []
    
    for page in pdf.pages:
       
        text = page.extract_text()
        if text: 
            text1.append(text)

text2 = "\n".join(text1)

print(text2)

with open("extracted_text.txt", "w") as text_file:
    text_file.write(text2)