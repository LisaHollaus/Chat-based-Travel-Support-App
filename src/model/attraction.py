from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base() # All custom classes must inherit from a known Base:


class Attraction(Base):
    __tablename__ = 'attraction_table'
    id = Column(Integer, primary_key=True, autoincrement=True) # unique gets created automatically
    name = Column(String)
    description = Column(String)
    contact = Column(String)
    price_range = Column(String)
    rating = Column(Float)
    reviews = Column(String)
    #bookings = Column(String)
    #visited = Column(String)
    special_offer = Column(String)
    destination = Column(String)
    attraction_type = Column(String)

    
    def __init__(self):
        pass


# create engine:
engine = create_engine('sqlite:///travel_app.db', echo=True)
Base.metadata.create_all(engine) #### create database/ table?