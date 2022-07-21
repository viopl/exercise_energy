import importlib
import os
import sys

import pytest

TEST_DIR = os.path.dirname(__file__)

PROJECT_DIR = os.path.dirname(TEST_DIR)

sys.path.insert(0, PROJECT_DIR)
tele_io = importlib.import_module(".tele_io", "src")


def test_check_file():
    """Test the check_file method"""

    # existing file > expect True
    assert tele_io.check_file(__file__)

    # directory name > exception
    with pytest.raises(OSError):
        tele_io.check_file(TEST_DIR)

    # non existing file must raise exception
    with pytest.raises(OSError):
        tele_io.check_file("No file at all")


def test_check_file_path():
    """Test the check_file_path method"""

    # existing file > expect True
    assert tele_io.check_file_path(__file__)

    # non-existing file in an existing directory > expect True
    assert tele_io.check_file_path(os.path.join(TEST_DIR, "missing_file.txt"))

    # path is empty > exception
    with pytest.raises(OSError):
        tele_io.check_file_path("")

    # path is a directory name > exception
    with pytest.raises(OSError):
        tele_io.check_file_path(TEST_DIR)

    # path does not exist > exception
    with pytest.raises(OSError):
        tele_io.check_file_path(
            os.path.join(TEST_DIR, "missing_subdir", "file_name.txt")
        )
