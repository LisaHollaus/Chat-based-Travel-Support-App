from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
#from .user import User


Base = declarative_base() # All custom classes must inherit from a known Base:

# # association table for many to many relationship between attraction and traveller
# association_table = Table('attraction_traveller', Base.metadata,
#     Column('attraction_id', Integer, ForeignKey('attraction_table.id')),
#     Column('traveller_id', Integer, ForeignKey('user_table.id'))
# )

class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True, autoincrement=True) # unique id gets created automatically
    name = Column(String, unique=True)  # user name has to be unique 
    
    password = Column(String)   
    type = Column(String) # provider or traveller

    # Many-to-One relationship with Attraction through provider_id
    attractions = relationship("Attraction", backref="provider")

    #attractions = relationship("Attraction",  secondary='attraction_traveller', back_populates="users") # one to many relationship with attraction 
    
    # Many-to-Many relationship with Attraction through secondary table
    visited_attractions = relationship("Attraction", secondary='attraction_traveller', back_populates="visitors")
  

    def __init__(self):
        self.attractions = [] 


class Attraction(Base):
    __tablename__ = 'attraction_table'
    # use UUID as primary key?
    id = Column(Integer, autoincrement=True, primary_key=True) # unique id gets created automatically
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


    # Many-to-One relationship with User
    provider_id = Column(Integer, ForeignKey('user_table.id'))

    # Many-to-Many relationship with User
    visitors = relationship('User', secondary='attraction_traveller', back_populates='visited_attractions')

    # foreign keys:
    #provider_id = Column(Integer, ForeignKey('user_table.id')) # many to one relationship with user
    
    # many to many relationship with traveller
    #travellers_ids = relationship('User', secondary='attraction_traveller', back_populates='visited_attractions')
    
    def __init__(self): 
        self.travellers_ids = [] # list of traveller ids that visited the attraction
        # needed?


engine = create_engine('sqlite:///travel_app.db', echo=True)
Base.metadata.create_all(engine) # creates table when it does not exist

# association table for many to many relationship between attraction and traveller
association_table = Table('attraction_traveller', Base.metadata,
    Column('attraction_id', Integer, ForeignKey('attraction_table.id')),
    Column('traveller_id', Integer, ForeignKey('user_table.id'))
)

Base.metadata.create_all(engine) # creates table when it does not exist


#User.attractions = relationship('Attraction', secondary=association_table, backref="users")



# gets executed when the file is imported
# create engine and create the tables in the database (if they do not exist):

Base.metadata.create_all(engine) # creates table when it does not exist