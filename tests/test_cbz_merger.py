"""Unit tests for CBZ merger functionality."""

import zipfile
from pathlib import Path
import pytest

from comick_merger.cbz_merger import CBZFile, CBZMerger


class TestCBZFile:
    """Tests for CBZFile class."""

    def test_load_valid_cbz(self, simple_cbz_files):
        """Test loading a valid CBZ file."""
        cbz = CBZFile.from_path(simple_cbz_files[0])

        assert cbz.path == simple_cbz_files[0]
        assert len(cbz.entries) == 3
        assert "page_001.jpg" in cbz.entries
        assert "page_002.jpg" in cbz.entries
        assert "page_003.jpg" in cbz.entries

    def test_load_nonexistent_cbz(self, temp_dir):
        """Test loading a nonexistent CBZ file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            CBZFile.from_path(temp_dir / "nonexistent.cbz")

    def test_load_invalid_zip(self, invalid_cbz_dir):
        """Test loading an invalid ZIP file raises ValueError."""
        with pytest.raises(ValueError, match="Not a valid ZIP/CBZ file"):
            CBZFile.from_path(invalid_cbz_dir / "not_a_zip.cbz")

    def test_cbz_excludes_directories(self, special_cbz_dir):
        """Test that directories are excluded from entries."""
        cbz = CBZFile.from_path(special_cbz_dir / "with_dirs.cbz")

        # Only files, not directories
        assert len(cbz.entries) == 2
        assert "folder/" not in cbz.entries
        assert "folder/file.jpg" in cbz.entries


class TestCBZMergerConflictDetection:
    """Tests for conflict detection in CBZMerger."""

    def test_no_conflicts(self, simple_cbz_files):
        """Test that no conflicts are detected when files are unique."""
        merger = CBZMerger(simple_cbz_files)
        conflicts = merger.detect_conflicts()

        assert len(conflicts) == 0

    def test_detect_conflicts(self, conflicting_cbz_files):
        """Test that conflicts are properly detected."""
        merger = CBZMerger(conflicting_cbz_files)
        conflicts = merger.detect_conflicts()

        # cover.jpg appears in all 3 CBZ files
        assert "cover.jpg" in conflicts
        assert len(conflicts["cover.jpg"]) == 3
        assert conflicts["cover.jpg"] == [0, 1, 2]

        # page_001.jpg appears in CBZ 0 and 1
        assert "page_001.jpg" in conflicts
        assert len(conflicts["page_001.jpg"]) == 2
        assert conflicts["page_001.jpg"] == [0, 1]

        # page_002.jpg appears in CBZ 0 and 2
        assert "page_002.jpg" in conflicts
        assert len(conflicts["page_002.jpg"]) == 2
        assert conflicts["page_002.jpg"] == [0, 2]

    def test_nested_path_conflicts(self, nested_cbz_files):
        """Test that nested paths don't conflict when in different folders."""
        merger = CBZMerger(nested_cbz_files)
        conflicts = merger.detect_conflicts()

        # No conflicts: chapter1/page_001.jpg != chapter2/page_001.jpg
        assert len(conflicts) == 0


class TestCBZMergerPadding:
    """Tests for padding calculation in CBZMerger."""

    def test_padding_with_2_files(self, many_cbz_dir):
        """Test padding calculation with 2 files (indices 0-1)."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:2]
        merger = CBZMerger(cbz_files)

        padding = merger._calculate_prefix_padding()

        # 2 files: 0-1, max is 1, len("1") = 1
        assert padding == 1

    def test_padding_with_10_files(self, many_cbz_dir):
        """Test padding calculation with 10 files (indices 0-9)."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:10]
        merger = CBZMerger(cbz_files)

        padding = merger._calculate_prefix_padding()

        # 10 files: 0-9, max is 9, len("9") = 1
        assert padding == 1

    def test_padding_with_11_files(self, many_cbz_dir):
        """Test padding calculation with 11 files (indices 0-10)."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:11]
        merger = CBZMerger(cbz_files)

        padding = merger._calculate_prefix_padding()

        # 11 files: 0-10, max is 10, len("10") = 2
        assert padding == 2

    def test_padding_with_100_files(self, many_cbz_dir):
        """Test padding calculation with 100 files (indices 0-99)."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:100]
        merger = CBZMerger(cbz_files)

        padding = merger._calculate_prefix_padding()

        # 100 files: 0-99, max is 99, len("99") = 2
        assert padding == 2

    def test_padding_with_1000_files(self, many_cbz_dir):
        """Test padding calculation with 1000 files (indices 0-999)."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:1000]
        merger = CBZMerger(cbz_files)

        padding = merger._calculate_prefix_padding()

        # 1000 files: 0-999, max is 999, len("999") = 3
        assert padding == 3

    def test_padding_with_10000_files(self, many_cbz_dir):
        """Test padding calculation with 10000 files (indices 0-9999)."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:10000]
        merger = CBZMerger(cbz_files)

        padding = merger._calculate_prefix_padding()

        # 10000 files: 0-9999, max is 9999, len("9999") = 4
        assert padding == 4


class TestCBZMergerWithSpecificNames:
    """Tests with specific file names as requested."""

    def test_specific_chapter_names(self, many_cbz_dir):
        """Test with specific chapter names: chap1, chap2, chap3, chap9, chap10, chap11, chap1000, chap10000."""
        names = ["chap1", "chap2", "chap3", "chap9", "chap10", "chap11", "chap1000", "chap10000"]
        cbz_files = [many_cbz_dir / f"{name}.cbz" for name in names]

        # Verify all files exist
        for cbz_file in cbz_files:
            assert cbz_file.exists(), f"Missing test file: {cbz_file}"

        merger = CBZMerger(cbz_files)
        padding = merger._calculate_prefix_padding()

        # 8 files: 0-7, max is 7, len("7") = 1
        assert padding == 1
        assert len(merger.cbz_files) == 8

        # Verify all files loaded
        loaded_names = [cbz.path.stem for cbz in merger.cbz_files]
        assert loaded_names == names

    def test_padding_sufficient_for_1000_files(self, many_cbz_dir):
        """Test that padding is sufficient to handle 1000 files (0000-0999)."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:1000]
        merger = CBZMerger(cbz_files)

        padding = merger._calculate_prefix_padding()

        # With 1000 files, we need padding of 3 to represent 0-999
        assert padding == 3

        # Verify we can format all indices properly
        for i in range(1000):
            formatted = str(i).zfill(padding)
            assert len(formatted) == 3
            if i < 10:
                assert formatted.startswith("00")
            elif i < 100:
                assert formatted.startswith("0")

        # Check specific values
        assert str(0).zfill(padding) == "000"
        assert str(1).zfill(padding) == "001"
        assert str(999).zfill(padding) == "999"


class TestCBZMergerMerging:
    """Tests for the actual merging functionality."""

    def test_merge_simple_files_with_prefixes(self, simple_cbz_files, temp_dir):
        """Test merging simple files with prefix method."""
        merger = CBZMerger(simple_cbz_files)
        output = temp_dir / "merged.cbz"

        merger.merge(output, use_prefixes=True)

        assert output.exists()

        # Verify contents
        with zipfile.ZipFile(output, 'r') as zf:
            entries = zf.namelist()
            assert len(entries) == 6  # 3 files from each CBZ

            # Check prefixes
            assert "0_page_001.jpg" in entries
            assert "0_page_002.jpg" in entries
            assert "0_page_003.jpg" in entries
            assert "1_page_004.jpg" in entries
            assert "1_page_005.jpg" in entries
            assert "1_page_006.jpg" in entries

    def test_merge_simple_files_with_folders(self, simple_cbz_files, temp_dir):
        """Test merging simple files with folder method."""
        merger = CBZMerger(simple_cbz_files)
        output = temp_dir / "merged.cbz"

        merger.merge(output, use_prefixes=False)

        assert output.exists()

        # Verify contents
        with zipfile.ZipFile(output, 'r') as zf:
            entries = zf.namelist()
            assert len(entries) == 6

            # Check folders
            assert "0/page_001.jpg" in entries
            assert "0/page_002.jpg" in entries
            assert "0/page_003.jpg" in entries
            assert "1/page_004.jpg" in entries
            assert "1/page_005.jpg" in entries
            assert "1/page_006.jpg" in entries

    def test_merge_conflicting_files_with_prefixes(self, conflicting_cbz_files, temp_dir):
        """Test merging conflicting files with prefixes resolves conflicts."""
        merger = CBZMerger(conflicting_cbz_files)
        output = temp_dir / "merged.cbz"

        merger.merge(output, use_prefixes=True)

        assert output.exists()

        # Verify all files are preserved with prefixes
        with zipfile.ZipFile(output, 'r') as zf:
            entries = zf.namelist()

            # 3 CBZ files with 3 files each = 9 files total
            assert len(entries) == 9

            # Check that conflicts are resolved
            assert "0_cover.jpg" in entries
            assert "1_cover.jpg" in entries
            assert "2_cover.jpg" in entries

            # Verify content is preserved
            content_0 = zf.read("0_cover.jpg").decode()
            assert "CBZ1" in content_0

            content_1 = zf.read("1_cover.jpg").decode()
            assert "CBZ2" in content_1

    def test_merge_many_files_correct_padding(self, many_cbz_dir, temp_dir):
        """Test that merging many files uses correct padding."""
        cbz_files = sorted(many_cbz_dir.glob("chapter*.cbz"))[:100]
        merger = CBZMerger(cbz_files)
        output = temp_dir / "merged.cbz"

        merger.merge(output, use_prefixes=True)

        # Verify padding is 2 (for 0-99)
        with zipfile.ZipFile(output, 'r') as zf:
            entries = zf.namelist()

            # Should have files with 2-digit prefixes
            assert "00_page_000.jpg" in entries
            assert "01_page_000.jpg" in entries
            assert "09_page_000.jpg" in entries
            assert "10_page_000.jpg" in entries
            assert "99_page_000.jpg" in entries

    def test_merge_preserves_file_content(self, simple_cbz_files, temp_dir):
        """Test that merging preserves file content correctly."""
        merger = CBZMerger(simple_cbz_files)
        output = temp_dir / "merged.cbz"

        merger.merge(output, use_prefixes=True)

        with zipfile.ZipFile(output, 'r') as zf:
            # Check content from first CBZ
            content = zf.read("0_page_001.jpg").decode()
            assert "CBZ1 of page_001.jpg" in content

            # Check content from second CBZ
            content = zf.read("1_page_004.jpg").decode()
            assert "CBZ2 of page_004.jpg" in content

    def test_merge_nested_paths_with_prefixes(self, nested_cbz_files, temp_dir):
        """Test merging files with nested paths using prefixes."""
        merger = CBZMerger(nested_cbz_files)
        output = temp_dir / "merged.cbz"

        merger.merge(output, use_prefixes=True)

        with zipfile.ZipFile(output, 'r') as zf:
            entries = zf.namelist()

            # Prefixes are added to the entire path
            assert "0_chapter1/page_001.jpg" in entries
            assert "0_chapter1/page_002.jpg" in entries
            assert "1_chapter2/page_001.jpg" in entries
            assert "1_chapter2/page_002.jpg" in entries

    def test_merge_nested_paths_with_folders(self, nested_cbz_files, temp_dir):
        """Test merging files with nested paths using folders."""
        merger = CBZMerger(nested_cbz_files)
        output = temp_dir / "merged.cbz"

        merger.merge(output, use_prefixes=False)

        with zipfile.ZipFile(output, 'r') as zf:
            entries = zf.namelist()

            # Folders wrap the entire path
            assert "0/chapter1/page_001.jpg" in entries
            assert "0/chapter1/page_002.jpg" in entries
            assert "1/chapter2/page_001.jpg" in entries
            assert "1/chapter2/page_002.jpg" in entries
