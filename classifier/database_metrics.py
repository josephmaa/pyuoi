import sqlite3


def generate_sql_database_distribution(path_to_database: str):
    """
    Count all the unique behaviors in the column 'behavior' in the given sql database.

    Input:
        path_to_database: path to database as a string.
    Output:
        behavior_map: dictionary of behaviors to count.
    """
    # Connect the existing database to the file.
    conn = sqlite3.connect(path_to_database)
    cur = conn.cursor()
    cur.execute(
        f"SELECT behavior_name, COUNT(*) FROM ShuffledDownSampled GROUP BY behavior_name"
    )

    result = cur.fetchall()
    conn.close()

    return result
