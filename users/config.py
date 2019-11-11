import os


class Config:
    PORT = 5001
    SQLDATABASE_DATABASE_URI = 'sqlite:///{}'.format(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'users.db')
    )


class DebugConfig(Config):
    DEBUG = True
