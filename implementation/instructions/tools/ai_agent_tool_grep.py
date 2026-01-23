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
    parser = argparse.ArgumentParser(description="[AI AGENT TOOL] AI Agent Content Search Tool (Persistence Focused)")
    parser.add_argument("query", help="Search string or regex")
    parser.add_argument("file_pattern", nargs="?", default="*", help="Glob pattern for candidate files")
    parser.add_argument("--path", help="Directory to search (defaults to repo root)")
    parser.add_argument("--regex", action="store_true", help="Treat query as a regex")
    parser.add_argument("--no-recursive", action="store_false", dest="recursive", help="Search non-recursively")
    parser.set_defaults(recursive=True)

    args = parser.parse_args()

    fs = FileSystemSkill()
    search = SearchSkill(fs)
    query_skill = QuerySkill(fs.repo_root)

    root_path = args.path or str(fs.repo_root)

    print(f"--- AI Agent Tool: Grep ---")
    print(f"Query:        {'Regex' if args.regex else 'String'} '{args.query}'")
    print(f"File Pattern: {args.file_pattern}")
    print(f"Target:       {root_path}")
    print("-" * 24)

    try:
        results = []
        count = 0
        found_in_files = set()

        # Silently search content
        for result in search.grep_content(
            args.query,
            root=root_path,
            file_pattern=args.file_pattern,
            regex=args.regex,
            recursive=args.recursive
        ):
            path = result["path"].resolve()
            found_in_files.add(str(path))

            results.append({
                "path": str(path),
                "line_number": result["line_number"],
                "content": result["content"]
            })
            count += 1

        # Persistence is MANDATORY by default
        metadata = {
            "tool": "ai_agent_tool_grep",
            "timestamp": datetime.now().isoformat(),
            "query": args.query,
            "file_pattern": args.file_pattern,
            "root": root_path,
            "regex": args.regex,
            "count": count,
            "file_count": len(found_in_files)
        }

        run_dir = query_skill.create_run_dir("grep", args.query)
        query_skill.persist_results(run_dir, metadata, results)

        # Output Summary only
        print(f"GREP OPERATION COMPLETE.")
        print(f"Total Matches Found:     {count}")
        print(f"Matches Across Files:    {len(found_in_files)}")
        print(f"Results Persisted To:    {run_dir.resolve()}\\results.json")
        print(f"Run ID:                  {run_dir.name}")
        print("-" * 24)
        print("ACTION REQUIRED: Review the output file listed above or use 'ai_agent' tools (find, filter, diff) to process this data.")
        print("PURPOSE: This tool persists results to disk to conserve YOUR (the LLM's) context and improve operation speed.")

    except Exception as e:
        print(f"Error during grep: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
