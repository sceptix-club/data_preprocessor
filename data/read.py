from pypdf import PdfReader

reader = PdfReader("C:/Users/HP/OneDrive/Desktop/dataprocess/data_preprocessor/data/acetone-acs-l (1).pdf")

# Print the number of pages in the PDF
print(f"There are {len(reader.pages)} Pages")

# Get the first page (index 0) 
page = reader.pages[0]
# Use extract_text() to get the text of the page
print(page.extract_text())

# Go through every page and get the text
for i in range(len(reader.pages)):
  page = reader.pages[i]
  print(page.extract_text())
  