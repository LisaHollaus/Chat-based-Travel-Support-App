# 'from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship


# # engine = create_engine('sqlite:///travel_app.db', echo=True)
# Base = declarative_base() # All custom classes must inherit from a known Base:


# class User(Base):
#     __tablename__ = 'user_table'
#     name = Column(String, primary_key=True) # user name has to be unique
#     password = Column(String)
#     attractions = Column(String)
#     type = Column(String) # provider or traveller

    


# class Destination(Base):
#     __tablename__ = 'destination_table'


#     def __init__(self, bars=[], restaurants=[], tours=[], hotels=[]):
#         self.bars = bars
#         self.restaurants = restaurants
#         self.tours = tours
#         self.hotels = hotels
    
#     def __init__(self):
#         pass


# # create engine:
# ###nedded?
# engine = create_engine('sqlite:///travel_app.db', echo=True)
# Base.metadata.create_all(engine) ### create database or table?

