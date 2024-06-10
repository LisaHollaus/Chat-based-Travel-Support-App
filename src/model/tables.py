from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base() # All custom classes must inherit from a known Base:


class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True, autoincrement=True) # unique id gets created automatically with autoincrement
    name = Column(String, unique=True)  # user-name has to be unique 
    password = Column(String)   
    type = Column(String) # provider or traveller

    # Many-to-One relationship with Attraction through provider_id
    attractions = relationship("Attraction", backref="provider", overlaps="attractions,provider") 

    # Many-to-Many relationship with Attraction through secondary table
    visited_attractions = relationship("Attraction", secondary='attraction_traveller', back_populates="visitors")
    
    # Many to One relationship with Attraction
    favourite_attractions = relationship("Attraction", backref="attractions", overlaps="attractions,provider")

    def __init__(self):
        self.attractions = [] 


class Attraction(Base):
    __tablename__ = 'attraction_table'

    id = Column(Integer, autoincrement=True, primary_key=True) # unique id gets created automatically
    name = Column(String)
    description = Column(String)
    contact = Column(String)
    price_range = Column(String)
    rating = Column(Float)
    special_offer = Column(String)
    destination = Column(String)
    attraction_type = Column(String)


    # Many-to-One relationship with User
    provider_id = Column(Integer, ForeignKey('user_table.id'))

    # Many-to-Many relationship with User
    visitors = relationship('User', secondary='attraction_traveller', back_populates='visited_attractions')

    # foreign keys:
    #provider_id = Column(Integer, ForeignKey('user_table.id')) # many to one relationship with user
    
    # many to many relationship with traveller
    #travellers_ids = relationship('User', secondary='attraction_traveller', back_populates='visited_attractions')
    
    def __init__(self): 
        pass


# association table for many to many relationship between attraction and traveller
association_table = Table('attraction_traveller', Base.metadata,
    Column('attraction_id', Integer, ForeignKey('attraction_table.id')),
    Column('traveller_id', Integer, ForeignKey('user_table.id'))
)


# create the engine and the tables in the database (if they do not exist yet):
# gets executed when the file is imported
engine = create_engine('sqlite:///travel_app.db') # create a database file
Base.metadata.create_all(engine) # creates tables if they don't exist yet