import sqlite3


def dal_retrieve(func):
    def _decorate(self, *args):
        cursor: sqlite3.Cursor = self.db.cursor()
        query, data = func(self, *args)
        if data is None:
            cursor.execute(query)
            rows = cursor.fetchall()
        else:
            cursor.execute(query, data)
            rows = cursor.fetchall()

        return rows

    return _decorate


