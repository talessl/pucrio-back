import os
from src.infrastructure.db.database import DatabaseInterface

def setup_database(db: DatabaseInterface):
    conn = db.get_connection()

    schema_path = os.path.join("src", "infrastructure", "db", "schema.sql")
    seed_path = os.path.join("src", "infrastructure", "db", "seed.sql")

    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    with open(seed_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
        