# **Open-ATS**

##**Introduction**

- Open-ATS is an Open Source resume rating software
- It enables the user to input 2 things:
  1. A Job Description
  2. A set of resumes
    
- It then converts the resume to a string for extracting details from it.
- The following skillsets are fetched from the resumes:
  1. Name
  2. phone
  3. email
  4. Career Duration
  5 Currently Working Status
  6. Gaps in resume
  7. Highest Qualification
  8. Skills
  9. Work Experience
  10. Marital Status
  11. Spoken Languages
  12. Certifications
  13. Projects
  14. Location (State)
  15. Score of Resume (As matched with Job Description)

**Installation Steps:**
  1. Install the dependencies: run `pip install -r requirements.txt` to install add python package dependencies needed by the project

**Steps to Start**
1. In the same folder as the project, create a folder names `resume`
2. Paste all resumes to be tested in this folder
3. Create a file named `job_description.txt`
4. Paste the job description in the file while following the format of the file
5. run [main.py](https://github.com/AkshDesai04/Open-ATS/blob/main/main.py) without any arguments.
6. A file names `result.csv` will be created if not already present. If already present, it will be appended with the new data.
7. The data from the resumes will be appended to the result file as the resumes get processed.