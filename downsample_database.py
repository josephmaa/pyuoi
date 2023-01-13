import sqlite3
import pandas as pd
import time
import os
import argparse


def database_to_dataframe(input_db_file_path: str):
    """
    Transforms a SQL database to a pandas dataframe.
    """
    # Connect to the existing SQL database file.
    conn = sqlite3.connect(input_db_file_path)

    start = time.time()
    sql_query = pd.read_sql_query(
        """
                               SELECT
                               *
                               FROM features
                               """,
        conn,
    )
    end = time.time()

    print(f"Script took {end-start} seconds to run.")

    df = pd.DataFrame(sql_query)

    return df


def create_downsampled_database(input_db_file_path: str, num_rows: int) -> None:
    """
    Creates a downsampled SQL database from an input SQL database using a select query with a COUNT.
    """
    # Generate the path to the output SQL database file path based on the input database file path.
    input_db_file_directory = os.path.split(input_db_file_path)[0]
    output_db_file_path = os.path.join(
        input_db_file_directory, f"downsampled{num_rows:.2e}.db"
    )

    # Create the output database file.
    file_handle = open(output_db_file_path, "w")
    file_handle.close()

    # Connect the existing database to the file.
    conn = sqlite3.connect(output_db_file_path)
    cur = conn.cursor()
    cur.execute(f"ATTACH DATABASE '{input_db_file_path}' as 'TEST'")

    # Create a new table called features that has the selected number of rows.
    cur.execute(
        f"CREATE TABLE ShuffledDownSampled AS SELECT * FROM TEST.ShuffledDownSampled LIMIT {num_rows}"
    )

    # TODO(Joseph): Use the logging module to add a log entry to an output directory.
    print(f"Output SQL database created with {num_rows} rows.")


def downsample_database(database_path: str, num_rows: int):
    create_downsampled_database(
        input_db_file_path=database_path,
        num_rows=num_rows,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", help="The path to the input SQL database.")
    parser.add_argument(
        "--num_rows",
        help="The final number of rows to downsample the SQL database to.",
        type=int,
        default=0,
    )
    args = parser.parse_args()
    downsample_database(database_path=args.database_path, num_rows=int(args.num_rows))


if __name__ == "__main__":
    main()
