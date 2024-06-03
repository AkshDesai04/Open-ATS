import fitz
from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output

def ingest_profile(resume_path):
    text = ""
    try:
        # Open the resume PDF file
        with fitz.open(resume_path) as doc:
            for page in doc:
                text += page.get_text()

    except Exception as e:
        print(f"Error occurred while extracting text: {e}")

    return text

def ingest_profile_png(resume_path):
    text = ""
    try:
        pytesseract.pytesseract.tesseract_cmd =r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

        img = np.array(Image.open(resume_path))
        text = pytesseract.image_to_string(img)

    except Exception as e:
        print(f"Error occurred while extracting text: {e}")

    return text

def ingest_job_description(job_description_path):
    position = ""
    expected_experience = 0
    skills = []
    tools = []
    value = []  # This is a list of dictionaries

    try:
        with open(job_description_path, 'r') as file:
            for line in file:
                key, val = line.strip().split(':', 1)  # Split only on the first colon
                if key == 'position':
                    position = val.strip()
                elif key == 'expected experience':
                    expected_experience = int(val.strip().split()[0])
                elif key == 'skills':
                    skills = [skill.strip() for skill in val.split(',')]
                elif key == 'tools':
                    tools = [tool.strip() for tool in val.split(',')]
                elif key == 'value':
                    # Split the value string into components and parse each one
                    value_parts = val.split(',')
                    value_dict = {}
                    for part in value_parts:
                        sub_key, sub_val = part.strip().split('=')
                        value_dict[sub_key] = int(sub_val)
                    value.append(value_dict)

    except Exception as e:
        print(f"Error occurred while reading job description: {e}")

    requirement = {
        'position': position,
        'expected_experience': expected_experience,
        'skills': skills,
        'tools': tools,
        'value': value
    }

    return requirement