import sqlite3
import xarray as xr
import os
from tqdm import tqdm

DATAFRAMES_FILE_DIRECTORY = "features_all"
SQL_ALCHEMY_COMMAND = "mysql://admin@localhost/Volumes/LaCie/test.db"
DB_FILE_PATH = "/Volumes/LaCie/test.db"

def create_table(conn: sqlite3.Connection, create_table_sql: str) -> None:
    """
    Create a table from the create_table_sql statement.
    """
    try: 
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def main():
    conn = sqlite3.connect(DB_FILE_PATH)
    sql_create_features_table = """CREATE TABLE IF NOT EXISTS features (
                                        id integer PRIMARY KEY
                                    ); """
    create_table(conn, sql_create_features_table)
    c = conn.cursor()
    for f in tqdm(os.listdir(DATAFRAMES_FILE_DIRECTORY)):
        if f.endswith(".netcdf"):
            df = xr.load_dataset(os.path.join(DATAFRAMES_FILE_DIRECTORY, os.path.basename(f)), engine="h5netcdf").to_dataframe()
            try:
                df.to_sql(name="features", con=conn, if_exists="append", index=False)
            except:
                df.to_sql(name="features", con=conn, if_exists="replace", index=False)
    c.close()

if __name__ == "__main__":
    main()