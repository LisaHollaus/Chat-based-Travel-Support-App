from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# engine = create_engine('sqlite:///travel_app.db', echo=True)
Base = declarative_base() # All custom classes must inherit from a known Base:


class User(Base):
    __tablename__ = 'user_table'
    name = Column(String, primary_key=True) # user name has to be unique
    password = Column(String)
    attractions = Column(String)
    type = Column(String) # provider or traveller

    def __init__(self):
        pass


# create engine:
engine = create_engine('sqlite:///travel_app.db', echo=True) 
Base.metadata.create_all(engine) # create the tables in the database