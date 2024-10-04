from unstructured.partition.pdf import partition_pdf
import json

# Returns a List[Element] present in the pages of the parsed pdf document
elements = partition_pdf("data/acetone-acs-l (1).pdf")

print(elements)

# def convert_to_json(data):
#     return json.dumps(data, indent=4)

# def save_json_to_file(json_data, output_path):
#     with open(output_path, 'w') as json_file:
#         json_file.write(json_data)

# def main(el, output_json_path):
#     json_data = convert_to_json(el)
#     save_json_to_file(json_data, output_json_path)

# output_json_path = 'structured.json'
# main(elements, output_json_path)