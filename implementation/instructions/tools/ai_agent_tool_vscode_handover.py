import argparse
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Identify skills directory relative to this script
CURRENT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = CURRENT_DIR.parent / "skills"
if str(SKILLS_DIR) not in sys.path:
    sys.path.append(str(SKILLS_DIR))

# AI Agent Skill Imports
from ai_agent_skill_fs_ops import FileSystemSkill, HandoverSkill

class VSCodeChatExtractor:
    """Helper to find and extract VS Code chat history from local data."""

    @staticmethod
    def find_chat_json(repo_root: Path) -> Path:
        """Finds the most recent chat session JSON for this workspace."""
        app_data = os.environ.get('APPDATA')
        if not app_data: return None

        storage_root = Path(app_data) / "Code" / "User" / "workspaceStorage"
        if not storage_root.exists(): return None

        target_path_str = str(repo_root.resolve()).lower()

        # Iterate all workspace folders
        for folder in storage_root.iterdir():
            if not folder.is_dir(): continue
            workspace_json = folder / "workspace.json"
            if not workspace_json.exists(): continue

            try:
                # 1. Check if this is the right workspace
                with open(workspace_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    folder_ptr = data.get('folder', '')

                # Normalize URI -> Path
                if folder_ptr.startswith("file:///"):
                    path_str = folder_ptr.replace("file:///", "").replace("%20", " ").replace("/", "\\").replace("%3A", ":")
                else:
                    path_str = folder_ptr

                # Check match
                try:
                    if str(Path(path_str).resolve()).lower() == target_path_str:
                        # Found workspace! Now look for chat
                        chat_dir = folder / "chatSessions"
                        if chat_dir.exists():
                            # Return most recent JSON
                            chats = list(chat_dir.glob("*.json"))
                            if chats:
                                chats.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                                return chats[0]
                except Exception:
                    continue
            except Exception:
                continue
        return None

    @staticmethod
    def export_to_markdown(json_path: Path, output_file: Path, chunk_size: int = 500) -> list:
        """Converts VS Code Chat JSON to Markdown, chunking if necessary."""
        created_files = []
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            requests = data.get('requests', [])
            if not requests:
                return []

            # Pre-calculate blocks to enable chunking
            blocks = []
            for req in requests:
                parts = []
                message = req.get('message', {}).get('text', '')
                parts.append(f"\n\n## User\n{message}")

                # Coalesce all response parts into a single Assistant block
                responses = req.get('response', [])
                full_response_text = ""
                for resp in responses:
                    val = resp.get('value', '')
                    if val:
                        full_response_text += val

                if full_response_text and full_response_text.strip():
                    parts.append(f"\n\n## Assistant\n{full_response_text}")

                parts.append("\n\n---")
                blocks.append("".join(parts))

            total_lines = sum(b.count('\n') for b in blocks)

            if total_lines <= chunk_size:
                # Single file mode
                header = f"# VS Code Chat History (Auto-Extracted)\nSource: {json_path.name}\nDate: {datetime.now()}\n---"
                with open(output_file, 'w', encoding='utf-8') as out:
                    out.write(header + "".join(blocks))
                created_files.append(output_file)
            else:
                # Chunk mode
                current_chunk_idx = 1
                current_lines = 0
                current_blocks = []

                base_stem = output_file.stem

                def flush_chunk(idx, blks):
                    fname = output_file.parent / f"{base_stem}_part{idx:03d}{output_file.suffix}"
                    header = f"# VS Code Chat History (Part {idx})\nSource: {json_path.name}\nDate: {datetime.now()}\n---\n"
                    with open(fname, 'w', encoding='utf-8') as out:
                        out.write(header + "".join(blks))
                    return fname

                for block in blocks:
                    b_lines = block.count('\n')
                    if current_lines + b_lines > chunk_size and current_lines > 0:
                        f = flush_chunk(current_chunk_idx, current_blocks)
                        created_files.append(f)
                        current_chunk_idx += 1
                        current_blocks = []
                        current_lines = 0

                    current_blocks.append(block)
                    current_lines += b_lines

                if current_blocks:
                    f = flush_chunk(current_chunk_idx, current_blocks)
                    created_files.append(f)

            return created_files
        except Exception as e:
            print(f"Failed to export chat: {e}")
            return []

def derive_session_id(source_path: Path, repo_root: Path) -> str:
    """
    Derives a session ID from available context.
    1. Checks for CODE_IMPLEMENTATION_SPEC_*.md in source or docs/implementation/in_progress
    2. Checks for *.md with 'SPEC' in filename
    3. Fallback to directory name
    """
    search_paths = [source_path]
    # If source is near root, also check global spec folder
    if source_path.resolve() == repo_root.resolve():
        search_paths.append(repo_root / "docs" / "implementation" / "in_progress")

    for base in search_paths:
        if not base.exists(): continue
        try:
            # Look for explicit specs with dates
            candidates = list(base.glob("CODE_IMPLEMENTATION_SPEC_*.md"))
            if candidates:
                candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return candidates[0].stem

            # Broader spec search
            candidates = list(base.glob("*SPEC*.md"))
            if candidates:
                 candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                 return candidates[0].stem
        except Exception:
            continue

    return source_path.name

def main():
    parser = argparse.ArgumentParser(description="[AI AGENT TOOL] VS Code Session Handover Tool")
    parser.add_argument("source_path", nargs="?", default=".", help="The folder containing session artifacts")
    parser.add_argument("--name", "--session-id", dest="session_id", help="Custom Name/ID for the session (overrides auto-detection)")
    parser.add_argument("--target-root", help="Override handover destination root")
    parser.add_argument("--no-chat", action="store_true", help="Skip automatic VS Code chat extraction")
    parser.add_argument("--with-files", action="store_true", help="Include file archival (markdown docs, ZIP) in the handover bundle")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--force", action="store_true", help="Bypass safety checks for large directories")

    args = parser.parse_args()

    # 1. Initialize Skills
    skill = FileSystemSkill(dry_run=args.dry_run)
    handover = HandoverSkill(skill)

    # 2. Resolve Dynamic Paths
    repo_root = skill.repo_root

    # Source Path Resolution
    source_path = Path(args.source_path).resolve()

    if not source_path.exists():
        print(f"Error: Source path not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    # Safety Check: Prevent accidental archiving of entire repo or huge folders
    if not args.force:
        risky_dirs = ["node_modules", ".git", ".venv", "venv", "target", "dist"]
        # Check immediate children if scanning root or large folders
        if any((source_path / d).exists() for d in risky_dirs):
            # Only warn if not in a designated 'safe' area like inbox or scratch
            if "_inbox" not in str(source_path) and "temp" not in str(source_path):
                print(f"WARNING: The source directory '{source_path.name}' looks like a project root (contains git/node_modules).")
                print("Archiving this might be huge. Use --force to proceed specific path.")
                # We don't exit here to match user request "source path = .", just warn.
                # Actually, standard behavior is to just warn to stderr but proceed if user insists,
                # but let's be safe: if it's the ROOT, we might only want to pick specific files.
                # For this tool, it bundles everything in source_path.
                pass

    # Handover storage: Default to [WORKSPACE_ROOT]/_ops/handovers/vscode_sessions
    target_root = Path(args.target_root) if args.target_root else repo_root / "_ops" / "handovers" / "vscode_sessions"

    # 3. Define Bundle Naming
    # Format: [YYYYMMDD_HHMMSS]_[SESSION_ID]
    timestamp_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Auto-detection or explicit name
    if args.session_id:
        raw_session_id = args.session_id
    else:
        raw_session_id = derive_session_id(source_path, repo_root)

    # Sanitize session ID
    safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in raw_session_id)

    bundle_name = f"{timestamp_prefix}_{safe_id}"
    bundle_dir = target_root / bundle_name

    print(f"--- AI Agent Tool: VS Code Handover ---")
    print(f"Workspace Root: {repo_root}")
    print(f"Source Context: {source_path}")
    print(f"Target Bundle:  {bundle_dir}")
    if args.dry_run:
        print("[DRY RUN MODE]")

    try:
        # 4. Execute Modular Handover
        if args.with_files:
            results = handover.create_bundle(
                source_brain_path=source_path,
                bundle_dir=bundle_dir,
                zip_name=safe_id
            )

            print(f"\nSuccess! VS Code Session handover staged at:")
            print(f" - Dir:  {results['bundle_dir']}")
            print(f" - Zip:  {results['zip_path'].name}")
            print(f" - Docs: {results['docs_dir'].name}/")
        else:
            print("Mode: Chat Extraction Only (Default)")
            if not args.dry_run:
                bundle_dir.mkdir(parents=True, exist_ok=True)
            results = {
                "bundle_dir": bundle_dir,
                "zip_path": None,
                "docs_dir": None
            }

        # 5. Extract Chat History (if requested)
        if not args.no_chat and not args.dry_run:
            print("\n... Attempting to extract VS Code Chat History ...")
            chat_json = VSCodeChatExtractor.find_chat_json(repo_root)
            if chat_json:
                chat_out = results['bundle_dir'] / "vscode_chat_history.md"
                exported = VSCodeChatExtractor.export_to_markdown(chat_json, chat_out)
                if exported:
                    for f in exported:
                        print(f" - Chat Log: {f.name}")
                    print(f"   (Extracted from {chat_json.name})")
                else:
                    print(" - Chat: Extraction Failed")
            else:
                print(" - Chat: No active chat session found.")

        print("-" * 24)
        print("PURPOSE: This tool archives the current VS Code session context (specs, chat logs, scratches) to ensure context conservation.")
        print("TIP: Point this tool at your '_inbox' or 'docs/in_progress' folder.")

    except Exception as e:
        print(f"Error during handover: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
