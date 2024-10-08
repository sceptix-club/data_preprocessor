#file location: data_preprocessor/data/acetone-acs-l (1).pdf

import pdfplumber
import json

text=""
with pdfplumber.open("data_preprocessor/data/acetone-acs-l (1).pdf") as pdf:
    first_page = pdf.pages[0] #reading only first pages for testing
    text = first_page.extract_text()
    print(text)


from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
textArr = tokenizer.tokenize(text)
print(textArr)
#sample o/p ['SAFETY', 'DATA', 'SHEET', 'Creation', 'Date', '28', 'Apr', '2009', 'Revision', 'Date', '13', 'Oct', '2023', 'Revision', 'Number']

text2 = ' '.join(textArr)

from transformers import BertTokenizer, BertForTokenClassification
import torch

# Load tokenizer and model for token classification
tokenizer = BertTokenizer.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english')
model = BertForTokenClassification.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english', num_labels=9)  # Change num_labels based on your use case

# Your extracted text from the PDF
text2 = ' '.join(textArr)

# Tokenize the text
tokens = text2.split()
input_tokens = tokenizer(tokens, is_split_into_words=True, return_tensors="pt", padding=True, truncation=True)

# Get predictions
with torch.no_grad():
    outputs = model(**input_tokens)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)

# Define a mapping of label IDs to label names
label_map = {
    0: 'O',      # Outside
    1: 'B-MISC', # Begin Miscellaneous
    2: 'I-MISC', # Inside Miscellaneous
    3: 'B-PER',  # Begin Person
    4: 'I-PER',  # Inside Person
    5: 'B-ORG',  # Begin Organization
    6: 'I-ORG',  # Inside Organization
    7: 'B-LOC',  # Begin Location
    8: 'I-LOC',  # Inside Location
}

# Print the tokens and their predicted labels
for token, pred in zip(tokens, predictions[0].numpy()):
    print(f"Token: {token} -> Label: {label_map[pred]}")

#Token: SAFETY -> Label: O
#Token: DATA -> Label: I-ORG
#Token: SHEET -> Label: I-ORG
#Token: Creation -> Label: I-ORG
#Token: Date -> Label: I-ORG
#Token: 28 -> Label: I-ORG

# Convert to JSON
json_output = json.dumps(tokens, indent=4)
# Print JSON output
print(json_output)
# Optionally, save to a JSON file
with open('token_classification_output.json', 'w') as json_file:
    json.dump(tokens, json_file, indent=4)





