import os
import pdfplumber
import re
import json

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file):
    all_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"
    return all_text


def extract_field(text, field_label, after_label_chars=50):
    field_pattern = re.escape(field_label) + r".{0," + str(after_label_chars) + r"}"
    match = re.search(field_pattern, text)
    if match:
        return re.sub(r'\n+', ' ', match.group(0).replace(field_label, '').strip())
    return "Field not found"


def extract_list(text, field_label, stop_at_label=None):
    field_pattern = re.escape(field_label) + r"(.*?)(?=" + re.escape(stop_at_label) + r"|\Z)" if stop_at_label else re.escape(field_label) + r"(.*?)$"
    match = re.search(field_pattern, text, re.S)
    if match:
        return [statement.strip() for statement in match.group(1).split("\n") if statement.strip()]
    return []

def process_pdf(pdf_file, output_folder):
    pdf_text = extract_text_from_pdf(pdf_file)

    # Extract fields
    product_name = extract_field(pdf_text, "Product Name", 50)
    cas_number = extract_field(pdf_text, "CAS No", 50)
    synonyms = extract_field(pdf_text, "Synonyms", 100)
    recommended_use = extract_field(pdf_text, "Recommended Use", 50)
    uses_advised_against = extract_field(pdf_text, "Uses advised against",100)
    company_name = extract_field(pdf_text, "Company\n", 50)
    address = extract_field(pdf_text, "One", 100)
    telephone = extract_field(pdf_text, "Tel: ", 20)
    signal_word = extract_field(pdf_text, "Signal Word\n", 20)
    eye_damage = extract_field(pdf_text, "Serious Eye Damage/Eye Irritation", 20)
    dust = extract_field(pdf_text, "Combustible dust", 20)
    general_advice = extract_field(pdf_text, "General Advice", 20)
    eye_contact = extract_field(pdf_text, "Eye Contact", 20)
    skin_contact = extract_field(pdf_text, "Skin Contact", 20)
    inhalation = extract_field(pdf_text, "Inhalation", 20)
    ingestion = extract_field(pdf_text, "Ingestion", 100)
    notes = extract_field(pdf_text, "Notes to Physician", 20)
    suitable_extinguishing_media = extract_field(pdf_text, "Suitable Extinguishing Media", 250)
    hazardous_combustion_products = extract_field(pdf_text, "Hazardous Combustion Products", 250)
    flash_point = extract_field(pdf_text, "Flash Point", 20)
    autoignite = extract_field(pdf_text, "Autoignition Temperature", 20)
    physical = extract_field(pdf_text, "Physical State", 20)
    appearance = extract_field(pdf_text, "Appearance", 20)
    odor = extract_field(pdf_text, "Odor", 20)
    ph = extract_field(pdf_text, "pH", 20)
    melting_point = extract_field(pdf_text, "Melting Point/Range", 20)
    boiling_point = extract_field(pdf_text, "Boiling Point/Range", 20)
    vapor_pressure = extract_field(pdf_text, "Vapor Pressure", 20)
    vapor_density = extract_field(pdf_text, "Vapor Density", 20)
    specific_gravity = extract_field(pdf_text, "Specific Gravity", 20)
    solubility = extract_field(pdf_text, "Solubility", 20)
    molecular_formula = extract_field(pdf_text, "Molecular Formula", 20)
    molecular_weight = extract_field(pdf_text, "Molecular Weight", 20)
    oral_ld50 = extract_field(pdf_text, "Oral LD50", 20)
    dermal_ld50 = extract_field(pdf_text, "Dermal LD50", 20)
    inhalation_lc50 = extract_field(pdf_text, "Inhalation LC50", 20)
    irritant = extract_field(pdf_text, "Irritation", 20)
    reproductive_effects = extract_field(pdf_text, "Reproductive Effects", 50)
    freshwater_algae = extract_field(pdf_text, "Freshwater Algae", 20)
    freshwater_fish = extract_field(pdf_text, "Freshwater Fish", 20)
    water_flea = extract_field(pdf_text, "Water Flea", 20)
    microtox = extract_field(pdf_text, "Microtox", 20)
    bioaccumulation = extract_field(pdf_text, "Bioaccumulation", 50)
    mobility = extract_field(pdf_text, "Mobility", 50)
    preapre_date = extract_field(pdf_text, "Prepared By", 100)
    revision_date = extract_field(pdf_text, "Revision Date", 50)
    disclaimer = extract_field(pdf_text, "Disclaimer\n", 200)
    california_prop65 = extract_field(pdf_text, "California Prop 65", 100)
    dot_regulated = extract_field(pdf_text, "DOT Regulated", 50)
    marine_pollutant = extract_field(pdf_text, "Marine Pollutant", 50)


    # Extract lists
    hazard_statements = extract_list(pdf_text, "Hazard Statements", "Precautionary Statements")
    precautionary_prevention = extract_list(pdf_text, "Prevention", "Response")
    precautionary_response = extract_list(pdf_text, "Response", "Storage")
    precautionary_storage = extract_list(pdf_text, "Storage", "Disposal")
    precautionary_disposal = extract_list(pdf_text, "Disposal\n", "Hazards not otherwise classified (HNOC)")
    components = extract_list(pdf_text, "Component", "First-aid measures")
    special_firefighting_instructions = extract_list(pdf_text, "Special firefighting instructions", "Accidental release measures")
    handling = extract_list(pdf_text, "\nHandling", "Exposure controls / personal protection")
    storage = extract_list(pdf_text, "Storage.", "Exposure controls / personal protection")

    # structure
    safety_data_sheet = {
        "SafetyDataSheet": {
            "Identification": {
                "ProductName": product_name,
                "CASNumber": cas_number,
                "Synonyms": synonyms,
                "RecommendedUse": recommended_use,
                "UsesAdvisedAgainst": uses_advised_against,
                "Company": {
                    "Name": company_name,
                    "Address": address,
                    "Telephone": telephone
                }
            },
            "HazardsIdentification": {
                "SignalWord": signal_word,
                "HazardStatements": hazard_statements,
                "HazardCategories": {
                    "EyeDamage": eye_damage,
                    "CombustibleDust": dust
                },
                "PrecautionaryStatements": {
                "Prevention": precautionary_prevention,
                "Eyes": precautionary_response,
                "Storage": precautionary_storage,
                "HazardsNotClassified": precautionary_disposal
                }
            },
            "CompositionInformation": {
                "Components": components
            },
            "FirstAidMeasures": {
                "GeneralAdvice": general_advice,
                "EyeContact": eye_contact,
                "SkinContact": skin_contact,
                "Inhalation": inhalation,
                "Ingestion": ingestion,
                "NotesToPhysician": notes
            },
            "FireFightingMeasures": {
                "SuitableExtinguishingMedia": suitable_extinguishing_media,
                "HazardousCombustionProducts": hazardous_combustion_products,
                "FlashPoint": flash_point,
                "AutoignitionTemperature": autoignite,
                "SpecialFirefightingInstructions": special_firefighting_instructions
            },
            "HandlingAndStorage": {
                "Handling": handling,
                "Storage": storage
            },
            "PhysicalChemicalProperties": {
                "PhysicalState": physical,
                "Appearance": appearance,
                "Odor": odor,
                "pH": ph,
                "MeltingPoint": melting_point,
                "BoilingPoint": boiling_point,
                "VaporPressure": vapor_pressure,
                "VaporDensity": vapor_density,
                "SpecificGravity": specific_gravity,
                "FlashPoint": flash_point,
                "AutoignitionTemperature": autoignite,
                "Solubility": solubility,
                "MolecularFormula": molecular_formula,
                "MolecularWeight": molecular_weight
            },
            "ToxicologicalInformation": {
                "AcuteToxicity": {
                    "OralLD50": oral_ld50,
                    "DermalLD50": dermal_ld50,
                    "InhalationLC50": inhalation_lc50
                },
                "Irritation": irritant,
                "ReproductiveEffects": reproductive_effects
            },
            "EcologicalInformation": {
                "Ecotoxicity": {
                    "FreshwaterAlgae": freshwater_algae,
                    "FreshwaterFish": freshwater_fish,
                    "WaterFlea": water_flea,
                    "Microtox": microtox
                },
                "Bioaccumulation": bioaccumulation,
                "Mobility": mobility
            },
            "RegulatoryInformation": {
                "CaliforniaProp65": california_prop65,
                "USDepartmentOfTransportation": {
                    "DOTRegulated": dot_regulated,
                    "MarinePollutant": marine_pollutant
                }
            },
            "OtherInformation": {
                "PreparedBy": preapre_date,
                "RevisionDate": revision_date,
                "Disclaimer": disclaimer
            }
        }
    }

    # save as json
    json_filename = os.path.splitext(os.path.basename(pdf_file))[0] + ".json"
    json_filepath = os.path.join(output_folder, json_filename)
    with open(json_filepath, "w") as json_file:
        json.dump(safety_data_sheet, json_file, indent=4)

    print(f"Processed {pdf_file} -> {json_filepath}")

# process all pdf
def process_all_pdfs(pdf_folder, output_folder):
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            process_pdf(pdf_path, output_folder)

# Example usage
pdf_folder = "/home/roche-jeethan/Codes/notebook/data_preprocessor/data"  # input folder, change while using
output_folder = "/home/roche-jeethan/Codes/notebook/data_preprocessor/json_output"  # output folder. change while using

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

process_all_pdfs(pdf_folder, output_folder)