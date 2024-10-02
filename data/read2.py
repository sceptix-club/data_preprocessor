import pdfplumber

# Use raw string format to avoid issues with backslashes
file_path = r"C:\Users\HP\OneDrive\Desktop\data_preprocessor\data\acetone-acs-l (1).pdf"

# Open the PDF
with pdfplumber.open(file_path) as pdf:
    # Iterate through each page of the PDF
    for page_num, page in enumerate(pdf.pages):
        # Extract text from the page
        text = page.extract_text()
        print(f"Text from page {page_num + 1}:")
        print(text)

        # Extract tables from the page
        tables = page.extract_tables()  # Use extract_tables() instead of extract_table()
        print(f"Tables from page {page_num + 1}:")
        for table in tables:
            for row in table:
                print(row)

        # Extract images from the page
        images = page.images  # Use page.images to get a list of images on the page
        if images:
            print(f"Images on page {page_num + 1}:")
            for image in images:
                print(f"Image on page {page_num + 1}: {image}")
                # Note: PDFPlumber does not extract the image data itself, only metadata like its position, width, height, etc.
                # For extracting image data, you might need another library like Pillow to render the PDF into an image.


