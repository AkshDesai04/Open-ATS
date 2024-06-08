import os

import ingest
import cleanup
import result
import score

def main():
    print("Into Main")
    # Uncomment the following lines for user input
    # job_description = input("Enter path to the job description: ")
    # resume_folder = input("Enter path to the resumes folder: ")

    # For testing, use hardcoded paths
    job_description = "./job_description.txt"
    resume_folder = "./resumes/"

    return process_resumes(job_description, resume_folder)

def process_resumes(job_description_path, resume_folder):
    outputs = []
    job_description = ingest.ingest_job_description(job_description_path)
    # print(job_description)
    max_score = score.calculate_max_score(job_description)
    # print("Maximal score: ", max_score)

    with os.scandir(resume_folder) as entries:
        for entry in entries:
            print("Working on : ", entry.name)
            extension = os.path.splitext(entry)[1][1:]
            match extension:
                case "pdf":
                    if entry.is_file():
                        resume_path = os.path.join(resume_folder, entry.name)
                        try:
                            profile = ingest.ingest_profile(resume_path)
                        except Exception as e:
                            print(f"0_Error processing resume '{resume_path}': {e}")
                            print(e)
                            pass

                        try:
                            resume_cleanup = cleanup.clean_resume(profile)
                        except Exception as e:
                            print(f"1_Error processing resume '{resume_path}': {e}")
                            print(e)
                            pass

                        try:
                            resume_divide = cleanup.divide_resume(resume_cleanup)
                        except Exception as e:
                            print(f"2_Error processing resume '{resume_path}': {e}")
                            print(e)
                            pass
                            # print(resume_divide)
                        
                        try:
                            resume_score = score.calculate_score(job_description, resume_divide)
                        except Exception as e:
                            print(f"3_Error processing resume '{resume_path}': {e}")
                            print(e)
                            pass
                            # print("value: ", (resume_score/max_score)*100, "%")
                        try:
                            result.save_to_csv(resume_divide, ((resume_score/max_score)*100))
                        except Exception as e:
                            print(f"4_Error processing resume '{resume_path}': {e}")
                            print(e)
                            pass
                        
                        try:
                            outputs.append((resume_divide, ((resume_score/max_score)*100)))
                        except Exception as e:
                            print(f"5_Error processing resume '{resume_path}': {e}")
                            print(e)
                            pass


                case "png":
                    
                    if entry.is_file():
                        resume_path = os.path.join(resume_folder, entry.name)
                        try:
                            profile = ingest.ingest_profile_png(resume_path)
                            resume_cleanup = cleanup.clean_resume(profile)
                            resume_divide = cleanup.divide_resume(resume_cleanup)
                            # print(resume_divide)
                            resume_score = score.calculate_score(job_description, resume_divide)
                            # print("value: ", (resume_score/max_score)*100, "%")
                            result.save_to_csv(resume_divide, ((resume_score/max_score)*100))
                            outputs.append((resume_divide, ((resume_score/max_score)*100)))

                        except Exception as e:
                            print(f"Error processing resume '{resume_path}': {e}")
                            print(e)
                            pass

    print("outputs")
    print(outputs)
    print("outputs")
    return outputs


if __name__ == "__main__":
    print(main())