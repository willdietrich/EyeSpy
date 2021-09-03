import sqlite3


def dal_execute(func):
    def _decorate(*args):
        db: sqlite3.Connection = args[0].db
        query = func(*args)
        db.cursor().execute(query)
        db.commit()

    return _decorate
