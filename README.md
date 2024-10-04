# Project Report: Data Pre-processing

## 1. Initial Approach: Using Regex and Spacy for Data Extraction
The first approach involved using a combination of **regular expressions (regex)** and **Spacy** for data extraction. The plan was to:
- Use **regex patterns** to identify and extract the headings from the data.
- Use **Spacy**, a powerful natural language processing library, to extract the subheadings based on named entity recognition and other language features.

This method was partially effective but had limitations in identifying all necessary data due to inconsistencies in the formatting of headings and subheadings.

## 2. Extracting Data Based on Font Styles
The next idea involved attempting to extract information based on the **font styles** in the document. For example:
- **Blue-colored text** was identified as main headings.
- **Black-colored text** was identified as subheadings.

This approach relied on font color and style metadata, but it proved challenging to implement consistently across different documents, as not all documents had well-defined font styling for hierarchical structures.

## 3. Final Approach: Regex and Section-based Functions
The final approach used **regex** for pattern matching and involved creating **separate functions** for each section. For instance:
- A function was designed to extract information specifically from the **Identification** section of a document, such as:

```python
def format_identification(section_text):
    lines = section_text.splitlines()
    identification_data = {}
    for line in lines:
        if "Product Name" in line and ":" in line:
            identification_data["ProductName"] = line.split(":")[1].strip()
        elif "Product Name" in line and ":" not in line:
            identification_data["ProductName"] = line.replace("Product Name", "").strip()
        elif "Cat No." in line and ":" in line:
            identification_data["CatNumbers"] = [item.strip() for item in line.split(":")[1].strip().split(";")]
        elif "Cat No." in line and ":" not in line:
            identification_data["CatNumbers"] = [item.strip() for item in line.replace("Cat No.", "").strip().split(";")]
    return identification_data
