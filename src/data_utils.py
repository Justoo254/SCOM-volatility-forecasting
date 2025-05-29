import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
import glob
import pandas as pd
def combine_files(filepath):
    csv_files = glob.glob(filepath)
    df= pd.concat ([pd.read_csv(f) for f in csv_files],ignore_index=True)
    df["Date"]=pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df
def get_connection():
    db_path = os.getenv("DB_PATH")
    if not db_path:
        raise ValueError("DB_PATH not set in .env file")
    
    # Convert to absolute path relative to this file's directory
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Go 2 levels up to project root
    full_path = os.path.join(base_dir, db_path)
    
    return sqlite3.connect(full_path)
