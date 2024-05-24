def personal_information(resume):
    # Extract the 'info' string from the dictionary
    info_str = resume.get('info', '')
    
    # Split the input string into lines
    lines = info_str.split('\n')
    
    # Initialize variables to store the extracted values
    name = ''
    location = ''
    email = ''
    phone_number = ''

    # Iterate through the lines to find the required information
    for line in lines:
        if ' ' in line:
            # Find the name (first line)
            if not name:
                name = line
            # Find the location (line starts with 'location')
            elif line.startswith('location'):
                location = line.replace('location ', '', 1)
            # Find the email (line starts with 'email')
            elif line.startswith('email'):
                email = line.replace('email ', '', 1)
            # Find the phone number (line starts with 'mobile')
            elif line.startswith('mobile'):
                phone_number = line.replace('mobile ', '', 1)

    return name, location, email, phone_number