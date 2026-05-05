from controllers import Preprocessing
from controllers import RankingController

if __name__ == "__main__":
    # Read the JSON files
    with open('./Data/jobs.json', 'r') as f:
        text_jobs = f.read()
    with open('./Data/candidates.json', 'r') as f:
        text_candidates = f.read()

            
    # Create an instance of the Preprocessing class
    preprocessing = Preprocessing()
    
    jobs,candidates= preprocessing.read_json(text_jobs=text_jobs,text_candidates=text_candidates)
    data_extractor = RankingController()
    for job in jobs:
        for candidate in candidates:
            extracted_data = data_extractor.extracting_data(candidate, job)
            score = data_extractor.calculate_score(extracted_data)
            print(f"Candidate: {candidate['id']} - Job: {job['id']} - Score: {score}")
    


  

    # print("Corrected Job Offers:\n", corrected_jobs)
    