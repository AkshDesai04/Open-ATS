import re
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
    # Define regular expressions for extracting information
    phone_pattern = re.compile(r'(?:(?:\+?\d{1,3})[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', re.IGNORECASE)
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE)

    # Extract name from the first line
    lines = resume_text.split('\n')
    name = lines[0].strip()

    # Extract phone and email using regular expressions
    phone_match = re.search(phone_pattern, resume_text)
    phone = phone_match.group().strip() if phone_match else ""
    
    email_match = re.search(email_pattern, resume_text)
    email = email_match.group().strip() if email_match else ""

    # Print extracted information
    # print({'name': name, 'phone': phone, 'email': email})

    # Return extracted information as a dictionary
    return {'name': name, 'phone': phone, 'email': email}