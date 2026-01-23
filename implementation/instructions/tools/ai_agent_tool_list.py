import argparse
import sys
import os
import json
from datetime import datetime

# Add skills dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../skills")))
from fs_ops import FileSystemSkill

def main():
    parser = argparse.ArgumentParser(description="Agile File Listing Tool")
    parser.add_argument("root", help="Root directory to search")
    parser.add_argument("--pattern", default="*", help="Glob pattern")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recursive search")
    parser.add_argument("--dirs", action="store_true", help="Include directories")
    parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")
    parser.add_argument("--mode", choices=['eq', 'gt', 'lt'], default='eq', help="Date filter mode")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    skill = FileSystemSkill()

    try:
        files = skill.list_files(
            args.root,
            pattern=args.pattern,
            recursive=args.recursive,
            include_dirs=args.dirs
        )

        if args.date:
            filter_date = datetime.strptime(args.date, "%Y-%m-%d")
            files = skill.filter_by_date(files, filter_date, args.mode)

        results = []
        for f in files:
            stat = f.stat()
            info = {
                "path": str(f),
                "name": f.name,
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
            results.append(info)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results:
                print(f"{r['path']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
