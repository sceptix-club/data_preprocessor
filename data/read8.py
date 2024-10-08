import pdfplumber

def process_pdf_with_font_details(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract characters with their properties
            chars = page.chars
            
            # Initialize a variable to hold the current word
            current_word = ""
            current_font_name = None
            current_font_size = None
            current_fill = None
            
            for char in chars:
                text = char['text']
                font_size = char['size']
                font_name = char['fontname']
                fill_color = char.get('fill')  # Get fill color
                
                # Check for spaces to identify word boundaries
                if text.isspace():
                    if current_word:
                        # Print the accumulated word with font details
                        print(f"'{current_word}' (Font size: {current_font_size}, Font style: {current_font_name}, Font color: {current_fill})")
                        current_word = ""
                        current_font_name = None
                        current_font_size = None
                        current_fill = None
                else:
                    current_word += text
                    # Store the font details of the current character
                    current_font_name = font_name
                    current_font_size = font_size
                    current_fill = fill_color  # Store the fill color
            
            # Print the last word if it exists
            if current_word:
                print(f"'{current_word}' (Font size: {current_font_size}, Font style: {current_font_name}, Font color: {current_fill})")

# Example usage
pdf_path = r"C:\Users\HP\OneDrive\Desktop\data_preprocessor\data\acetone-acs-l (1).pdf"

process_pdf_with_font_details(pdf_path)
