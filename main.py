import ingest

def main():
    # profile = input("Enter path and name to resume")
    # job_description = input("Enter path and name to description")
    profile = ingest.ingest_profile()
    job_description = ingest.ingest_job_description()

if __name__ == "__main__":
    main()