from inspect import get_annotations
from typing import Any
import sqlite3

from bookkeeper.repository.abstract_repository import AbstractRepository, T
from bookkeeper.models.category import Category


class SQLiteRepository(AbstractRepository[T]):
    db_file: str
    cls: type
    table_name: str
    fields: dict

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.cls = cls
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({', '.join(self.fields.keys())})")
        con.close()

    def add(self, obj) -> None:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object with filled primary key attribute')
        names = ', '.join(self.fields.keys())
        placeholders = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) '
                f'VALUES ({placeholders})', values
            )
            obj.pk = cur.lastrowid
            cur.execute(
                f'UPDATE {self.table_name} SET pk = {obj.pk} '
                f'WHERE ROWID = {obj.pk}'
            )
        con.close()

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'SELECT * FROM {self.table_name} WHERE pk = {pk}'
            )
            obj_tuple = cur.fetchone()
        con.close()
        obj = self.cls(obj_tuple)
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'SELECT * FROM {self.table_name}'
            )
            objs_tuple = cur.fetchall()
        con.close()
        objs = []
        for obj_tuple in objs_tuple:
            objs.append(self.cls(obj_tuple[1:], pk=obj_tuple[0]))
        if where is None:
            return objs
        else:
            return [obj for obj in objs
                    if all(getattr(obj, attr) == where[attr] for attr in
                           where.keys())]

    def update(self, pk: int, attrs: tuple) -> None:
        if pk == 0:
            raise ValueError(f'trying to update objects {attrs} with unknown primary key')
        names = list(self.fields.keys())
        sets = ', '.join(f'{name} = \'{attrs[names.index(name)]}\''
                         for name in names)
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'UPDATE {self.table_name} SET {sets} WHERE pk = {pk}'
            )
        con.close()

    def delete(self, pk: int) -> None:
        if self.get(pk) is None:
            raise KeyError
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'DELETE FROM {self.table_name} WHERE pk = {pk}'
            )
        con.close()
