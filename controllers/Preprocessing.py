from controllers.BaseController import BaseController
import json

class Preprocessing(BaseController):
    def __init__(self):
        super().__init__()
    def read_json(self,text_candidates=None,text_jobs=None):
        if text_jobs is not None:
            job_offers = json.loads(text_jobs)
        if text_candidates is not None:
            candidates = json.loads(text_candidates)

        return job_offers, candidates

    def Alias_correction(self, text):
        # Define a mapping of common aliases to their corrected forms
        alias_mapping = {
            "JS": "JavaScript",
            "TS": "TypeScript",
            "ReactJS": "React",
            "Node": "Node.js"
        }

        corrected_words = [alias_mapping.get(word, word) for word in text.split()]
       
        corrected_text = ' '.join(corrected_words)
        return corrected_text