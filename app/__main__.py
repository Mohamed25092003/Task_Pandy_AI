import argparse
from types import SimpleNamespace

from cli.rank import run_rank
from cli.explain import run_explain
from cli.demo import run_demo


def interactive_menu():
    print("Task interactive launcher")
    print("Commands:")
    print("  1) rank   - Rank candidates for a job")
    print("  2) explain - Explain candidate vs job")
    print("  3) demo   - Run demo for all jobs")
    print("  q) quit")

    while True:
        choice = input("Choose command: ").strip()
        if choice in ("q", "quit", "exit"):
            print("Goodbye")
            return
        if choice in ("1", "rank"):
            job_id = input("Job id (e.g. j-001): ").strip()
            top_k_raw = input("Top k (default 10): ").strip()
            out = input("Output path (e.g. outputs/j-001.json): ").strip()
            top_k = int(top_k_raw) if top_k_raw else 10
            out = out or f"outputs/{job_id}.json"
            args = SimpleNamespace(job_id=job_id, top_k=top_k, out=out)
            run_rank(args)
        elif choice in ("2", "explain"):
            job_id = input("Job id (e.g. j-001): ").strip()
            candidate_id = input("Candidate id (e.g. c-001): ").strip()
            args = SimpleNamespace(job_id=job_id, candidate_id=candidate_id)
            run_explain(args)
        elif choice in ("3", "demo"):
            out_dir = input("Output directory (e.g. outputs/): ").strip() or "outputs"
            args = SimpleNamespace(out_dir=out_dir)
            run_demo(args)
        else:
            print("Unknown choice. Please select 1,2,3 or q.")

def main():
    parser = argparse.ArgumentParser(
        prog="app",
        description="Candidate Ranking CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- rank subcommand ---
    rank_parser = subparsers.add_parser("rank", help="Rank candidates for a job")
    rank_parser.add_argument("--job-id", required=True, help="Job ID (e.g. j-001)")
    rank_parser.add_argument("--top-k", type=int, default=10, help="Number of top candidates")
    rank_parser.add_argument("--out", required=True, help="Output JSON file path")

    # --- explain subcommand ---
    explain_parser = subparsers.add_parser("explain", help="Explain a candidate vs a job")
    explain_parser.add_argument("--job-id", required=True)
    explain_parser.add_argument("--candidate-id", required=True)

    # --- demo subcommand ---
    demo_parser = subparsers.add_parser("demo", help="Run demo for all jobs")
    demo_parser.add_argument("--out-dir", required=True, help="Output directory")

    args = parser.parse_args()

    if args.command == "rank":
        run_rank(args)
    elif args.command == "explain":
        run_explain(args)
    elif args.command == "demo":
        run_demo(args)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
