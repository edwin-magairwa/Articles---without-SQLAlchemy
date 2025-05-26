import os
import sqlite3
from lib.db.connection import get_connection
from lib.db.seed import seed

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '../lib/db/schema.sql')
DB_PATH = os.path.join(os.path.dirname(__file__), '../articles.db')

def setup_db():
    # Create DB and run schema
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.executescript(schema_sql)
    finally:
        conn.close()
    # Seed data
    seed()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_db()
