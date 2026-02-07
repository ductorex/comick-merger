"""
Script to generate test CBZ files once.
Run this script to create all test data before running tests.

Usage:
    python tests/setup_test_data.py
"""

import zipfile
from pathlib import Path


def create_cbz(path: Path, files: list[str], content_prefix: str = "Content") -> Path:
    """Create a CBZ file with specified files."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(path, 'w') as zf:
        for filename in files:
            content = f"{content_prefix} of {filename}"
            zf.writestr(filename, content)
    return path


def setup_test_data():
    """Create all test data."""
    base_dir = Path(__file__).parent / "test_data"

    # Clean up existing data
    if base_dir.exists():
        import shutil
        shutil.rmtree(base_dir)

    base_dir.mkdir(parents=True, exist_ok=True)

    print("Creating test data...")

    # 1. Simple CBZ files (no conflicts)
    print("  - Creating simple CBZ files (no conflicts)...")
    simple_dir = base_dir / "simple"
    create_cbz(
        simple_dir / "simple1.cbz",
        ["page_001.jpg", "page_002.jpg", "page_003.jpg"],
        "CBZ1"
    )
    create_cbz(
        simple_dir / "simple2.cbz",
        ["page_004.jpg", "page_005.jpg", "page_006.jpg"],
        "CBZ2"
    )

    # 2. Conflicting CBZ files
    print("  - Creating conflicting CBZ files...")
    conflict_dir = base_dir / "conflict"
    create_cbz(
        conflict_dir / "conflict1.cbz",
        ["cover.jpg", "page_001.jpg", "page_002.jpg"],
        "CBZ1"
    )
    create_cbz(
        conflict_dir / "conflict2.cbz",
        ["cover.jpg", "page_001.jpg", "page_003.jpg"],
        "CBZ2"
    )
    create_cbz(
        conflict_dir / "conflict3.cbz",
        ["cover.jpg", "page_002.jpg", "page_004.jpg"],
        "CBZ3"
    )

    # 3. Nested directory structure
    print("  - Creating nested CBZ files...")
    nested_dir = base_dir / "nested"
    create_cbz(
        nested_dir / "nested1.cbz",
        ["chapter1/page_001.jpg", "chapter1/page_002.jpg"],
        "CBZ1"
    )
    create_cbz(
        nested_dir / "nested2.cbz",
        ["chapter2/page_001.jpg", "chapter2/page_002.jpg"],
        "CBZ2"
    )

    # 4. Many CBZ files for padding tests
    print("  - Creating many CBZ files (10000 files, this may take a while)...")
    many_dir = base_dir / "many"

    # Create specific named files
    specific_names = ["chap1", "chap2", "chap3", "chap9", "chap10", "chap11", "chap1000", "chap10000"]
    for i, name in enumerate(specific_names):
        create_cbz(
            many_dir / f"{name}.cbz",
            [f"page_{j:03d}.jpg" for j in range(3)],
            f"Chapter_{name}"
        )
        if (i + 1) % 100 == 0:
            print(f"    Created {i + 1} specific files...")

    # Create numbered files for padding tests
    # We'll create 10000 files total
    for i in range(10000):
        create_cbz(
            many_dir / f"chapter{i:05d}.cbz",
            [f"page_{j:03d}.jpg" for j in range(3)],
            f"Chapter{i}"
        )
        if (i + 1) % 1000 == 0:
            print(f"    Created {i + 1} / 10000 files...")

    # 5. CBZ with directories in the zip
    print("  - Creating CBZ with directory entries...")
    special_dir = base_dir / "special"
    cbz_path = special_dir / "with_dirs.cbz"
    cbz_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(cbz_path, 'w') as zf:
        zf.writestr("folder/", "")  # Directory entry
        zf.writestr("folder/file.jpg", "content")
        zf.writestr("file2.jpg", "content2")

    # 6. Invalid/test files
    print("  - Creating invalid test files...")
    invalid_dir = base_dir / "invalid"
    invalid_dir.mkdir(parents=True, exist_ok=True)
    (invalid_dir / "not_a_zip.cbz").write_text("This is not a ZIP file")

    print(f"\n[OK] Test data created in: {base_dir.absolute()}")
    print(f"     Total size: {sum(f.stat().st_size for f in base_dir.rglob('*.cbz')) / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    setup_test_data()
