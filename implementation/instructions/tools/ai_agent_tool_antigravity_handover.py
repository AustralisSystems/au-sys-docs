import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# Identify skills directory relative to this script
CURRENT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = CURRENT_DIR.parent / "skills"
if str(SKILLS_DIR) not in sys.path:
    sys.path.append(str(SKILLS_DIR))

# AI Agent Skill Imports (Renamed)
from ai_agent_skill_fs_ops import FileSystemSkill, HandoverSkill

def main():
    parser = argparse.ArgumentParser(description="[AI AGENT TOOL] Session Handover Tool")
    parser.add_argument("source_id", help="The brain ID to archive")
    parser.add_argument("bundle_id", nargs="?", help="ID for the bundle folder (defaults to source_id)")
    parser.add_argument("--brain-root", help="Override brain storage root")
    parser.add_argument("--target-root", help="Override handover destination root")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")

    args = parser.parse_args()

    # 1. Initialize Skills
    skill = FileSystemSkill(dry_run=args.dry_run)
    handover = HandoverSkill(skill)

    # 2. Resolve Dynamic Paths
    repo_root = skill.repo_root

    # Brain storage: Default to ~/.gemini/antigravity/brain
    brain_root = Path(args.brain_root) if args.brain_root else Path(os.path.expanduser("~")) / ".gemini" / "antigravity" / "brain"

    # Handover storage: Default to [WORKSPACE_ROOT]/_ops/handovers/antigravity_brains
    target_root = Path(args.target_root) if args.target_root else repo_root / "_ops" / "handovers" / "antigravity_brains"

    source_path = brain_root / args.source_id

    if not source_path.exists():
        print(f"Error: Source brain path not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    # 3. Define Bundle Naming
    # Format: [YYYYMMDD_HHMMSS]_[BRAIN_ID]
    timestamp_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_name = f"{timestamp_prefix}_{args.source_id}"
    bundle_dir = target_root / bundle_name

    print(f"--- AI Agent Tool: Handover ---")
    print(f"Workspace Root: {repo_root}")
    print(f"Source Brain:   {source_path}")
    print(f"Target Bundle:  {bundle_dir}")
    if args.dry_run:
        print("[DRY RUN MODE]")

    try:
        # 4. Execute Modular Handover
        results = handover.create_bundle(
            source_brain_path=source_path,
            bundle_dir=bundle_dir,
            zip_name=args.source_id
        )

        print(f"\nSuccess! Handover bundle staged at:")
        print(f" - Dir:  {results['bundle_dir']}")
        print(f" - Zip:  {results['zip_path'].name}")
        print(f" - Docs: {results['docs_dir'].name}/")

        print("-" * 24)
        print("PURPOSE: This tool archives the current session state to ensure context conservation for future sessions.")

    except Exception as e:
        print(f"Error during handover: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
