import pyuoi
import pandas as pd
import sqlite3

DF_PATH = "test_small.db"

def main():
	conn = sqlite3.connect(DF_PATH)
	c = conn.cursor()
	df = pd.read_sql(DF_PATH)
	

if __name__ == "__main__":
	main()
