import argparse
import sys
import json
from pathlib import Path

# Identify skills directory relative to this script
CURRENT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = CURRENT_DIR.parent / "skills"
if str(SKILLS_DIR) not in sys.path:
    sys.path.append(str(SKILLS_DIR))

# AI Agent Skill Imports (Renamed)
from ai_agent_skill_fs_ops import FileSystemSkill
from ai_agent_skill_query_ops import QuerySkill

def main():
    parser = argparse.ArgumentParser(description="[AI AGENT TOOL] AI Agent Result Inspection Tool")
    parser.add_argument("run_id", nargs="?", help="The Run ID to inspect")
    parser.add_argument("--list", action="store_true", help="List all available runs")
    parser.add_argument("--tool", help="Filter by tool (find/grep)")
    parser.add_argument("--limit", type=int, default=10, help="Number of results to show")
    parser.add_argument("--offset", type=int, default=0, help="Starting index for results")
    parser.add_argument("--full", action="store_true", help="Show all results (caution: context usage)")

    args = parser.parse_args()

    fs = FileSystemSkill()
    query_skill = QuerySkill(fs.repo_root)

    print(f"--- AI Agent Tool: Result Viewer ---")

    if args.list or not args.run_id:
        runs = query_skill.list_runs(args.tool)
        if not runs:
            print("No persisted runs found in _temp/ai_agent/.")
            return

        print(f"{'Run ID':<40} | {'Tool':<6} | {'Count':<6} | {'Query'}")
        print("-" * 80)
        for run in runs:
            print(f"{run['run_id']:<40} | {run['tool']:<6} | {run['count']:<6} | {run.get('query',''):<30}")
        return

    try:
        data = query_skill.load_results(args.run_id)
        meta = data["metadata"]
        results = data["results"]

        print(f"Run ID:    {args.run_id}")
        print(f"Tool:      {meta['tool']}")
        print(f"Query:     {meta.get('query')}")
        print(f"Total:     {len(results)}")
        print("-" * 24)

        display_results = results
        if not args.full:
            start = args.offset
            end = args.offset + args.limit
            display_results = results[start:end]
            print(f"Showing results {start+1} to {min(end, len(results))}:")
        else:
            print("Showing ALL results:")

        for i, res in enumerate(display_results, args.offset + 1):
            if isinstance(res, dict):
                # Grep result
                print(f"[{i}] {res['path']}:{res['line_number']}")
                print(f"    {res['content']}")
            else:
                # Find result
                print(f"[{i}] {res}")

        if not args.full and len(results) > (args.offset + args.limit):
            print(f"\n... and {len(results) - (args.offset + args.limit)} more.")
            print(f"SUGGESTION: Use --offset {args.offset + args.limit} to see the next batch, or use search/filter skills on the results file directly.")

        print("-" * 24)
        print("PURPOSE: This tool allows you to peep into large results to conserve YOUR (the LLM's) context.")

    except Exception as e:
        print(f"Error loading run: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
