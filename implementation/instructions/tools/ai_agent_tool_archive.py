import argparse
import sys
import os

# Add skills dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../skills")))
from ai_agent_skill_fs_ops import FileSystemSkill

def main():
    parser = argparse.ArgumentParser(description="Agile Archival Tool")
    parser.add_argument("source", help="Source directory to archive")
    parser.add_argument("output", help="Output zip file path")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")

    args = parser.parse_args()

    skill = FileSystemSkill(dry_run=args.dry_run)

    try:
        output_path = skill.archive_directory(args.source, args.output)

        status = "[DRY RUN] Would archive" if args.dry_run else "Archived"
        print(f"{status}: {args.source} -> {output_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
