import os

import ingest
import cleanup
import result
import score

def main():
    # Uncomment the following lines for user input
    # job_description = input("Enter path to the job description: ")
    # resume_folder = input("Enter path to the resumes folder: ")

    # For testing, use hardcoded paths
    job_description = "./ignore/job_description.txt"
    resume_folder = "./ignore/resumes/testing/"
    process_resumes(job_description, resume_folder)

def process_resumes(job_description_path, resume_folder):
    job_description = ingest.ingest_job_description(job_description_path)
    print(job_description)
    max_score = score.calculate_max_score(job_description)
    print("Maximal score: ", max_score)

    with os.scandir(resume_folder) as entries:
        for entry in entries:
            if entry.is_file():
                resume_path = os.path.join(resume_folder, entry.name)
                try:
                    profile = ingest.ingest_profile(resume_path)
                    resume_cleanup = cleanup.clean_resume(profile)
                    resume_divide = cleanup.divide_resume(resume_cleanup)
                    print(resume_divide)
                    resume_score = score.calculate_score(job_description, resume_divide)
                    print("value: ", (resume_score/max_score)*100, "%")
                    result.save_to_csv(resume_divide, ((resume_score/max_score)*100))

                except Exception as e:
                    print(f"Error processing resume '{resume_path}': {e}")
                    print(e)
                    pass

if __name__ == "__main__":
    main()
