import PyPDF2
import easyocr
import re
import json
from pdf2image import convert_from_path  # Convert PDF pages to images
import camelot

class SafetyDataSheetParser:
    def __init__(self, pdf_path, output_json_path):
        self.pdf_path = pdf_path
        self.output_json_path = output_json_path
        self.reader = easyocr.Reader(['en'], gpu=False)  # Initialize EasyOCR reader

    def extract_pdf_text(self):
        try:
            # First, try to extract text with PyPDF2
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""  # Avoid NoneType errors
            if text.strip():
                print("PDF text extraction successful with PyPDF2!")
                return text
            else:
                raise ValueError("PyPDF2 extraction failed. Attempting OCR...")

        except Exception as e:
            print(f"Error during PDF extraction with PyPDF2: {e}")
            return self.extract_text_with_ocr()  # Use EasyOCR as fallback

    def extract_text_with_ocr(self):
        try:
            print("Extracting text using EasyOCR...")
            # Convert PDF pages to images for OCR processing
            images = convert_from_path(self.pdf_path)
            text = ""
            for img in images:
                text += "\n".join(self.reader.readtext(img, detail=0))  # Extract text from image
            if text.strip():
                print("Text extraction with EasyOCR successful!")
                return text
            else:
                raise ValueError("OCR text extraction failed.")
        except Exception as e:
            print(f"Error during OCR extraction: {e}")
            return ""

class SafetyDataSheetParser:
    def __init__(self, pdf_path, output_json_path):
        self.pdf_path = pdf_path
        self.output_json_path = output_json_path

        self.sds_data = {
            "SafetyDataSheet": {
                "Identification": {},
                "HazardIdentification": {},
                "Composition/Information on Ingredients": {},
                "First-aid measures": {},
                "Fire-fighting measures": {},
                "Accidental release measures": {},
                "Handling and storage": {},
                "Exposure controls/personal protection": {},
                "Physical and chemical properties": {},
                "Stability and reactivity": {},
                "Toxicological information": {},
                "Ecological information": {},
                "Disposal considerations": {},
                "Transport information": {},
                "Regulatory information": {},
                "Other information": {},
                "Tables": []
            }
        }

    def extract_tables(self):
        try:
            print("Extracting tables using Camelot...")
            tables = camelot.read_pdf(self.pdf_path, pages='all', strip_text='\n')  # Read all tables in the PDF
            table_data = []
            for table in tables:
                table_data.append(table.df.to_dict())  # Convert tables to dict (can also save as CSV/JSON)
            self.sds_data["SafetyDataSheet"]["Tables"] = table_data
            print(f"{len(tables)} table(s) extracted successfully!")
        except Exception as e:
            print(f"Error during table extraction: {e}")

    def extract_pdf_text(self):
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""  # Avoid NoneType errors
            if not text:
                raise ValueError("PDF text extraction failed or PDF is empty.")
            print("PDF text extraction successful!")
            return text
        except Exception as e:
            print(f"Error during PDF extraction: {e}")
            return ""

    def parse_identification_section(self, text):
        try:
            product_name_match = re.search(r'Product Name\s+(.+)', text)
            cat_no_match = re.search(r'Cat No. :\s+(.+)', text)
            cas_no_match = re.search(r'CAS No\s+(\d+-\d+-\d+)', text)
            recommended_use_match = re.search(r'Recommended Use\s+(.+)', text)
            supplier_match = re.search(r'Details of the supplier.+\n(.+)\n(.+)\n(.+)', text)

            self.sds_data["SafetyDataSheet"]["Identification"] = {
                "ProductName": product_name_match.group(1) if product_name_match else "N/A",
                "Cat No.": cat_no_match.group(1) if cat_no_match else "N/A",
                "CASNo": cas_no_match.group(1) if cas_no_match else "N/A",
                "RecommendedUse": recommended_use_match.group(1) if recommended_use_match else "N/A",
                "Supplier": {
                    "Name": supplier_match.group(1) if supplier_match else "N/A",
                    "Address": supplier_match.group(2) if supplier_match else "N/A",
                    "Telephone": supplier_match.group(3) if supplier_match else "N/A"
                }
            }
            print("Identification section parsed successfully!")
        except Exception as e:
            print(f"Error during Identification section parsing: {e}")

    def parse_hazard_identification_section(self, text):
        try:
            signal_word_match = re.search(r'Signal Word\s+(.+)', text)
            hazard_statements = re.findall(r'Hazard Statements\s+(.+)', text)
            precautionary_statements = re.findall(r'Precautionary Statements\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["HazardIdentification"] = {
                "SignalWord": signal_word_match.group(1) if signal_word_match else "N/A",
                "HazardStatements": hazard_statements if hazard_statements else ["N/A"],
                "PrecautionaryStatements": precautionary_statements if precautionary_statements else ["N/A"]
            }
            print("Hazard Identification section parsed successfully!")
        except Exception as e:
            print(f"Error during Hazard Identification section parsing: {e}")

    def parse_composition_section(self, text):
        try:
            component_match = re.search(r'Component\s+(.+)\nCAS No\s+(.+)\nWeight %\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Composition/Information on Ingredients"] = {
                "Component": component_match.group(1) if component_match else "N/A",
                "CASNo": component_match.group(2) if component_match else "N/A",
                "WeightPercentage": component_match.group(3) if component_match else "N/A"
            }
            print("Composition section parsed successfully!")
        except Exception as e:
            print(f"Error during Composition section parsing: {e}")

    def parse_first_aid_measures(self, text):
        try:
            general_advice_match = re.search(r'General Advice\s+(.+)', text)
            eye_contact_match = re.search(r'Eye Contact\s+(.+)', text)
            skin_contact_match = re.search(r'Skin Contact\s+(.+)', text)
            inhalation_match = re.search(r'Inhalation\s+(.+)', text)
            ingestion_match = re.search(r'Ingestion\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["First-aid measures"] = {
                "GeneralAdvice": general_advice_match.group(1) if general_advice_match else "N/A",
                "EyeContact": eye_contact_match.group(1) if eye_contact_match else "N/A",
                "SkinContact": skin_contact_match.group(1) if skin_contact_match else "N/A",
                "Inhalation": inhalation_match.group(1) if inhalation_match else "N/A",
                "Ingestion": ingestion_match.group(1) if ingestion_match else "N/A"
            }
            print("First-aid measures section parsed successfully!")
        except Exception as e:
            print(f"Error during First-aid measures section parsing: {e}")

    def parse_fire_fighting_measures(self, text):
        try:
            extinguishing_media_match = re.search(r'Suitable Extinguishing Media\s+(.+)', text)
            fire_hazards_match = re.search(r'Specific Hazards Arising from the Chemical\s+(.+)', text)
            protective_equipment_match = re.search(r'Protective Equipment and Precautions for Firefighters\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Fire-fighting measures"] = {
                "ExtinguishingMedia": extinguishing_media_match.group(1) if extinguishing_media_match else "N/A",
                "SpecificHazards": fire_hazards_match.group(1) if fire_hazards_match else "N/A",
                "ProtectiveEquipment": protective_equipment_match.group(1) if protective_equipment_match else "N/A"
            }
            print("Fire-fighting measures section parsed successfully!")
        except Exception as e:
            print(f"Error during Fire-fighting measures section parsing: {e}")

    def parse_accidental_release_measures(self, text):
        try:
            personal_precautions_match = re.search(r'Personal Precautions\s+(.+)', text)
            environmental_precautions_match = re.search(r'Environmental Precautions\s+(.+)', text)
            containment_cleanup_match = re.search(r'Methods for Containment and Clean Up\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Accidental release measures"] = {
                "PersonalPrecautions": personal_precautions_match.group(1) if personal_precautions_match else "N/A",
                "EnvironmentalPrecautions": environmental_precautions_match.group(1) if environmental_precautions_match else "N/A",
                "MethodsForContainmentAndCleanUp": containment_cleanup_match.group(1) if containment_cleanup_match else "N/A"
            }
            print("Accidental release measures section parsed successfully!")
        except Exception as e:
            print(f"Error during Accidental release measures section parsing: {e}")

    def parse_handling_and_storage(self, text):
        try:
            handling_match = re.search(r'Handling\s+(.+)', text)
            storage_match = re.search(r'Storage\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Handling and storage"] = {
                "Handling": handling_match.group(1) if handling_match else "N/A",
                "Storage": storage_match.group(1) if storage_match else "N/A"
            }
            print("Handling and storage section parsed successfully!")
        except Exception as e:
            print(f"Error during Handling and storage section parsing: {e}")

    def parse_exposure_controls(self, text):
        try:
            exposure_guidelines_match = re.search(r'Exposure Guidelines\s+(.+)', text)
            engineering_controls_match = re.search(r'Engineering Measures\s+(.+)', text)
            personal_protection_match = re.search(r'Personal Protective Equipment\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Exposure controls/personal protection"] = {
                "ExposureGuidelines": exposure_guidelines_match.group(1) if exposure_guidelines_match else "N/A",
                "EngineeringControls": engineering_controls_match.group(1) if engineering_controls_match else "N/A",
                "PersonalProtection": personal_protection_match.group(1) if personal_protection_match else "N/A"
            }
            print("Exposure controls/personal protection section parsed successfully!")
        except Exception as e:
            print(f"Error during Exposure controls/personal protection section parsing: {e}")

    def parse_physical_and_chemical_properties(self, text):
        try:
            physical_state_match = re.search(r'Physical State\s+(.+)', text)
            appearance_match = re.search(r'Appearance\s+(.+)', text)
            odor_match = re.search(r'Odor\s+(.+)', text)
            pH_match = re.search(r'pH\s+(.+)', text)
            melting_point_match = re.search(r'Melting Point/Range\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Physical and chemical properties"] = {
                "PhysicalState": physical_state_match.group(1) if physical_state_match else "N/A",
                "Appearance": appearance_match.group(1) if appearance_match else "N/A",
                "Odor": odor_match.group(1) if odor_match else "N/A",
                "pH": pH_match.group(1) if pH_match else "N/A",
                "MeltingPoint": melting_point_match.group(1) if melting_point_match else "N/A"
            }
            print("Physical and chemical properties section parsed successfully!")
        except Exception as e:
            print(f"Error during Physical and chemical properties section parsing: {e}")

    def parse_stability_and_reactivity(self, text):
        try:
            stability_match = re.search(r'Stability\s+(.+)', text)
            conditions_to_avoid_match = re.search(r'Conditions to Avoid\s+(.+)', text)
            incompatible_materials_match = re.search(r'Incompatible Materials\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Stability and reactivity"] = {
                "Stability": stability_match.group(1) if stability_match else "N/A",
                "ConditionsToAvoid": conditions_to_avoid_match.group(1) if conditions_to_avoid_match else "N/A",
                "IncompatibleMaterials": incompatible_materials_match.group(1) if incompatible_materials_match else "N/A"
            }
            print("Stability and reactivity section parsed successfully!")
        except Exception as e:
            print(f"Error during Stability and reactivity section parsing: {e}")

    def parse_toxicological_information(self, text):
        try:
            acute_toxicity_match = re.search(r'Acute Toxicity\s+(.+)', text)
            symptoms_match = re.search(r'Symptoms\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Toxicological information"] = {
                "AcuteToxicity": acute_toxicity_match.group(1) if acute_toxicity_match else "N/A",
                "Symptoms": symptoms_match.group(1) if symptoms_match else "N/A"
            }
            print("Toxicological information section parsed successfully!")
        except Exception as e:
            print(f"Error during Toxicological information section parsing: {e}")

    def parse_ecological_information(self, text):
        try:
            ecotoxicity_match = re.search(r'Ecotoxicity\s+(.+)', text)
            bioaccumulation_match = re.search(r'Bioaccumulation\s+(.+)', text)
            mobility_match = re.search(r'Mobility\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Ecological information"] = {
                "Ecotoxicity": ecotoxicity_match.group(1) if ecotoxicity_match else "N/A",
                "Bioaccumulation": bioaccumulation_match.group(1) if bioaccumulation_match else "N/A",
                "Mobility": mobility_match.group(1) if mobility_match else "N/A"
            }
            print("Ecological information section parsed successfully!")
        except Exception as e:
            print(f"Error during Ecological information section parsing: {e}")

    def parse_disposal_considerations(self, text):
        try:
            waste_disposal_match = re.search(r'Waste Disposal Methods\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Disposal considerations"] = {
                "WasteDisposal": waste_disposal_match.group(1) if waste_disposal_match else "N/A"
            }
            print("Disposal considerations section parsed successfully!")
        except Exception as e:
            print(f"Error during Disposal considerations section parsing: {e}")

    def parse_transport_information(self, text):
        try:
            un_number_match = re.search(r'UN-No\s+(.+)', text)
            proper_shipping_name_match = re.search(r'Proper Shipping Name\s+(.+)', text)
            hazard_class_match = re.search(r'Hazard Class\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Transport information"] = {
                "UNNumber": un_number_match.group(1) if un_number_match else "N/A",
                "ProperShippingName": proper_shipping_name_match.group(1) if proper_shipping_name_match else "N/A",
                "HazardClass": hazard_class_match.group(1) if hazard_class_match else "N/A"
            }
            print("Transport information section parsed successfully!")
        except Exception as e:
            print(f"Error during Transport information section parsing: {e}")

    def parse_regulatory_information(self, text):
        try:
            regulatory_match = re.search(r'U\.S\. Federal Regulations\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Regulatory information"] = {
                "USFederalRegulations": regulatory_match.group(1) if regulatory_match else "N/A"
            }
            print("Regulatory information section parsed successfully!")
        except Exception as e:
            print(f"Error during Regulatory information section parsing: {e}")

    def parse_other_information(self, text):
        try:
            preparation_date_match = re.search(r'Creation Date\s+(.+)', text)
            revision_date_match = re.search(r'Revision Date\s+(.+)', text)

            self.sds_data["SafetyDataSheet"]["Other information"] = {
                "CreationDate": preparation_date_match.group(1) if preparation_date_match else "N/A",
                "RevisionDate": revision_date_match.group(1) if revision_date_match else "N/A"
            }
            print("Other information section parsed successfully!")
        except Exception as e:
            print(f"Error during Other information section parsing: {e}")

    def process_sds(self):
        try:
            text = self.extract_pdf_text()

            if text:
                # Parse all relevant sections
                self.parse_identification_section(text)
                self.parse_hazard_identification_section(text)
                self.parse_composition_section(text)
                self.parse_first_aid_measures(text)
                self.parse_fire_fighting_measures(text)
                self.parse_accidental_release_measures(text)
                self.parse_handling_and_storage(text)
                self.parse_exposure_controls(text)
                self.parse_physical_and_chemical_properties(text)
                self.parse_stability_and_reactivity(text)
                self.parse_toxicological_information(text)
                self.parse_ecological_information(text)
                self.parse_disposal_considerations(text)
                self.parse_transport_information(text)
                self.parse_regulatory_information(text)
                self.parse_other_information(text)
                self.extract_tables()

                # Save the structured data as JSON
                with open(self.output_json_path, 'w') as json_file:
                    json.dump(self.sds_data, json_file, indent=4)

                print(f"SDS data successfully saved to {self.output_json_path}")
            else:
                print("No text extracted from the PDF.")
        except Exception as e:
            print(f"Error during SDS processing: {e}")

# Example Usage:
if __name__ == "__main__":
    pdf_file = "data/acetone-acs-l.pdf"  # Path to your PDF file
    output_json = "output_sds.json"  # Path to save the output JSON

    parser = SafetyDataSheetParser(pdf_file, output_json)
    parser.process_sds()
