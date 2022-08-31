import os


def main():
    """
    This script is meant to be run from the parent directory of pyuoi
    """
    current_working_directory = os.get_cwd()
    for file in os.lostdir(current_working_directory):
        print(file)


if __name__ == "__main__":
    main()
