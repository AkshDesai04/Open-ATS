import os
import csv

def save_to_csv(resume_info, score, file_path="./resultzzz.csv"):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Define fieldnames for CSV header
    fieldnames = ['serial_number', 'name', 'score', 'phone', 'email', 'career_duration', 'is_still_working', 'gap_durations', 'qualification', 'skills', 'work_experience', 'marital_status', 'spoken_languages', 'certifications', 'projects', 'state']

    # Read existing data from the file
    existing_data = []
    if file_exists:
        with open(file_path, mode='r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                existing_data.append(row)

    # Add new data to the existing data
    skills_str = ', '.join(resume_info['skills']) if resume_info['skills'] else ""
    work_experience_str = '; '.join([f"{exp['company']} ({exp['start_date']} - {exp['end_date']})" for exp in resume_info['work_experience']])

    new_resume_info_dict = {
        'name': resume_info['name'],
        'phone': resume_info['phone'],
        'email': resume_info['email'],
        'career_duration': resume_info['career_duration'],
        'is_still_working': resume_info['is_still_working'],
        'gap_durations': resume_info['gap_durations'],
        'qualification': resume_info['qualification'],
        'skills': skills_str,
        'work_experience': work_experience_str,
        'marital_status': resume_info['marital_status'],
        'spoken_languages': resume_info['spoken_languages'],
        'certifications': resume_info['certifications'],
        'projects': resume_info['projects'],
        'state': resume_info['state'],
        'score': score
    }

    existing_data.append(new_resume_info_dict)

    # Sort data based on the score column
    sorted_data = sorted(existing_data, key=lambda x: float(x['score']), reverse=True)

    # Add serial numbers to each row
    for i, row in enumerate(sorted_data):
        row['serial_number'] = i + 1

    # Write sorted data to the CSV file
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted_data:
            writer.writerow(row)
