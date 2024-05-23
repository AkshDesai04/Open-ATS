import re
from nltk.corpus import stopwords

def clean_resume(resume_text):
    # Download stopwords if not already done
    import nltk
    nltk.download('stopwords')
    
    # Define stopwords
    stop_words = set(stopwords.words('english'))

    # Function to remove unwanted characters but preserve common programming language patterns
    def clean_line(line):
        # Allow common programming language characters like +, #, etc.
        line = re.sub(r'[^a-zA-Z0-9@.+#\s-]', ' ', line)
        
        # Normalize whitespace
        line = re.sub(r'\s+', ' ', line).strip()
        
        # Convert to lowercase (optional, comment this line if case needs to be preserved)
        line = line.lower()
        
        # Remove stopwords
        words = line.split()
        words = [word for word in words if word not in stop_words]
        return ' '.join(words)
    
    # Split the resume text into lines
    lines = resume_text.split('\n')
    
    cleaned_lines = [clean_line(line) for line in lines]
    
    # Join the cleaned lines back into a single string with line breaks
    cleaned_resume = '\n'.join(cleaned_lines)
    
    return cleaned_resume