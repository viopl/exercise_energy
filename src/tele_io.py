"""
perform the OS tasks
"""
import os


def check_file(file_name: str) -> bool:
    """Checks existence of a file
    :param file_name: full or relative path to a file
    :return: True if file exists; raises error if file does not exist
    """
    if os.path.exists(file_name) and os.path.isfile(file_name):
        return True

    raise OSError(f"File '{file_name}' does not exist")


def check_file_path(file_path: str) -> bool:
    """Checks existence of a directory
    :param file_path: full or relative path to a file
    :return: True if the path exists; raises error if the path does not exist or is not a file
    """
    if not file_path:  # None or empty string
        raise OSError(f"File name may not be empty")
    elif not os.path.exists(file_path):
        # file does not exist, so check the path
        dirname = os.path.dirname(file_path)
        if not os.path.exists(dirname) or not os.path.isdir(dirname):
            raise OSError(f"Path '{dirname}' does not exist")
    elif not os.path.isfile(file_path):
        # the file_path is a directory
        raise OSError(f"'{file_path}' is a directory, must be a file")

    return True
