import csv
import os

def save_to_csv(resume_info_tuple, file_path="./ignore/result.csv"):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Define fieldnames for CSV header
    fieldnames = ['name', 'phone', 'email', 'experience', 'qualification', 'skills', 'work experience']

    # Write to CSV file
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if the file is empty
        if not file_exists:
            writer.writeheader()

        # Check if the tuple has the expected structure
        if len(resume_info_tuple) == 7:
            # Convert tuple to dictionary
            try:
                resume_info = {'name': resume_info_tuple['name'],
                            'phone': resume_info_tuple['phone'],
                            'email': resume_info_tuple['email'],
                            'experience': resume_info_tuple['experience_years'],
                            'qualification': resume_info_tuple['qualification'],
                            'skills': resume_info_tuple['skills'],
                            'work experience': resume_info_tuple['work experience']
                            }
            except Exception:
                try:
                    resume_info = {'name': resume_info_tuple['name'],
                                'phone': resume_info_tuple['phone'],
                                'email': resume_info_tuple['email'],
                                'experience': resume_info_tuple['experience_years'],
                                'qualification': resume_info_tuple['qualification'],
                                'skills': "",
                                'work experience': resume_info_tuple['work experience']
                                }
                except Exception:
                    print("Something wrong in writing to csv")
            
            # Write the resume_info to the CSV file
            writer.writerow(resume_info)
        else:
            print("Error: Invalid tuple structure. Expected a tuple with 6 elements (name, phone, email, experience, qualification, skills).")
