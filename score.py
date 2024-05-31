def calculate_max_score(job_description):
    # Extract the values for experience, skills, and tools
    experience_value = job_description['value'][0]['experiance']
    skill_value = job_description['value'][0]['skill']
    tool_value = job_description['value'][0]['tool']
    
    # Calculate the maximum score
    max_experience_score = experience_value
    max_skill_score = len(job_description['skills']) * skill_value
    max_tool_score = len(job_description['tools']) * tool_value
    
    max_score = max_experience_score + max_skill_score + max_tool_score
    return max_score

def calculate_score(job_description, resume):
    score = 0
    
    # Check experience
    experience_needed = job_description['expected_experience']
    candidate_experience = resume['experience_years']
    
    experience_value = job_description['value'][0]['experiance']
    if candidate_experience >= experience_needed:
        score += experience_value
    
    # Check skills
    required_skills = job_description['skills']
    candidate_skills = resume['skills']
    
    skill_value = job_description['value'][0]['skill']
    for skill in required_skills:
        if skill in candidate_skills:
            score += skill_value
    
    # Check tools
    required_tools = job_description['tools']
    candidate_tools = resume['skills']
    
    tool_value = job_description['value'][0]['tool']
    for tool in required_tools:
        if tool in candidate_tools:
            score += tool_value
    return score