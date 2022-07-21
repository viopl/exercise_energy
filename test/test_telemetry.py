import filecmp
import os
from glob import glob

import pytest

import src.telemetry as telemetry

TEST_DIR = os.path.dirname(__file__)


@pytest.mark.parametrize(
    "test_method", [telemetry.invalidate_zeros, telemetry.aggregate_telemetry]
)
def test_no_input(test_method):
    """Test the methods when the input file does not exist
    in this case, OSError should have been raised"""
    file_input = "Not existing file"
    with pytest.raises(OSError) as e:
        test_method(file_input, None)

    assert str(e.value) == f"File '{file_input}' does not exist"


@pytest.mark.parametrize(
    "test_method", [telemetry.invalidate_zeros, telemetry.aggregate_telemetry]
)
def test_no_output(test_method):
    """Test the methods when the path for the output file does not exist
    in this case, OSError should have been raised"""
    file_input = __file__  # misuse the current module

    with pytest.raises(OSError):
        test_method(file_input, None)

    with pytest.raises(OSError):
        test_method(file_input, "Not existing output file")

    with pytest.raises(OSError):
        test_method(file_input, TEST_DIR)


@pytest.mark.parametrize(
    "file_mask,test_method",
    [
        ("zero*.csv", telemetry.invalidate_zeros),
        ("agg*.csv", telemetry.aggregate_telemetry),
    ],
)
def test_files(tmp_path, file_mask, test_method):
    """Put the input data in directory ./data with the name matching the mask
    and the expected result into a file with the same name but extension ".res"
    After calling the methods, their output will be compared with the expected result
    """

    for file_input in glob(os.path.join(TEST_DIR, "data", file_mask)):
        file_expected = os.path.splitext(file_input)[0] + ".res"

        file_output = os.path.join(tmp_path, os.path.basename(file_input))

        test_method(file_input, file_output)

        assert filecmp.cmp(file_expected, file_output)
