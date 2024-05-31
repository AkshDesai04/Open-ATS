import fitz

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

def ingest_job_description(job_description_path):
    position = ""
    expected_experience = 0
    skills = []
    tools = []
    # value = [] TODO

    try:
        with open(job_description_path, 'r') as file:
            for line in file:
                key, val = line.strip().split(':')
                if key == 'position':
                    position = val.strip()
                elif key == 'expected experience':
                    expected_experience = int(val.strip().split()[0])
                elif key == 'skills':
                    skills = [skill.strip() for skill in val.split(',')]
                elif key == 'tools':
                    tools = [tool.strip() for tool in val.split(',')]
                # elif key == 'value':
                #     value = [{'experience': int(val.strip().split('=')[1])}, {'skill': int(val.strip().split('=')[2])}, {'tools': int(val.strip().split('=')[3])}]
                #TODO: Fix this. Taking too long right now hence skipping for later.

    except Exception as e:
        print(f"Error occurred while reading job description: {e}")

    requirement = {
        'position': position,
        'expected_experience': expected_experience,
        'skills': skills,
        'tools': tools,
        # 'value': value TODO
    }

    # print(requirement)

    return requirement