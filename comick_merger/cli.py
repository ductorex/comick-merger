"""Command-line interface for comick-merger."""

import sys
import argparse
from pathlib import Path
from typing import List

from .cbz_merger import CBZMerger


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Merge multiple CBZ (Comic Book Zip) files into one",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge with prefixes (default)
  comick-cli chapter1.cbz chapter2.cbz chapter3.cbz -o complete.cbz

  # Merge using folders instead of prefixes
  comick-cli *.cbz -o complete.cbz --folders

  # Check for conflicts without merging
  comick-cli *.cbz --check-only
        """
    )

    parser.add_argument(
        'cbz_files',
        nargs='+',
        type=Path,
        help="CBZ files to merge (in order)"
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('merged.cbz'),
        help="Output CBZ file path (default: merged.cbz)"
    )

    parser.add_argument(
        '--folders',
        action='store_true',
        help="Use folders (00/, 01/) instead of prefixes (00_, 01_)"
    )

    parser.add_argument(
        '--check-only',
        action='store_true',
        help="Only check for conflicts, don't merge"
    )

    args = parser.parse_args()

    # Validate input files
    cbz_files: List[Path] = []
    for path in args.cbz_files:
        if not path.exists():
            print(f"Error: File not found: {path}", file=sys.stderr)
            return 1
        cbz_files.append(path)

    if len(cbz_files) < 2:
        print("Error: Need at least 2 CBZ files to merge", file=sys.stderr)
        return 1

    try:
        print(f"Loading {len(cbz_files)} CBZ files...")
        merger = CBZMerger(cbz_files)

        # Check for conflicts
        conflicts = merger.detect_conflicts()

        if conflicts:
            print(f"\n[WARNING] Found {len(conflicts)} file path conflicts:")
            for path, indices in list(conflicts.items())[:10]:
                cbz_names = [cbz_files[i].name for i in indices]
                print(f"  - {path}")
                print(f"    Found in: {', '.join(cbz_names)}")

            if len(conflicts) > 10:
                print(f"  ... and {len(conflicts) - 10} more conflicts\n")
        else:
            print("[OK] No conflicts detected\n")

        if args.check_only:
            return 0

        # Perform merge
        use_prefixes = not args.folders
        print(f"Merging using {'prefixes' if use_prefixes else 'folders'}...")

        merger.merge(
            output_path=args.output,
            use_prefixes=use_prefixes
        )

        print(f"\n[OK] Success! Merged CBZ saved to: {args.output}")
        return 0

    except Exception as e:
        print(f"\n[ERROR] Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
