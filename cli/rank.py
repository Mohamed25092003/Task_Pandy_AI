import json
from controllers import Preprocessing, RankingController
import os

def run_rank(args):
    with open('./Data/jobs.json') as f:
        text_jobs = f.read()
    with open('./Data/candidates.json') as f:
        text_candidates = f.read()

    preprocessing = Preprocessing()
    jobs, candidates = preprocessing.read_json(text_candidates=text_candidates, text_jobs=text_jobs)
    print(f"Loaded {len(jobs)} jobs and {len(candidates)} candidates.")
    print("Available job IDs:", [j['id'] for j in jobs])
    print("args.job_id:", args.job_id)

    if args.job_id not in [j['id'] for j in jobs]:
        print(f"Job {args.job_id} not found.")
        return
    else:
        job = next(j for j in jobs if j['id'] == args.job_id)

    controller = RankingController()
    scores_jobs = {}
    all_extracted_data = []

    print(f"Processing job: {job['id']}")
    for candidate in candidates:
            extracted = controller.extracting_data(candidate, job)
            ratio = controller.get_ratio(extracted)
            score = controller.calculate_score(ratio)
            scores_jobs.setdefault(job['id'], []).append((candidate['id'], score))
            all_extracted_data.append(extracted)

    ranked = controller.rank_candidates(scores_jobs)

    # Apply top-k
    for job_id in ranked:
        ranked[job_id] = ranked[job_id][:args.top_k]

    output = controller.create_output_json(ranked, all_extracted_data)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w') as f:
        json.dump(output, f, indent=4)

    print(f"Saved top {args.top_k} candidates for job {args.job_id} → {args.out}")