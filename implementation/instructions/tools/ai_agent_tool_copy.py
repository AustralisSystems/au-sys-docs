import argparse
import sys
import os
from datetime import datetime

# Add skills dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../skills")))
from fs_ops import FileSystemSkill

def main():
    parser = argparse.ArgumentParser(description="Agile Copy/Extraction Tool")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("dest", help="Destination directory")
    parser.add_argument("--pattern", default="*", help="Glob pattern")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recursive copy")
    parser.add_argument("--flatten", "-f", action="store_true", help="Flatten directory structure")
    parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")
    parser.add_argument("--mode", choices=['eq', 'gt', 'lt'], default='eq', help="Date filter mode")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")

    args = parser.parse_args()

    skill = FileSystemSkill(dry_run=args.dry_run)

    date_filter = None
    if args.date:
        try:
            date_filter = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)

    try:
        ops = skill.copy_files(
            args.source,
            args.dest,
            pattern=args.pattern,
            recursive=args.recursive,
            flatten=args.flatten,
            date_filter=date_filter,
            date_mode=args.mode
        )

        for src, dst in ops:
            status = "[DRY RUN] Would copy" if args.dry_run else "Copied"
            print(f"{status}: {src} -> {dst}")

        print(f"Total operations: {len(ops)}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
