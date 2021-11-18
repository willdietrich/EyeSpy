import sqlite3


def dal_execute_param(func):
    def _decorate(*args) -> int:
        db: sqlite3.Connection = args[0].db
        query, data = func(*args)

        cursor = db.cursor()
        cursor.execute(query, data)
        db.commit()
        return cursor.lastrowid

    return _decorate
