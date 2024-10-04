import json
import re
import pdfplumber

def extract(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages])

    data = {}

    data["Identification"] = {}
    data["Identification"]["ProductName"] = re.search(r"Product Name\s+(.*)", text).group(1).strip()
    data["Identification"]["CASNo"] = re.search(r"CAS No\s+(.*)", text).group(1).strip()

    data["HazardIdentification"] = {}
    data["HazardIdentification"]["SignalWord"] = re.search(r"Signal Word\s+(.*)", text).group(1).strip()
    data["HazardIdentification"]["HazardStatements"] = re.findall(r"Hazard Statements\s+(.*)", text)

    data["Composition"] = []
    for match in re.finditer(r"Component\s+(.*)\s+Weight %(.*)", text):
        component = {}
        component["Name"] = match.group(1).strip()
        component["Percentage"] = match.group(2).strip()
        data["Composition"].append(component)

    return data

file = "C:/Users/HP/OneDrive/Desktop/Data Pre-processing/data_preprocessor/data/acetone-acs-l.pdf"
json_data = extract(file)
jsonFilepath = "acetone.json"
with open(jsonFilepath, 'w') as jsonFile:
    json.dump(json_data, jsonFile, indent=4)