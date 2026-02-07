"""Pytest fixtures for comick-merger tests."""

from pathlib import Path
import pytest


# Base path for test data
TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to the test data directory."""
    if not TEST_DATA_DIR.exists():
        raise RuntimeError(
            f"Test data directory not found: {TEST_DATA_DIR}\n"
            "Please run: python tests/setup_test_data.py"
        )
    return TEST_DATA_DIR


@pytest.fixture(scope="session")
def simple_cbz_files(test_data_dir):
    """Simple CBZ files without conflicts."""
    simple_dir = test_data_dir / "simple"
    return [
        simple_dir / "simple1.cbz",
        simple_dir / "simple2.cbz",
    ]


@pytest.fixture(scope="session")
def conflicting_cbz_files(test_data_dir):
    """CBZ files with conflicting file paths."""
    conflict_dir = test_data_dir / "conflict"
    return [
        conflict_dir / "conflict1.cbz",
        conflict_dir / "conflict2.cbz",
        conflict_dir / "conflict3.cbz",
    ]


@pytest.fixture(scope="session")
def nested_cbz_files(test_data_dir):
    """CBZ files with nested directory structures."""
    nested_dir = test_data_dir / "nested"
    return [
        nested_dir / "nested1.cbz",
        nested_dir / "nested2.cbz",
    ]


@pytest.fixture(scope="session")
def many_cbz_dir(test_data_dir):
    """Directory containing many CBZ files for padding tests."""
    return test_data_dir / "many"


@pytest.fixture(scope="session")
def special_cbz_dir(test_data_dir):
    """Directory containing special CBZ files (with dirs, etc.)."""
    return test_data_dir / "special"


@pytest.fixture(scope="session")
def invalid_cbz_dir(test_data_dir):
    """Directory containing invalid test files."""
    return test_data_dir / "invalid"


# Temporary directory fixture for output files
@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test outputs."""
    return tmp_path
