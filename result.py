import os
import csv

def save_to_csv(resume_info, score, file_path="./ignore/result.csv"):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Define fieldnames for CSV header
    fieldnames = ['name', 'phone', 'email', 'career_duration', 'is_still_working', 'gap_durations', 'qualification', 'skills', 'work_experience', 'marital_status', 'spoken_languages', 'certifications', 'projects', 'state', 'score']

    # Write to CSV file
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if the file is empty
        if not file_exists:
            writer.writeheader()

        # Ensure the resume_info contains all necessary fields
        try:
            skills_str = ', '.join(resume_info['skills']) if resume_info['skills'] else ""
            work_experience_str = '; '.join([f"{exp['company']} ({exp['start_date']} - {exp['end_date']})" for exp in resume_info['work_experience']])

            resume_info_dict = {
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

            writer.writerow(resume_info_dict)
        except Exception as e:
            print(f"Error writing to CSV: {e}")
