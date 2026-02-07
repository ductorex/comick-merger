"""Core logic for merging CBZ files."""

import zipfile
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass


@dataclass
class CBZFile:
    """Represents a CBZ file with its path and contents."""
    path: Path
    entries: List[str]  # List of file paths inside the CBZ

    @classmethod
    def from_path(cls, path: Path) -> 'CBZFile':
        """Create a CBZFile from a path."""
        if not path.exists():
            raise FileNotFoundError(f"CBZ file not found: {path}")

        if not zipfile.is_zipfile(path):
            raise ValueError(f"Not a valid ZIP/CBZ file: {path}")

        with zipfile.ZipFile(path, 'r') as zf:
            # Filter out directories, keep only files
            entries = [name for name in zf.namelist() if not name.endswith('/')]

        return cls(path=path, entries=entries)


class CBZMerger:
    """Handles merging multiple CBZ files into one."""

    def __init__(self, cbz_paths: List[Path]):
        """Initialize with a list of CBZ file paths."""
        self.cbz_files = [CBZFile.from_path(path) for path in cbz_paths]

    def detect_conflicts(self) -> Dict[str, List[int]]:
        """
        Detect file path conflicts between CBZ files.

        Returns:
            Dict mapping conflicting paths to list of CBZ indices that contain them.
        """
        path_to_indices: Dict[str, List[int]] = {}

        for idx, cbz in enumerate(self.cbz_files):
            for entry in cbz.entries:
                if entry not in path_to_indices:
                    path_to_indices[entry] = []
                path_to_indices[entry].append(idx)

        # Keep only paths that appear in multiple CBZ files
        conflicts = {path: indices for path, indices in path_to_indices.items()
                    if len(indices) > 1}

        return conflicts

    def _calculate_prefix_padding(self) -> int:
        """Calculate the number of digits needed for prefixes."""
        num_files = len(self.cbz_files)
        return len(str(num_files - 1))

    def merge(
        self,
        output_path: Path,
        use_prefixes: bool = True
    ) -> None:
        """
        Merge all CBZ files into a single output CBZ.

        Args:
            output_path: Path for the output CBZ file
            use_prefixes: If True, add prefixes (00_, 01_, etc.) to prevent conflicts.
                         If False, add folders (00/, 01/, etc.)
        """
        conflicts = self.detect_conflicts()

        padding = self._calculate_prefix_padding()

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as output_zip:
            for idx, cbz in enumerate(self.cbz_files):
                prefix = str(idx).zfill(padding)

                with zipfile.ZipFile(cbz.path, 'r') as input_zip:
                    for entry in cbz.entries:
                        # Read the file data
                        data = input_zip.read(entry)

                        # Determine the new path
                        if use_prefixes:
                            # Add prefix to filename: 00_image.jpg
                            new_path = f"{prefix}_{entry}"
                        else:
                            # Put in folder: 00/image.jpg
                            new_path = f"{prefix}/{entry}"

                        # Write to output
                        output_zip.writestr(new_path, data)
