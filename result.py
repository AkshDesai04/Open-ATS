import csv
import os

def save_to_csv(data, filename='./ignore/result.csv'):
    header = ['name', 'location', 'email', 'phone number']
    name = data[0]
    location = data[1]
    email = data[2]
    phone_number = data[3]

    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow([name, location, email, phone_number])