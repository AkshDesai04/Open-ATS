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

# Example usage:
data = {
    'info': 'aksh desai\nlocation valsad gujarat india\nlinkedin github leetcode\nemail aksh.d.4002@gmail.com\nmobile +91 635-396-8666\nprofile\nthird-year information technology student cspit charotar university science technology. proficient java python c c++\nsource management tools like git github. currently part graphics media team cp squad student club\ncollege.',
    'education': 'education\ncspit - charotar university science technology\nchanga gujarat india\nbachelor technology information technology aug 2023 present\ngujarat technological university\n\nsurat gujarat india\ndiploma information technology 2020 - 2023\natul vidyalaya\nvalsad gujarat india\nsecondary school 2007 -\n2020\n\nprojects\ncommunity\n\nflutter application development\ncreated intra society communication management service internship leading team 5 members. provided platform communication society payment maintenance raising issues much more.',
    'skills': 'technical skills\n\nlanguages\n\njava python dart c c++\ndatabases\n\noracle mysql firebase\ntools\n\ngit github docker\nnon-coding skills\n\nphotoshop effects premiere pro excel blender\n\nexperience\nintern may 2024 jun 2024\natul ltd\natul gujarat india\nworked various projects across multiple domains python ai ml python automation database web etc. researched open-source ml models created pipeline automating specified systems. assisted system design database schema designing assisting normalizing schema. automated created ats-like system using python.',
    'experience': '',
    'projects': 'passionate technology developed deployed multiple open-source projects various domains. worked using tools adobe photoshop adobe illustrator canva\nintern\nfeb 2023 jul 2023\nsapient codelabs\n\nsurat gujarat india\ncontinued previous project previous internship worked leading team. completed represented project company college. intern\njul 2022 feb 2023\ntechnomads solutions pvt ltd\nsurat gujarat india\nlead team 5 inters creating mobile application using flutter firebase\nspoc college company representing team. github repository https github.com our-community-tdec our-community\n\nproject watchdog\n\npython cyber security digital forensics\ncreated desktop privacy security monitoring service using python\nusers get notified blocked people states occurring devices device gets locked shut down. github repository https github.com our-community-tdec our-community\n\npycompare\n\n\n\npython image\nefficiently scale across many cores cpu gpu cuda chosen. compare terabyte photos effectively utilizing 16gb system memory cases. modular powerful allowing user control attribute system.',
    'certifications': 'github repository https github.com akshdesai04 pycompare\npublications\ndesktop security swiss-cheese approach\n\nwrite domain\nwrite\nlink add link paper published\ndocker docker performance penalties\n\nwrite domain\nwrite\nlink add link paper published\nlockbit case study\n\nwrite domain\nwrite\nlink add link paper published\npenalties logging\n\nwrite domain\nwrite\nlink add link paper published\ninter-browser rendering performance differences\n\nwrite domain\nwrite\nlink add link paper published\nredesigning system architecture improve security critical high-value places\nwrite domain\nwrite\nlink add link paper published\n\ncertifications\n\ncommunity\n\nflutter application development\ncreated intra society communication management service internship leading team 5 members. provided platform communication society payment maintenance raising issues much more. github repository https github.com our-community-tdec our-community\nvolunteering\n\nwebsite making deployment\nnov 2022 feb 2023\nhabitat humanity\nvalsad gujarat india\ndesigned developed deployed website pro bono local ngo. implemented updates enhancements based organization evolving needs.',
    'others': 'graphics media team\nmar 2024 current\ncp squad charusat\nchanga gujarat india\nanother team member worked graphics media team cp squad student club.'
}

name, location, email, phone_number = personal_information(data)
print(f'name = {name}')
print(f'location = {location}')
print(f'email = {email}')
print(f'phone number = {phone_number}')
