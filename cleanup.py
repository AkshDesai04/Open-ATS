import get_durations
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

def extract_experience(resume_text):
    # Normalize the text to make matching easier
    resume_text = resume_text.lower()
    
    # Extract text starting from 'experience'
    experience_start = re.search(r'experience', resume_text)
    if experience_start:
        resume_text = resume_text[experience_start.start():]
    else:
        return []

    # Define refined regex patterns to match company-related keywords and potential company names
    experience_patterns = [
        r'intern at ([\w\s]+)',      # Matches "Intern at [Company]"
        r'worked at ([\w\s]+)',      # Matches "Worked at [Company]"
        r'([a-z\s]+ ltd)',           # Matches "[Company] Ltd"
        r'([a-z\s]+ labs)',          # Matches "[Company] Labs"
        r'([a-z\s]+ solutions)',     # Matches "[Company] Solutions"
        r'([a-z\s]+ inc)',           # Matches "[Company] Inc"
        r'([a-z\s]+ pvt ltd)',       # Matches "[Company] Pvt Ltd"
        r'([a-z\s]+ corporation)',   # Matches "[Company] Corporation"
        r'([a-z\s]+ consulting)',    # Matches "[Company] Consulting"
        r'([a-z\s]+ services)',      # Matches "[Company] Services"
        r'([a-z\s]+ llp)',           # Matches "[Company] LLP"
        r'([a-z\s]+ group)',         # Matches "[Company] Group"
        r'([a-z\s]+ enterprises)',   # Matches "[Company] Enterprises"
        r'([a-z\s]+ technologies)',  # Matches "[Company] Technologies"
        r'([a-z\s]+ brothers)',      # Matches "[Company] Brothers"
        r'([a-z\s]+ design)',        # Matches "[Company] Design"
        r'([a-z\s]+ cab service)',   # Matches "[Company] Cab Service"
        r'freelancer'                # Matches "freelancer"
    ]
    
    # Combine all patterns into a single pattern
    combined_pattern = re.compile('|'.join(experience_patterns), re.IGNORECASE)
    
    # Define a regex pattern for extracting dates
    date_pattern = re.compile(r'(?P<start_month>[a-zA-Z]+)?\s*(?P<start_year>\d{4})?\s*[-–]\s*(?P<end_month>[a-zA-Z]+)?\s*(?P<end_year>\d{4}|current)', re.IGNORECASE)
    
    # Extract all matches in the resume text for companies
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
    
    # Additional filtering to ensure strings resemble company names
    valid_companies = filter_valid_companies(companies)
    
    # Remove duplicates by converting to a set and back to a list
    unique_companies = list(set(valid_companies))

    # Extract dates associated with each company
    experiences = []
    for company in unique_companies:
        start_date, end_date = extract_dates(resume_text, company)
        
        experiences.append({
            'company': company, 
            'start_date': start_date, 
            'end_date': end_date
        })
    
    return experiences

def filter_valid_companies(companies):
    def is_valid_company(name):
        # Check for common invalid patterns
        invalid_patterns = [
            r'^[a-z]{1,3}$',  # Too short words
            r'\d',            # Contains digits
            r'\n',            # Contains newline
            r'\b(?:at|worked|intern|project|team|member|club|college|university|school|institute|academy|department|faculty|committee|volunteer|association|society|ngo)\b'  # Common non-company words
        ]
        for pattern in invalid_patterns:
            if re.search(pattern, name):
                return False
        return True
    
    return [company for company in companies if is_valid_company(company)]

def extract_dates(resume_text, company):
    # Find the first occurrence of the company name
    company_start = resume_text.find(company.lower())
    if company_start == -1:
        return None, None
    
    # Look for the date pattern around the company name
    before_text = resume_text[max(0, company_start - 100):company_start]
    after_text = resume_text[company_start:company_start + 100]
    
    before_dates = date_pattern.findall(before_text)
    after_dates = date_pattern.findall(after_text)
    
    if before_dates:
        start_date, end_date = before_dates[-1][1], before_dates[-1][3]
    elif after_dates:
        start_date, end_date = after_dates[0][1], after_dates[0][3]
    else:
        start_date, end_date = None, None
    
    return start_date, end_date

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

def divide_resume(resume_text):
    # Extract name from the first line
    name = extract_name(resume_text)
    experience_years = extract_experience_duration(resume_text)
    skills = extract_skills(resume_text)
    highest_qualification = extract_highest_qualification(resume_text)
    work_experience = extract_experience(resume_text)
    career_duration, is_still_working, gap_durations = get_durations.get_durations(resume_text)

    return {
        'name': name,
        'phone': extract_phone(resume_text),
        'email': extract_email(resume_text),
        'experience_years': experience_years,
        'qualification': highest_qualification,
        'skills': skills,
        'work_experience': work_experience,
        'career_duration': career_duration,
        'is_still_working': is_still_working,
        'gap_durations': gap_durations,
        'marital_status': extract_marital_status(resume_text),
        'spoken_languages': extract_speaking_languages(resume_text),
        'certifications': extract_certifications(resume_text),
        'projects': extract_projects(resume_text),
    }

def extract_name(resume_text):
    lines = resume_text.split('\n')
    return lines[0].strip()

def extract_phone(resume_text):
    phone_pattern = re.compile(r'(?:(?:\+?\d{1,3})[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', re.IGNORECASE)
    phone_match = re.search(phone_pattern, resume_text)
    return phone_match.group().strip() if phone_match else ""

def extract_email(resume_text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE)
    email_match = re.search(email_pattern, resume_text)
    return email_match.group().strip() if email_match else ""

def extract_highest_qualification(resume_text):
    qualifications = [r"Ph\.?D\.?", r"M\.?S\.?C\.?\s?[A-Z]*", r"B\.?S\.?C\.?\s?[A-Z]*", r"B\.?A\.?", r"M\.?A\.?", r"Associate Degree", r"High School Diploma"]
    for qualification_pattern in qualifications:
        match = re.search(qualification_pattern, resume_text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None

def extract_experience_duration(resume_text):
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

def extract_marital_status(resume_text):
    # Define patterns to identify marital status
    marital_status_patterns = [
        r'\b(?:married|marital status: married)\b',
        r'\b(?:single|marital status: single)\b',
        r'\b(?:divorced|marital status: divorced)\b'
    ]
    
    # Search for matches
    for pattern in marital_status_patterns:
        if re.search(pattern, resume_text, re.IGNORECASE):
            return True
    
    return False

def extract_speaking_languages(resume_text):
    # Static list of all speaking languages (alphabetically sorted)
    languages = [
        "Afrikaans", "Akan", "Albanian", "Amharic", "Arabic", "Armenian",
        "Assamese", "Azerbaijani", "Basque", "Bashkir", "Bavarian",
        "Belarusian", "Bengali", "Bhojpuri", "Bislama", "Bosnian", "Breton",
        "Bulgarian", "Burmese", "Catalan", "Cebuano", "Chichewa", "Chinese",
        "Chittagonian", "Corsican", "Croatian", "Czech", "Danish", "Dari",
        "Divehi", "Dutch", "Dzongkha", "English", "Esperanto", "Estonian",
        "Faroese", "Fijian", "Filipino", "Finnish", "French", "Fula", "Galician",
        "Georgian", "German", "Greek", "Greenlandic", "Gujarati", "Haitian",
        "Haitian Creole", "Hausa", "Hebrew", "Herero", "Hiligaynon", "Hindi",
        "Hmong", "Hmong Daw", "Hungarian", "Icelandic", "Igbo", "Ilocano",
        "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Jin", "Kannada",
        "Kazakh", "Khmer", "Kinyarwanda", "Konkani", "Korean", "Kurdish",
        "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish",
        "Macedonian", "Magahi", "Maithili", "Malagasy", "Malay", "Malayalam",
        "Maltese", "Mandarin", "Maori", "Marathi", "Mongolian", "Nepali",
        "Norwegian", "Odia", "Oromo", "Pashto", "Persian", "Polish",
        "Portuguese", "Punjabi", "Quechua", "Romanian", "Russian", "Samoan",
        "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovene",
        "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tagalog",
        "Tajik", "Tamil", "Telugu", "Thai", "Tibetan", "Tigrinya", "Tongan",
        "Tswana", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uzbek",
        "Vietnamese", "Welsh", "Wolof", "Xhosa", "Yiddish", "Yoruba", "Zulu"
    ]

    # Compile the regex pattern to match any language in the list
    pattern = re.compile(r'\b(?:' + '|'.join(languages) + r')\b', re.IGNORECASE)

    # Find all matches in the resume string
    matches = pattern.findall(resume_text)

    # Get unique languages and preserve case
    spoken_languages = list(set(matches))

    # Return the spoken languages
    return spoken_languages

def extract_certifications(resume_text):
    # Define patterns to match lines with certifications
    certification_patterns = [
        r'\bcertificate\b',
        r'\bcertification\b',
        r'\bcertified\b',
        r'\bcompleted\b',
        r'\bid\b',
        r'\bnptel\b',
        r'\bcoursera\b',
        r'\bcisco\b',
        r'\bgoogle\b',
        r'\bec[-\s]?council\b'
    ]

    # Combine all patterns into a single regex
    combined_pattern = re.compile('|'.join(certification_patterns), re.IGNORECASE)
    
    # Find all matching lines
    certifications = []
    for line in resume_text.split('\n'):
        if combined_pattern.search(line):
            certifications.append(line.strip())
    
    return certifications