import sqlite3

from datetime import date
from errors import ValidationError


class SQLiteModel:
    _DATABASE = None
    _TABLE = None
    _MAPPING = {}
    __TYPE_MAPPING = {
        int : 'INTEGER',
        float : 'REAL',
        str : 'TEXT',
        date : 'DATE'
    }


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
                FROM {table}
                WHERE id = :pk
            """.format(table=cls._TABLE),
            {'pk': pk}
        )

        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col[0]] = record[idx]
        conn.close()
        return result

    
    @classmethod
    def get_all(cls):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute("""SELECT * 
                       FROM {table}""".format(
                           table=cls._TABLE))

        result = []
        records = cur.fetchall()
        for record in records:
            tmp = {}

            for idx, col in enumerate(cur.description):
                tmp[col[0]] = record[idx]

            result.append(tmp)

        conn.close()
        return result


    @classmethod
    def create_mapping(cls):
        conn = cls._connect()
        cur = conn.cursor()
        
        cur.execute("""CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY NOT NULL, {cols})""".format(
            table=cls._TABLE,
            cols=', '.join('{name} {type}'.format(
                name=name,
                type=cls.__TYPE_MAPPING[cls._MAPPING[name]]
            ) for name in cls._MAPPING)
        ))

        conn.commit()
        conn.close()


    def insert(self):
        conn = self._connect()
        cur = conn.cursor()
        vals = [getattr(self, v) for v in self._MAPPING.keys()]

        cur.execute("""INSERT INTO {table} ({cols}) VALUES({phs})""".format(
            table=self._TABLE,
            cols=', '.join(self._MAPPING),
            phs=', '.join('?' * len(self._MAPPING))
        ), vals)
        
        pk = cur.lastrowid

        conn.commit()
        conn.close()
        
        return pk


    def delete_by_pk(self, pk):
        conn = self._connect()
        cur = conn.cursor()

        cur.execute("""
                        DELETE FROM {table}
                        WHERE id = :pk
                    """.format(table=self._TABLE), 
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
