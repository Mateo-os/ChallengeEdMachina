import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

default_url = 'postgresql://postgres:postgres@localhost:5432/challenge'
DATABASE_URL = os.getenv('DATABASE_URL',default=default_url) 

engine = create_engine(DATABASE_URL)

session = sessionmaker(autocommit = False, autoflush=False,bind = engine)
 
Base = declarative_base()