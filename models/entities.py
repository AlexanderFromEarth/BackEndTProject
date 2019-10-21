from datetime import date
from base import BaseModel

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
