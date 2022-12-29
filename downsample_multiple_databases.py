import csv
from downsample_database import downsample_database
import argparse

DATABASE_SIZES_FILE = "database_sizes.csv"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", help="The path to the input SQL database.")

    args = parser.parse_args()

    with open(DATABASE_SIZES_FILE, "r") as database_sizes_file:
        database_sizes_file_reader = csv.reader(database_sizes_file, delimiter=",")
        for row in database_sizes_file_reader:
            for database_size in row:
                downsample_database(database_path=args.database_path, num_rows=database_size)


if __name__ == "__main__":
    main()
