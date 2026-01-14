import sqlite3
from core.logger import log


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("scopes.db")
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS scopes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scope TEXT UNIQUE
            )
        """)
        self.conn.commit()

    def get_all(self):
        cur = self.conn.execute("SELECT scope FROM scopes")
        return {row[0] for row in cur.fetchall()}

    def save(self, scopes):
        self.conn.execute("DELETE FROM scopes")
        for s in scopes:
            self.conn.execute("INSERT OR IGNORE INTO scopes(scope) VALUES (?)", (s,))
        self.conn.commit()
        log("Escopos atualizados no banco.")
