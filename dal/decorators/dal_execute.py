import sqlite3


def dal_execute(func):
    def _decorate(*args):
        db: sqlite3.Connection = args[0].db
        response: str = func(*args)

        db.cursor().execute(response)
        db.commit()

    return _decorate
