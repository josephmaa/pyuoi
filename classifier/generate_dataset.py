import os
from pathlib import Path


def main():
    """
    This script is meant to be run from the parent directory of pyuoi
    """
    current_working_directory = Path(os.path.abspath(os.getcwd()))
    print(current_working_directory.parent)
    for file in os.listdir(os.path.join(current_working_directory.parent, "pyuoi")):
        print(file)


if __name__ == "__main__":
    main()
