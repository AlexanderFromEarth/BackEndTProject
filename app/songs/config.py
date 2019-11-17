import os


class Config:
    pass


class DebugConfig(Config):
    DEBUG = True
    SQLDATABASE_DATABASE_URI = 'sqlite:///{}'.format(
        os.path.join(os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))),
                     'songs.db')
    )
