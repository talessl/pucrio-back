import sqlite3
from src.infrastructure.db.database import DatabaseInterface

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, path: str):
        self.path = path
        self._conn = None
    
    def get_connection(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON")
        return self._conn
    
    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None