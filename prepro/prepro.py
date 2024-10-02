import re 

from pdfminer.high_level import extract_text

text = extract_text('./data/acetone-acs-l.pdf')
print(text)