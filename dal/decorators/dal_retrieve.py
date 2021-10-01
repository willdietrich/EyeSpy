import sqlite3


def dal_retrieve(func):
    def _decorate(self, *args):
        cursor: sqlite3.Cursor = self.db.cursor()
        query: str = func(*args)
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows

    return _decorate


