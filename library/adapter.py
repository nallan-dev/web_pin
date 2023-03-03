import sqlite3
from pathlib import Path
from sqlite3 import Connection, Cursor

from conf import settings

DB_PATH = settings.DATABASES["default"]["NAME"]


class SQLite3Adapter:
    def __init__(self, db_path: Path | str):
        self.db_path = db_path
        self.connection: Connection | None = None
        self.cursor: Cursor | None = None

    def start(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()

    def stop(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute(self, sql: str, *args, **kwargs):
        self.cursor.execute(sql, *args, **kwargs)

    def fetch_rows(self, sql: str, *args, **kwargs) -> list[dict]:
        self.execute(sql, *args, **kwargs)
        return [dict(row) for row in self.cursor.fetchall()]

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if exc_val:
            raise


db_adapter = SQLite3Adapter(DB_PATH)
