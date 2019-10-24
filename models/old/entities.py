from datetime import date
from .base import BaseModel

class UserModel(BaseModel):
    _TABLE='Users'
    _MAPPING = {
        'realname' : str,
        'username' : str,
        'password' : str,
        'email' : str,
        'birthday' : date,
        'join_date' : date,
        'info' : str,
        'phone_number' : str,
        'city' : str
    }


class SongModel(BaseModel):
    _TABLE = 'Songs'
    _MAPPING = {
        'title': str,
        'author_id': int,
        'publication_date': date,
    }


class ArtistsModel(BaseModel):
    _TABLE = 'Artists'
    _MAPPING = {
        'name': str,
        'establishment_date': date,
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
    _TABLE = 'Articles'
    _MAPPING = {
        'creator_id': int,
        'title': str,
        'text': str,
        'publication_date': date,
    }


class SearchEntryModel(BaseModel):
    _TABLE = 'SearchEntries'
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
