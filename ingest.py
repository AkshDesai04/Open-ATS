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

resume_path = "./ignore/Aksh.pdf"
print(ingest_profile(resume_path)) #0.13 secs per run on #test_resume0 (without print)