import os
import ingest
import cleanup
import result

from get_durations import get_durations

def main():
    # Uncomment the following lines for user input
    # job_description = input("Enter path to the job description: ")
    # resume_folder = input("Enter path to the resumes folder: ")

    # For testing, use hardcoded paths
    job_description = "./ignore/job_description.txt"
    resume_folder = "./resumes/"
    process_resumes(job_description, resume_folder)

def process_resumes(job_description_path, resume_folder):
    with os.scandir(resume_folder) as entries:
        for entry in entries:
            if entry.is_file():
                resume_path = os.path.join(resume_folder, entry.name)
                try:
                    profile = ingest.ingest_profile(resume_path)
                    resume_cleanup = cleanup.clean_resume(profile)
                    work_extracted = cleanup.extract_experience(resume_cleanup)
                    resume_divide = cleanup.divide_resume(resume_cleanup)
                    result.save_to_csv(resume_divide)
                except Exception as e:
                    print(f"Error processing resume '{resume_path}': {e}")

if __name__ == "__main__":
    main()
