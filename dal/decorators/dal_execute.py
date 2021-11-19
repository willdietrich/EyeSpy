import sqlite3


def dal_execute(func):
    def _decorate(self, *args) -> int:
        db: sqlite3.Connection = self.db
        query, data = func(self, *args)
        cursor = db.cursor()

        if data is None:
            cursor.execute(query)
        else:
            cursor.execute(query, data)

        db.commit()

        return cursor.lastrowid

    return _decorate
