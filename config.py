import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(
                                                    os.path.dirname(
                                                        os.path.abspath(
                                                            __file__
                                                            )),
                                                    'my.db'))
SECRET_KEY = 'nasosalibabi'
