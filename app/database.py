from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import settings


class SQLAlchemy:
    def __init__(self):
        self.Model = declarative_base()
        self.settings = settings

    def init_app(self, app):
        SQLALCHEMY_DATABASE_URI = self.settings.DATABASE_URL

        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # self.Model.metadata.create_all(bind=self.engine)


db = SQLAlchemy()


# Dependency
def get_db():
    try:
        x = db.session()
        yield x
    finally:
        x.close()
