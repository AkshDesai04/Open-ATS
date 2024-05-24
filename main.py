import os

import ingest
import cleanup
import data_retrieval
import result

def main():
    # job_description = input("Enter path and name to description")
    # job_description = ingest.ingest_job_description()

    # resume_folder = input("Enter path and name to resumes")
    resume_folder = "./ignore/resumes/testing/"
    process_resumes(resume_folder)

def process_resumes(resume_folder):
    with os.scandir(resume_folder) as entries:
        for entry in entries:
            if entry.is_file():
                print("Processing: " + resume_folder + entry.name)
                profile = ingest.ingest_profile(resume_folder + entry.name)
                resume_cleanup = cleanup.clean_resume(profile)
                resume_divide = cleanup.divide_resume(resume_cleanup)
                result.save_to_csv(resume_divide)
                # print('Hola')
                # # print(resume_divide)
                # print('Hola')

                # print("resume_cleanup" + '**********')
                # print(resume_cleanup)
                # print("resume_divide" + '**********')
                # print(resume_divide)



if __name__ == "__main__":
    main()