import time
from contextlib import contextmanager
from django.db.backends.sqlite3.base import\
    DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.utils import\
    CursorWrapper as DjangoCursorWrapper


@contextmanager
def calculate_sql_time(sql: str):
    timestamp = time.monotonic()

    yield
    # print(
    #     f'SQL-request time {sql} - '
    #     f'{time.monotonic() - timestamp:.3f} sec'
    # )

class CursorWrapper(DjangoCursorWrapper):
    def execute(self, sql: str, params=None):
        with calculate_sql_time(sql):
            return super().execute(sql, params)


class DatabaseWrapper(DjangoDatabaseWrapper):
    def create_cursor(self, name=None):
        cursor = super().create_cursor(name)
        return CursorWrapper(cursor, self)
