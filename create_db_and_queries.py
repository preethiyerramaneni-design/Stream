import pandas as pd
import sqlite3
from pathlib import Path

# Path to your CSV
csv_file = Path("argo_data/argo_master_clean.csv")

# Load CSV
df = pd.read_csv(csv_file)

# Connect to SQLite
conn = sqlite3.connect("argo_data/argo_data.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS argo_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    depth REAL,
    temperature REAL,
    salinity REAL,
    lat REAL,
    lon REAL
)
""")

# Ensure lat/lon exist
if 'lat' not in df.columns:
    df['lat'] = None
if 'lon' not in df.columns:
    df['lon'] = None

# Insert CSV into table
df.to_sql("argo_profiles", conn, if_exists="replace", index=False)

conn.commit()
conn.close()
print("✅ CSV successfully saved to SQLite database")