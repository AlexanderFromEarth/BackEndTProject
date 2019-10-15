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

    @classmethod
    def update_mapping(cls):
        """Сделать обновления полей таблицы"""
        pass

    @classmethod
    def insert(cls):
        conn = cls._connect()
        cur = conn.cursor()
        keys = tuple([str(k) for k in cls._MAPPING.keys()])
        vals = tuple([cls.__dict__[v] for v in cls._MAPPING.keys()])

        cur.execute("""INSERT INTO ?("""+ ("?," * len(keys))[:-1] +""") VALUES("""+ ("?," * len(vals))[:-1] +""")""", (cls._TABLE,) + keys + vals)
        
        pk = cur.lastrowid

        conn.commit()
        conn.close()
        
        return pk


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


class UserModel(BaseModel):
    _TABLE='Users'
    _MAPPING = {
        'realname' : str,
        'username' : str,
        'password' : str,
        'email' : str,
        'birthday' : date,
        'registration_date' : date,
        'info' : str,
        'phone_number' : str,
        'city' : str
    }


class SongModel(BaseModel):
    _TABLE = 'Songs'
    _MAPPING = {
        'title': str,
        'author': str,
        'song_duration ': str,
        'publication_date': date,
    }


class GroupModel(BaseModel):
    _TABLE = 'Groups'
    _MAPPING = {
        'title': str,
        'group_members': str,
        'establishment_date': date,
    }


class GroupMemberModel(BaseModel):
    _TABLE = 'GroupMember'
    _MAPPING = {
        'group_id': int,
        'user_id': int,
    }


class MessageModel(BaseModel):
    _TABLE = 'Messages'
    _MAPPING = {
        'send_user_id': int,
        'receive_user_id': int,
        'text': str,
        'send_date': date,
    }


class ArticleModel(BaseModel):
    _TABLE = 'Article'
    _MAPPING = {
        'creator_id': int,
        'title': str,
        'text': str,
        'publication_date': date,
    }


class SearchEntryModel(BaseModel):
    _TABLE = 'SearchEntry'
    _MAPPING = {
        'creator_id': int,
        'text': str,
        'role': str,
        'publication_date': date,
    }


class CommentModel(BaseModel):
    _TABLE = 'Comments'
    _MAPPING = {
        'post_id': int,
        'ancestor_id': int,
        'text': str,
        'publication_date': date,
    }


"""Дописать остальные модели"""
