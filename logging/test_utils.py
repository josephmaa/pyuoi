"""Helper functions for tests."""

import os
import pathlib
import shutil

TMP_DIR = "tmp/nested_tmp"


def object_logging_dir():
    return os.path.join(TMP_DIR)


def create_temp_dir():
    path = pathlib.Path(TMP_DIR)
    path.mkdir(parents=True, exist_ok=True)


def delete_temp_dir():
    path = pathlib.Path(TMP_DIR)
    shutil.rmtree(path.parts[0], ignore_errors=True)
