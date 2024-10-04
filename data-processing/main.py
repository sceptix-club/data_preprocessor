import re
import json


extracted_text = """

"""


patterns = {
    "Identification": r"--- 1\. Identification ---\n(.*?)--- 2\. Hazard",
    "HazardIdentification": r"--- 2\. Hazard\(s\) identification ---\n(.*?)--- 3\. Composition",
    "Composition": r"--- 3\. Composition/Information on Ingredients ---\n(.*?)--- 4\. First-aid",
    "FirstAidMeasures": r"--- 4\. First-aid measures ---\n(.*?)--- 5\. Fire-fighting",
    "FireFightingMeasures": r"--- 5\. Fire-fighting measures ---\n(.*?)--- 6\. Accidental release",
    "AccidentalRelease": r"--- 6\. Accidental release measures ---\n(.*?)--- 7\. Handling",
    "HandlingStorage": r"--- 7\. Handling and storage ---\n(.*?)--- 8\. Exposure controls",
    "ExposureControls": r"--- 8\. Exposure controls / personal protection ---\n(.*?)--- 9\. Physical",
    "PhysicalChemicalProperties": r"--- 9\. Physical and chemical properties ---\n(.*?)--- 10\. Stability",
    "StabilityReactivity": r"--- 10\. Stability and reactivity ---\n(.*?)--- 11\. Toxicological",
    "ToxicologicalInformation": r"--- 11\. Toxicological information ---\n(.*?)--- 12\. Ecological",
    "EcologicalInformation": r"--- 12\. Ecological information ---\n(.*?)--- 13\. Disposal",
    "DisposalConsiderations": r"--- 13\. Disposal considerations ---\n(.*?)--- 14\. Transport",
    "TransportInformation": r"--- 14\. Transport information ---\n(.*?)--- 15\. Regulatory",
    "RegulatoryInformation": r"--- 15\. Regulatory information ---\n(.*?)--- 16\. Other",
    "OtherInformation": r"--- 16\. Other information ---\n(.*)"
}



def extract_section(text, pattern):
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else "Section not found"



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


def format_hazard_identification(section_text):
    hazard_data = {}
    lines = section_text.splitlines()

    for line in lines:
        if "Flammable liquids" in line:
            hazard_data["FlammableLiquids"] = line.split("Category")[1].strip()
        elif "Eye Damage" in line:
            hazard_data["EyeDamage"] = line.split("Category")[1].strip()
        elif "Specific target organ toxicity" in line:
            hazard_data["SpecificTargetOrganToxicity"] = line.split("Category")[1].strip()

    return hazard_data

def format_composition(section_text):
    composition_data = []
    lines = section_text.splitlines()

    for line in lines:
        if "Component" in line or "CAS No" in line or "Weight %" in line:
            continue  
        parts = line.split()
        if len(parts) >= 3:
            composition_data.append({
                "ChemicalName": parts[0],
                "CASNumber": parts[1],
                "Concentration": parts[2]
            })

    return composition_data


def format_first_aid_measures(section_text):
    first_aid_data = {}
    lines = section_text.splitlines()

    for line in lines:
        if "Eye Contact" in line:
            first_aid_data["EyeContact"] = line.split("Eye Contact")[1].strip()
        elif "Skin Contact" in line:
            first_aid_data["SkinContact"] = line.split("Skin Contact")[1].strip()
        elif "Inhalation" in line:
            first_aid_data["Inhalation"] = line.split("Inhalation")[1].strip()
        elif "Ingestion" in line:
            first_aid_data["Ingestion"] = line.split("Ingestion")[1].strip()

    return first_aid_data


def format_fire_fighting_measures(section_text):
    fire_fighting_data = {}
    lines = section_text.splitlines()

    for line in lines:
        if "Suitable Extinguishing Media" in line:
            fire_fighting_data["ExtinguishingMedia"] = line.split("Media")[1].strip()
        elif "Flash Point" in line:
            fire_fighting_data["FlashPoint"] = line.split("Flash Point")[1].strip()
        elif "Autoignition Temperature" in line:
            fire_fighting_data["AutoignitionTemperature"] = line.split("Autoignition Temperature")[1].strip()

    return fire_fighting_data


json_data = {}


identification_text = extract_section(extracted_text, patterns["Identification"])
json_data["Identification"] = format_identification(identification_text)

hazard_identification_text = extract_section(extracted_text, patterns["HazardIdentification"])
json_data["HazardIdentification"] = format_hazard_identification(hazard_identification_text)

composition_text = extract_section(extracted_text, patterns["Composition"])
json_data["Composition"] = format_composition(composition_text)

first_aid_measures_text = extract_section(extracted_text, patterns["FirstAidMeasures"])
json_data["FirstAidMeasures"] = format_first_aid_measures(first_aid_measures_text)

fire_fighting_measures_text = extract_section(extracted_text, patterns["FireFightingMeasures"])
json_data["FireFightingMeasures"] = format_fire_fighting_measures(fire_fighting_measures_text)

print(json_data)