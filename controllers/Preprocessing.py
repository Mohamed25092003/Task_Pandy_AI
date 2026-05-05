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

    def Alias_correction(self, skill):
            alias_mapping = {
                "js": "javascript",
                "ts": "typescript",
                "reactjs": "react",
                "node": "node.js",
                "d3": "data visualization",
                "recharts": "data visualization",
            }
            cleaned = skill.strip().lower()
            return alias_mapping.get(cleaned, cleaned)