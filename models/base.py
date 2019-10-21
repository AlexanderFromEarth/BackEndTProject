import sqlite3

from datetime import date
from errors import ValidationError


class SQLiteModel:
    _DATABASE = None
    _TABLE = None
    _MAPPING = {}
    __TYPE_MAPPING = {
        int : 'INTEGER',
        str : 'TEXT',
        float : 'REAL',
        date : 'DATE'
    }


    @classmethod
    def _connect(cls):
        return sqlite3.connect(cls._DATABASE)


    @classmethod
    def get_by_pk(cls, pk):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(
            """
                SELECT *
                FROM :table
                WHERE id = :pk
            """,
            {'table': cls._TABLE, 'pk': pk}
        )

        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col] = record[idx]
        conn.close()
        return result


    @classmethod
    def create_mapping(cls):
        conn = cls._connect()
        cur = conn.cursor()
        mapfortable = tuple([str(k) + " " + str(cls.__TYPE_MAPPING.get(v)) for k, v in cls._MAPPING.items()])
        
        cur.execute("""CREATE TABLE IF NOT EXISTS ? (id INTEGER AUTOINCREMENT PRIMARY KEY""" + (",?" * len(mapfortable)) + """)""", (cls._TABLE,) + mapfortable)

        conn.commit()
        conn.close()


    def insert(self):
        conn = self._connect()
        cur = conn.cursor()
        keys = tuple([str(k) for k in self._MAPPING.keys()])
        vals = tuple([self.__dict__[v] for v in self._MAPPING.keys()])

        cur.execute("""INSERT INTO ?("""+ ("?," * len(keys))[:-1] +""") VALUES("""+ ("?," * len(vals))[:-1] +""")""", (self._TABLE,) + keys + vals)
        
        pk = cur.lastrowid

        conn.commit()
        conn.close()
        
        return pk

    def delete_by_pk(self, pk):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
                        DELETE FROM :table 
                        WHERE id = :pk
                    """, 
                    {"table" : self._TABLE, "pk" : pk}
        )

        conn.commit()
        conn.close()


class BaseModel(SQLiteModel):
    _DATABASE = 'def.db'

    def __getattr__(self, attr):
        if attr in self._MAPPING.keys():
            return None
        raise AttributeError()

    def __setattr__(self, attr, val):
        if attr in self._MAPPING.keys():
            if self._validate(attr, val):
                self.__dict__[attr] = val
                return
        raise AttributeError()

    def fill(self, data):
        for key, val in data.items():
            if self._validate(key, val):
                self.__dict__[key] = val
    
    def _validate(self, key, val):
        key_type = self._MAPPING.get(key)

        if not key_type:
            raise ValidationError

        if key_type != type(val):
            raise ValidationError

        return True

    @classmethod
    def get_by_pk(cls, pk):
        record = cls.get_by_pk(pk)
        obj = cls()
        obj.fill_data(record)
        return obj
    
    def get_data(self):
        data = {}

        for key in self._MAPPING:
            data[key] = getattr(self, key)

        return data
