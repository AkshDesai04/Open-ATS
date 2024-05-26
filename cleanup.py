import re
from datetime import datetime

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

# Ensure nltk resources are downloaded
nltk.download('stopwords')
nltk.download('punkt')

def clean_resume(resume_text):
    stop_words = set(stopwords.words('english'))

    def clean_line(line):
        # Keep only alphanumeric characters and some symbols
        line = re.sub(r'[^a-zA-Z0-9@.+#\s-]', ' ', line)
        # Replace multiple spaces with a single space
        line = re.sub(r'\s+', ' ', line).strip()
        line = line.lower()

        # Remove stop words
        words = line.split()
        words = [word for word in words if word not in stop_words]
        return ' '.join(words)

    # Process each line of the resume
    lines = resume_text.split('\n')
    cleaned_lines = [clean_line(line) for line in lines]
    cleaned_resume = '\n'.join(cleaned_lines)

    return cleaned_resume

def divide_resume(resume_text):
    def extract_experience(resume_text):
        recorded_years = []
        # Define regular expression pattern to extract experience section
        experience_pattern = r'(?i)\b(?:intern|experience)\b[\s\S]+?(?=\b(?:education|projects|skills|certifications|publications|volunteering|honors|awards|memberships|leadership|licenses|clinical|work|related|relevant|technical|professional|experience|projects|certifications)\b)'

        # Search for matches
        experience_matches = re.findall(experience_pattern, resume_text)

        # Calculate total experience
        total_years = 0
        for match in experience_matches:
            # Extract date ranges
            date_ranges = re.findall(r'(?:(?:\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?)\s+\d{4})|(?:\d{4}))', match)
            
            # Calculate experience duration for each date range
            for date in date_ranges:
                if date.strip().isdigit() and int(date.strip()) <= datetime.now().year and int(date.strip()) not in recorded_years:
                    recorded_years.append(int(date.strip()))
                    # If only year is provided, assume it as a full year of experience
                    total_years += 1
                else:
                    # If month and year are provided, extract month and year
                    dates = date.split()
                    if len(dates) == 2:  # Ensure there are both month and year
                        month = dates[0][:3]  # Take first 3 letters to handle abbreviated month names
                        year = int(dates[1])
                        total_years += ((datetime.now().year - year) * 12 + (datetime.now().month - (['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(month) + 1))) / 12
        
        return round(total_years, 1)

    def extract_skills(resume_text):
        # Define pattern to identify the skills section
        skills_pattern = r'(?i)\bskills\b[\s\S]+?(?=\b(?:education|projects|experience|certifications|publications|volunteering|honors|awards|memberships|leadership|licenses|clinical|work|related|relevant|technical|professional|experience|projects|certifications)\b)'

        # Search for matches
        skills_matches = re.findall(skills_pattern, resume_text)

        if skills_matches:
            # Extract the skills from the matched section
            skills_text = skills_matches[0]
            skills = re.findall(r'\b\w+\b', skills_text)
            return skills
        return []

    # Define regular expressions for extracting information
    phone_pattern = re.compile(r'(?:(?:\+?\d{1,3})[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', re.IGNORECASE)
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE)
    qualifications = [r"Ph\.?D\.?", r"M\.?S\.?C\.?\s?[A-Z]*", r"B\.?S\.?C\.?\s?[A-Z]*", r"B\.?A\.?", r"M\.?A\.?", r"Associate Degree", r"High School Diploma"]

    # Extract name from the first line
    lines = resume_text.split('\n')
    name = lines[0].strip()
    experience_years = extract_experience(resume_text)
    skills = extract_skills(resume_text)
    highest_qualification = None

    # Extract phone and email using regular expressions
    phone_match = re.search(phone_pattern, resume_text)
    phone = phone_match.group().strip() if phone_match else ""
    
    email_match = re.search(email_pattern, resume_text)
    email = email_match.group().strip() if email_match else ""

    for qualification_pattern in qualifications:
        match = re.search(qualification_pattern, resume_text, re.IGNORECASE)
        if match:
            highest_qualification = match.group(0)
            break

    # Return extracted information as a dictionary
    # print({'name': name, 'phone': phone, 'email': email, 'experience_years': experience_years, 'qualification': highest_qualification, 'skills': skills})
    return {'name': name, 'phone': phone, 'email': email, 'experience_years': experience_years, 'qualification': highest_qualification, 'skills': skills, 'work experience': extract_companies(resume_text)}

def extract_companies(resume_text):
    # Normalize the text to make matching easier
    resume_text = resume_text.lower()
    
    # Define regex patterns to match company-related keywords and potential company names
    experience_patterns = [
        r'intern at ([\w\s]+)',       # Matches "Intern at [Company]"
        r'worked at ([\w\s]+)',       # Matches "Worked at [Company]"
        r'([a-z\s]+ltd)',             # Matches "[Company] Ltd"
        r'([a-z\s]+labs)',            # Matches "[Company] Labs"
        r'([a-z\s]+solutions)',       # Matches "[Company] Solutions"
        r'([a-z\s]+inc)',             # Matches "[Company] Inc"
        r'([a-z\s]+pvt ltd)',         # Matches "[Company] Pvt Ltd"
        r'([a-z\s]+corporation)',     # Matches "[Company] Corporation"
        r'([a-z\s]+consulting)',      # Matches "[Company] Consulting"
        r'([a-z\s]+services)'         # Matches "[Company] Services"
    ]
    
    # Combine all patterns into a single pattern
    combined_pattern = re.compile('|'.join(experience_patterns), re.IGNORECASE)
    
    # Find all matches in the resume text
    matches = combined_pattern.findall(resume_text)
    
    # Clean up matches and filter out empty strings
    companies = []
    for match in matches:
        if isinstance(match, tuple):
            # Get the first non-empty group from the tuple
            company = next((m for m in match if m), '').strip()
        else:
            company = match.strip()
        if company:
            companies.append(company)
    
    # Remove duplicates by converting to a set and back to a list
    unique_companies = list(set(companies))
    
    return unique_companies