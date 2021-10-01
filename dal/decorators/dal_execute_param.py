import sqlite3


def dal_execute_param(func):
    def _decorate(*args):
        db: sqlite3.Connection = args[0].db
        query, data = func(*args)

        db.cursor().execute(query, data)
        db.commit()

    return _decorate
