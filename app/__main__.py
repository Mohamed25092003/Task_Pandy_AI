# app.py
import argparse
from cli.rank import run_rank
from cli.explain import run_explain
from cli.demo import run_demo

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
        parser.print_help()

if __name__ == "__main__":
    main()