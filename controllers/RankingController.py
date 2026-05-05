import json
from controllers.BaseController import BaseController
from WEIGHTS import Weights
from controllers.Preprocessing import Preprocessing 
from datetime import datetime

class RankingController(BaseController):
    def __init__(self):
        super().__init__()
        self.weights = Weights
        self.preprocessing = Preprocessing()

    def extracting_data(self, candidate, job_offer):
        job_skills=job_offer['requirements']
        job_id=job_offer["id"]

        ## Extracting JOB data for scoring
        job_must_have_skills = list(set(job_skills.get('mustHaveSkills', [])))
        job_nice_to_have_skills = list(set(job_skills.get('niceToHaveSkills', [])))
        job_min_years_experience = job_skills.get('minYears', 0)
        job_location = job_skills.get('location', '') 

        ## Extracting Candidate data for scoring
        candidate_skills=candidate.get('skills', [])
        candidate_experience_years = candidate.get('yearsOfExperience', 0)
        candidate_feedback_score = candidate.get('score', 0)
        candidate_availability = candidate.get('availability', 0)
        candidate_location = candidate.get('location', '')
        candidate_id=candidate.get('id', '')

        ## obtaining the relationship between the candidate and the job offer
        matched_must_have_skills = self.get_skills(job_must_have_skills, candidate_skills)
        matched_nice_to_have_skills = self.get_skills( job_nice_to_have_skills, candidate_skills)


        missing_must_have_skills = self.get_missing_skills(job_must_have_skills, candidate_skills)
        missing_nice_to_have_skills = self.get_missing_skills(job_nice_to_have_skills, candidate_skills)
    

        return {
            'job_id': job_id,
            'candidate_id': candidate_id,
            'matched_must_have_skills': matched_must_have_skills,
            'matched_nice_to_have_skills': matched_nice_to_have_skills,
            "job_must_have_skills": job_must_have_skills,
            "job_nice_to_have_skills": job_nice_to_have_skills,
            'candidate_experience_years': candidate_experience_years,
            'feedback_score': candidate_feedback_score,
            'missing_must_have_skills': missing_must_have_skills,
            'missing_nice_to_have_skills': missing_nice_to_have_skills,
            "job_location": job_location,
            "candidate_location": candidate_location,
            "candidate_availability": candidate_availability,
            "job_min_years_experience": job_min_years_experience,
            

        }


    def get_skills(self, job_skills, candidate_skills):
        job_normalized = {self.preprocessing.Alias_correction(s) for s in job_skills}
        candidate_normalized = {self.preprocessing.Alias_correction(s) for s in candidate_skills}

        matched = job_normalized & candidate_normalized
    

        return list(matched)
    def get_ratio(self, extracted_data):
        is_location_match = int(extracted_data['job_location'] == extracted_data['candidate_location'])
        is_availability_match = int(extracted_data['candidate_availability'].strip().lower() == 'immediate')
        candidate_experience_years_ratio= min(extracted_data['candidate_experience_years'] / extracted_data['job_min_years_experience'], 1) if extracted_data['job_min_years_experience'] > 0 else 1
        feedback_ratio=extracted_data['feedback_score']/100 if extracted_data['feedback_score'] > 0 else 0
        matched_must_have_skills_ratio= len(extracted_data['matched_must_have_skills']) / len(extracted_data['job_must_have_skills']) if len(extracted_data['job_must_have_skills']) > 0 else 0
        matched_nice_to_have_skills_ratio= len(extracted_data['matched_nice_to_have_skills']) / len(extracted_data['job_nice_to_have_skills']) if len(extracted_data['job_nice_to_have_skills']   ) > 0 else 0
        return {
            'is_location_match': is_location_match,
            'is_availability_match': is_availability_match,
            'candidate_experience_years_ratio': candidate_experience_years_ratio,
            'feedback_ratio': feedback_ratio,
            'matched_must_have_skills_ratio': matched_must_have_skills_ratio,
            'matched_nice_to_have_skills_ratio': matched_nice_to_have_skills_ratio
        }
    def calculate_score(self, extracted_data):
        score = 0
        # Calculate must-have skills score with penalty if not fully matched
        must_have_ratio = extracted_data['matched_must_have_skills_ratio']
        if must_have_ratio < 1.0:
            score += self.weights.MUST_HAVE.value * must_have_ratio * self.weights.MUST_HAVE_PENALTY.value
        else:
            score += self.weights.MUST_HAVE.value

        # Calculate experience score with penalty if below required years
        exp_ratio = min(extracted_data['candidate_experience_years_ratio'], 1.0)
        if exp_ratio < 1.0:
            score += self.weights.EXPERIENCE.value * exp_ratio * self.weights.EXPERIENCE_PENALTY.value
        else:
            score += self.weights.EXPERIENCE.value

        # rest of the score components
        score += self.weights.NICE_TO_HAVE.value * extracted_data['matched_nice_to_have_skills_ratio']
        score += self.weights.LOCATION.value * extracted_data['is_location_match']
        score += self.weights.FEEDBACK.value * extracted_data['feedback_ratio']
        score += self.weights.AVAILABILITY.value * int(extracted_data['is_availability_match'])

        return min(round(score, 4), 1.0)
    def rank_candidates(self, scores_jobs):
        sorted_scores_jobs = {}

        for job_id, candidates_list in scores_jobs.items():
            sorted_list = sorted(candidates_list, key=lambda x: x[1], reverse=True)
            sorted_scores_jobs[job_id] = sorted_list

        return sorted_scores_jobs
    def get_missing_skills(self, job_skills, candidate_skills):
        job_normalized = {self.preprocessing.Alias_correction(s) for s in job_skills}
        candidate_normalized = {self.preprocessing.Alias_correction(s) for s in candidate_skills}

        missing = job_normalized - candidate_normalized

        return list(missing)
    
    def generate_feedback(self, extracted_data):
        summary = ""
        ratios=self.get_ratio(extracted_data)
        if ratios['matched_must_have_skills_ratio'] < 1.0:
            summary += f"Missing must-have skills: {', '.join(extracted_data['missing_must_have_skills'])}\n"
        else:
            summary += f"All must-have skills matched which is {extracted_data['matched_must_have_skills']}\n"

        if ratios['matched_nice_to_have_skills_ratio'] < 1.0:
            summary += f"Missing nice-to-have skills: {', '.join(extracted_data['missing_nice_to_have_skills'])}\n" 
        else:
            summary += f"All nice-to-have skills matched which is {extracted_data['matched_nice_to_have_skills']}\n"
        if ratios['candidate_experience_years_ratio'] < 1.0:
            summary += "Candidate has less experience than required.\n"
        else:
            summary += "Candidate meets or exceeds the experience requirement.\n"
        return summary  
    def create_output_json(self, ranked_candidates, all_extracted_data, top_k=None):
        output = []
        
        for job_id, candidates in ranked_candidates.items():
            for i,(candidate_id, score) in enumerate(candidates):
                extracted_data = next((data for data in all_extracted_data if data['job_id'] == job_id and data['candidate_id'] == candidate_id), None)
                if extracted_data:
                    if top_k is not None and i >= top_k:
                        break
                    summary = self.generate_feedback(extracted_data)
                    reason= self.create_schema_of_reasons(extracted_data)
                    meta_data = {
                            "approach": "baseline-v1", # Or "hybrid-embedding-v1" if using Option B
                            "generatedAt": datetime.utcnow().isoformat() + "Z"
                        }
                    results = {
                        "candidate_id": candidate_id,
                        "score": score,
                        "matched_skills":list(set(extracted_data['matched_must_have_skills']) | set(extracted_data['matched_nice_to_have_skills'])),
                        "missing_must_have_skills": extracted_data['missing_must_have_skills'],
                        "missing_nice_to_have_skills": extracted_data['missing_nice_to_have_skills'],
                        "reasons": reason,
                        "summary": summary
                        
                    }
                    output.append({
                        "job_id": job_id,
                        "topk": i + 1,
                        "results": results,
                        "meta": meta_data
                    })
        return output
    def create_schema_of_reasons(self, extracted_data):
        all_reasons={}
        ratios=self.get_ratio(extracted_data)
        if ratios["is_location_match"] == 0:
            all_reasons["location"] = "Candidate location does not match job location."
        else:
            all_reasons["location"] = "Candidate location matches job location."
        if ratios["is_availability_match"] == 0:
            all_reasons["availability"] = "Candidate is not immediately available."
        else:
            all_reasons["availability"] = "Candidate is immediately available."
        if ratios["candidate_experience_years_ratio"] < 1.0:
            all_reasons["experience_years"] = f"{extracted_data['candidate_experience_years']} < {extracted_data['job_min_years_experience']}"
        else:
            all_reasons["experience_years"] = f"{extracted_data['candidate_experience_years']} >= {extracted_data['job_min_years_experience']}"
        all_reasons["must_have_skills"] = extracted_data['matched_must_have_skills']
 
        all_reasons["nice_to_have_skills"] = extracted_data['matched_nice_to_have_skills']

     
        all_reasons["feedback"] = f"{extracted_data['feedback_score']}%"
        return all_reasons

        
        