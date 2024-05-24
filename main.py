import ingest
import cleanup
import data_retrieval
import result

def main():
    # profile = input("Enter path and name to resume")
    # job_description = input("Enter path and name to description")
    profile = ingest.ingest_profile("./ignore/Aksh.pdf")
    # job_description = ingest.ingest_job_description()

    for i in range(10):
        resume_cleanup = cleanup.clean_resume(profile)
        resume_divide = cleanup.divide_resume(resume_cleanup)
        result.save_to_csv(data_retrieval.personal_information(resume_divide))

if __name__ == "__main__":
    main()