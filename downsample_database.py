import sqlite3
import pandas as pd
import time


def create_downsampled_database(input_db_file_path: str, output_db_file_path: str):
    """
    Creates a downsampled database by converting the existing full SQL database to a pandas dataframe, then downsamples to a smaller sized SQL database.
    """
    # Create the output db file.
    # open(output_db_file_path, "w")

    # Connect the existing database to the file.
    conn = sqlite3.connect(input_db_file_path)
    cur = conn.cursor()
    # cur.execute(f"ATTACH DATABASE '{input_db_file_path}' as 'TEST'")

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
    print(df.head(n=5))


def create_downsampled_head_database(
    input_db_file_path: str, output_db_file_path: str, num_rows: int
) -> None:
    """
    Creates a downsampled database using a select query with a COUNT.
    """
    # Create the output db file.
    file_handle = open(output_db_file_path, "w")
    file_handle.close()

    # Connect the existing database to the file.
    conn = sqlite3.connect(output_db_file_path)
    cur = conn.cursor()
    cur.execute(f"ATTACH DATABASE '{input_db_file_path}' as 'TEST'")

    # Create a new table called features that has the selected number of rows.
    cur.execute(
        f"CREATE TABLE features AS SELECT * FROM TEST.features LIMIT {num_rows}"
    )


def main():
    # create_downsampled_database(
    #     input_db_file_path="test.db",
    #     output_db_file_path=f"test2e6.db",
    #     num_rows=int(2e6),
    # )

    create_downsampled_database(input_db_file_path="test.db", output_db_file_path="")


if __name__ == "__main__":
    main()
