from controllers.BaseController import BaseController
import json

class Preprocessing(BaseController):
    def __init__(self):
        super().__init__()
    def read_json(self):
       with open(self.job_offers_path, 'r') as f:
           job_offers = json.load(f)
       with open(self.candidates_path, 'r') as f:
              candidates = json.load(f)
       return job_offers, candidates