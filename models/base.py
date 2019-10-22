import sqlite3

from datetime import date
from errors import ValidationError


class SQLiteModel:
    _DATABASE = None
    _TABLE = None
    _MAPPING = {}


    @classmethod
    def _connect(cls):
        return sqlite3.connect(cls._DATABASE)


    @classmethod
    def get_one(cls, pk):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(
            """
                SELECT *
                FROM """ + cls._TABLE + """
                WHERE id = :pk
            """,
            {'pk': pk}
        )

        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col[0]] = record[idx]
        conn.close()
        return result


    @classmethod
    def create_mapping(cls):
        conn = cls._connect()
        cur = conn.cursor()
        cols = ', '.join(str(col_name) + ' ' + col_type.__name__ for col_name, col_type in cls._MAPPING.items())
        
        cur.execute("""CREATE TABLE IF NOT EXISTS """ + cls._TABLE + """ (id INTEGER PRIMARY KEY NOT NULL, """ + cols + """)""")

        conn.commit()
        conn.close()


    def insert(self):
        conn = self._connect()
        cur = conn.cursor()
        cols = ', '.join(str(col_name) for col_name in self._MAPPING.keys())
        print(cols)
        vals = tuple([getattr(self, v) for v in self._MAPPING.keys()])

        cur.execute("""INSERT INTO """ + self._TABLE + """ ("""+ cols +""") VALUES("""+ ("?," * len(vals))[:-1] +""")""", vals)
        
        pk = cur.lastrowid

        conn.commit()
        conn.close()
        
        return pk


    def delete_by_pk(self, pk):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
                        DELETE FROM """+ self._TABLE + """
                        WHERE id = :pk
                    """, 
                    {"pk" : pk}
        )

        conn.commit()
        conn.close()


class BaseModel(SQLiteModel):
    _DATABASE = 'test.db'


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
            return False

        if val and key_type != type(val):
            raise ValidationError

        return True


    @classmethod
    def get_by_pk(cls, pk):
        record = cls.get_one(pk)
        obj = cls()
        obj.fill(record)
        return obj
    

    @property
    def serialize(self):
        data = {}

        for key in self._MAPPING:
            data[key] = getattr(self, key)

        return data
