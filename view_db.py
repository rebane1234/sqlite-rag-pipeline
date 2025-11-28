import sqlite3
import pandas as pd
import dtale

# 1. Connect to the DB
db_path = "ai_knowledge_base.db"
conn = sqlite3.connect(db_path)

# 2. Read the tables into Pandas DataFrames
print("Loading raw pages...")
df_pages = pd.read_sql_query("SELECT * FROM raw_pages", conn)

print("Loading vectors (this might take a moment)...")
df_vectors = pd.read_sql_query("SELECT * FROM knowledge_vectors", conn)

conn.close()

# 3. Start D-Tale
print("Starting D-Tale for Raw Pages...")
d = dtale.show(df_pages)
d.open_browser()

# Keep script running
input("\nPress ENTER to stop...")