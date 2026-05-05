import json
from controllers.BaseController import BaseController
from WEIGHTS import Weights
from controllers.Preprocessing import Preprocessing 

class RankingController(BaseController):
    def __init__(self):
        super().__init__()
        self.weights = Weights
        self.preprocessing = Preprocessing()

    def extracting_data(self, candidate, job_offer):
        job_skills=job_offer['requirements']

        ## Extracting JOB data for scoring
        job_must_have_skills = list(set(job_skills.get('mustHaveSkills', [])))
        job_nice_to_have_skills = list(set(job_skills.get('niceToHaveSkills', [])))
        job_min_years_experience = job_skills.get('minYears', 0)
        job_location = job_skills.get('location', '') 

        ## Extracting Candidate data for scoring
        candidate_skills=candidate.get('skills', [])
        candidateexperience_years = candidate.get('yearsOfExperience', 0)
        candidate_feedback_score = candidate.get('score', 0)
        candidate_availability = candidate.get('availability', 0)
        candidate_location = candidate.get('location', '')

        ## obtaining the relationship between the candidate and the job offer
        matched_must_have_skills = self.get_skills(job_must_have_skills, candidate_skills)
        matched_nice_to_have_skills = self.get_skills( job_nice_to_have_skills, candidate_skills)
        matched_must_have_skills_ratio= len(matched_must_have_skills) / len(job_must_have_skills) if len(job_must_have_skills) > 0 else 0
        matched_nice_to_have_skills_ratio= len(matched_nice_to_have_skills) / len(job_nice_to_have_skills) if len(job_nice_to_have_skills) > 0 else 0

        is_location_match = int(job_location == candidate_location)
        is_availability_match = int(candidate_availability.strip().lower() == 'immediate')
        candidate_experience_years_ratio= min(candidateexperience_years / job_min_years_experience, 1) if job_min_years_experience > 0 else 1
        feedback_ratio=candidate_feedback_score/100 if candidate_feedback_score > 0 else 0

        return {
            'matched_must_have_skills_ratio': matched_must_have_skills_ratio,
            'matched_nice_to_have_skills_ratio': matched_nice_to_have_skills_ratio,
            'candidate_experience_years_ratio': candidate_experience_years_ratio,
            'feedback_ratio': feedback_ratio,
            'is_location_match': is_location_match,
            'is_availability_match': is_availability_match
        }


    def get_skills(self, job_skills, candidate_skills):
        job_normalized = {self.preprocessing.Alias_correction(s) for s in job_skills}
        candidate_normalized = {self.preprocessing.Alias_correction(s) for s in candidate_skills}

        matched = job_normalized & candidate_normalized
    

        return list(matched)
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




        
        