import json, os
from controllers import Preprocessing, RankingController

def run_demo(args):
    with open('./Data/jobs.json') as f:
        text_jobs = f.read()
    with open('./Data/candidates.json') as f:
        text_candidates = f.read()

    preprocessing = Preprocessing()
    jobs, candidates = preprocessing.read_json(text_jobs=text_jobs, text_candidates=text_candidates)
    controller = RankingController()

    scores_jobs = {}
    all_extracted_data = []

    for job in jobs:
        for candidate in candidates:
            extracted = controller.extracting_data(candidate, job)
            ratio = controller.get_ratio(extracted)
            score = controller.calculate_score(ratio)
            scores_jobs.setdefault(job['id'], []).append((candidate['id'], score))
            all_extracted_data.append(extracted)

    ranked = controller.rank_candidates(scores_jobs)
    output = controller.create_output_json(ranked, all_extracted_data)

    os.makedirs(args.out_dir, exist_ok=True)
    json.dump(output, open(os.path.join(args.out_dir, 'demo_output.json'), 'w'), indent=4)
    print(f"Demo output saved to {os.path.join(args.out_dir, 'demo_output.json')}")
   