from controllers import Preprocessing

if __name__ == "__main__":
    # Read the JSON files
    with open('./Data/jobs.json', 'r') as f:
        text_jobs = f.read()
    with open('./Data/candidates.json', 'r') as f:
        text_candidates = f.read()
    count=0
    aliases = ["JS", "TS", "ReactJS", "Node"]
    for job in text_jobs:
        if any(alias in job for alias in aliases):
            count+=1
    print(f"Number of job offers containing aliases: {count}")
    for candidate in text_candidates:
        if any(alias in candidate for alias in aliases):
            count+=1
    print(f"Number of candidates containing aliases: {count}")
            
    # Create an instance of the Preprocessing class
    preprocessing = Preprocessing()
    # Read and process the JSON data
    corrected_candidates = preprocessing.Alias_correction(text_candidates)
    corrected_jobs = preprocessing.Alias_correction(text_jobs)
    for job in corrected_jobs:
        if any(alias in job for alias in aliases):
            count+=1
    print(f"Number of job offers containing aliases after correction: {count}")
    for candidate in corrected_candidates:
        if any(alias in candidate for alias in aliases):
            count+=1
    print(f"Number of candidates containing aliases after correction: {count}")
    # # print("Corrected Candidates:\n", corrected_candidates)
    # print("Corrected Job Offers:\n", corrected_jobs)
    