import argparse
import sys
from pathlib import Path
from datetime import datetime

# Identify skills directory relative to this script
CURRENT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = CURRENT_DIR.parent / "skills"
if str(SKILLS_DIR) not in sys.path:
    sys.path.append(str(SKILLS_DIR))

# AI Agent Skill Imports (Renamed)
from ai_agent_skill_fs_ops import FileSystemSkill
from ai_agent_skill_search_ops import SearchSkill
from ai_agent_skill_query_ops import QuerySkill

def main():
    parser = argparse.ArgumentParser(description="[AI AGENT TOOL] AI Agent File Discovery Tool (Persistence Focused)")
    parser.add_argument("pattern", help="Search pattern (glob or regex)")
    parser.add_argument("--path", help="Directory to search (defaults to repo root)")
    parser.add_argument("--regex", action="store_true", help="Use regex pattern matching")
    parser.add_argument("--no-recursive", action="store_false", dest="recursive", help="Search non-recursively")
    parser.set_defaults(recursive=True)

    args = parser.parse_args()

    fs = FileSystemSkill()
    search = SearchSkill(fs)
    query_skill = QuerySkill(fs.repo_root)

    root_path = args.path or str(fs.repo_root)

    print(f"--- AI Agent Tool: Find ---")
    print(f"Query:        {'Regex' if args.regex else 'Glob'} '{args.pattern}'")
    print(f"Target:       {root_path}")
    print("-" * 24)

    try:
        results = []
        count = 0
        # Silently find files
        for item in search.find_files(
            args.pattern,
            root=root_path,
            regex=args.regex,
            recursive=args.recursive
        ):
            results.append(str(item.resolve()))
            count += 1

        # Persistence is MANDATORY by default
        metadata = {
            "tool": "ai_agent_tool_find",
            "timestamp": datetime.now().isoformat(),
            "query": args.pattern,
            "root": root_path,
            "regex": args.regex,
            "count": count
        }

        run_dir = query_skill.create_run_dir("find", args.pattern)
        query_skill.persist_results(run_dir, metadata, results)

        # Output Summary only
        print(f"FIND OPERATION COMPLETE.")
        print(f"Total Matches Found: {count}")
        print(f"Results Persisted To: {run_dir.resolve()}\\results.json")
        print(f"Run ID:              {run_dir.name}")
        print("-" * 24)
        print("ACTION REQUIRED: Review the output file listed above or use 'ai_agent' tools (find, filter, diff) to process this data.")
        print("PURPOSE: This tool persists results to disk to conserve YOUR (the LLM's) context and improve operation speed.")

    except Exception as e:
        print(f"Error during find: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
