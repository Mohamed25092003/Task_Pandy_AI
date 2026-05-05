import sys
from types import SimpleNamespace

from cli.rank import run_rank
from cli.explain import run_explain
from cli.demo import run_demo


def input_nonempty(prompt):
    v = input(prompt).strip()
    return v


def menu():
    print("Task interactive launcher")
    print("Commands:")
    print("  1) rank   - Rank candidates for a job")
    print("  2) explain - Explain candidate vs job")
    print("  3) demo   - Run demo for all jobs")
    print("  q) quit")


def handle_rank():
    job_id = input_nonempty("Job id (e.g. j-001): ")
    top_k = input_nonempty("Top k (leave empty for all): ")
    out = input_nonempty("Output path (e.g. outputs/j-001.json): ") or f"outputs/{job_id}.json"
    args = SimpleNamespace(job_id=job_id, top_k=int(top_k) if top_k else None, out=out)
    run_rank(args)


def handle_explain():
    job_id = input_nonempty("Job id (e.g. j-001): ")
    candidate_id = input_nonempty("Candidate id (e.g. c-001): ")
    args = SimpleNamespace(job_id=job_id, candidate_id=candidate_id)
    run_explain(args)


def handle_demo():
    out_dir = input_nonempty("Output directory (e.g. outputs/): ") or "outputs"
    args = SimpleNamespace(out_dir=out_dir)
    run_demo(args)


def main():
    while True:
        menu()
        choice = input_nonempty("Choose command: ")
        if choice in ("q", "quit", "exit"):
            print("Goodbye")
            sys.exit(0)
        if choice in ("1", "rank"):
            handle_rank()
        elif choice in ("2", "explain"):
            handle_explain()
        elif choice in ("3", "demo"):
            handle_demo()
        else:
            print("Unknown choice. Please select 1,2,3 or q.")


if __name__ == "__main__":
    main()
