import csv
import os

def save_to_csv(resume_info_tuple, file_path="./ignore/result.csv"):
    print(resume_info_tuple)
    # Check if the file exists
    file_exists = os.path.isfile(file_path)

    # Define fieldnames for CSV header
    fieldnames = ['name', 'phone', 'email']

    # Write to CSV file
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if the file is empty
        if not file_exists:
            writer.writeheader()

        # Check if the tuple has the expected structure
        if len(resume_info_tuple) == 3:
            # Convert tuple to dictionary
            resume_info = {'name': resume_info_tuple['name'], 'phone': resume_info_tuple['phone'], 'email': resume_info_tuple['email']}
            
            # Write the resume_info to the CSV file
            writer.writerow(resume_info)
        else:
            print("Error: Invalid tuple structure. Expected a tuple with 3 elements (name, phone, email).")
