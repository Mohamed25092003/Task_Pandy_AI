from controllers import Preprocessing, RankingController

def run_explain(args):
    with open('./Data/jobs.json') as f:
        text_jobs = f.read()
    with open('./Data/candidates.json') as f:
        text_candidates = f.read()

    preprocessing = Preprocessing()
    jobs, candidates = preprocessing.read_json(text_jobs=text_jobs, text_candidates=text_candidates)

    job = next((j for j in jobs if j['id'] == args.job_id), None)
    candidate = next((c for c in candidates if c['id'] == args.candidate_id), None)

    if not job or not candidate:
        print("Job or candidate not found.")
        return
    controller = RankingController()
    scores_jobs = {}
    extracted = controller.extracting_data(candidate, job)
    ratio = controller.get_ratio(extracted)
    score = controller.calculate_score(ratio)
    scores_jobs.setdefault(job['id'], []).append((candidate['id'], score))
    output = controller.create_output_json(scores_jobs,[extracted])
    print("Raw Output:", output)
    ## no need to get topk here since we are explaining a specific candidate
    output[0].pop("topk")
 

    print(f"\nExplanation: {args.candidate_id} vs {args.job_id}")
    print("Output:", output)