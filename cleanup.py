import re
from nltk.corpus import stopwords

def clean_resume(resume_text):
    import nltk
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    def clean_line(line):
        line = re.sub(r'[^a-zA-Z0-9@.+#\s-]', ' ', line)
        line = re.sub(r'\s+', ' ', line).strip()
        line = line.lower()
        
        words = line.split()
        words = [word for word in words if word not in stop_words]
        return ' '.join(words)
    
    lines = resume_text.split('\n')
    cleaned_lines = [clean_line(line) for line in lines]
    cleaned_resume = '\n'.join(cleaned_lines)
    
    return cleaned_resume

def divide_resume(resume_text):
    import nltk
    nltk.download('punkt')
    
    section_patterns = {
        'info': r'(?i)^(name|email|phone|contact|address)\b',
        'education': r'(?i)education',
        'skills': r'(?i)skills?',
        'experience': r'(?i)(experience|employment|work history|professional history|career history)',
        'projects': r'(?i)projects?',
        'certifications': r'(?i)certifications?|achievements|awards',
        'others': r'(?i)others?|additional information|miscellaneous'
    }

    sentences = nltk.sent_tokenize(resume_text)
    sections = {key: [] for key in section_patterns.keys()}
    current_section = 'info'

    for sentence in sentences:
        matched = False
        for section, pattern in section_patterns.items():
            if re.search(pattern, sentence):
                current_section = section
                matched = True
                break
        
        sections[current_section].append(sentence.strip())

    for section in sections:
        sections[section] = ' '.join(sections[section])

    return sections