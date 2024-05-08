from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from .user import *
#from .destination import *
from .attraction import *



class Agency(object):
    singleton_instance = None
    

    # lists needed?
    def __init__(self, travellers=[], providers=[], destinations=[]):
        #self.travellers = travellers
        #self.providers = providers
        #self.destinations = destinations
        self.engine = create_engine('sqlite:///travel_app.db', echo=True)
        #self.connection = self.engine.connect() # connect to the database
        self.loged_in_user = None # to keep track of the loged in user

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()
            #engine = create_engine('sqlite:///travel_app.db', echo=True)
            #Base.metadata.create_all(engine) # create the tables in the database    

        return Agency.singleton_instance
    
    def start_session(self):
        SessionClass = sessionmaker(bind=self.engine)
        session = SessionClass()
        return session
        
        
    def create_user(self, name, type, password):
        session = self.start_session() # create a session
        
        try:
            user = User()
            user.name = name
            user.type = type
            user.password = password

            session.add(user)
            session.commit() 
        except:
            user = None

        session.close() 
        self.loged_in_users = user
        return user
    
    def get_user(self, name, password):
        session = self.start_session()
        user = session.query(User).filter(User.name == name, User.password == password).first() # get the user from the database .first() returns the first result or None
        session.close()
        self.loged_in_users = user
        return user
    
    def get_destinations(self):
        session = self.start_session()
        destinations = session.query(Attraction.destination).all() # get all destinations from the database as a list of tuples
        session.close()
        destinations = sorted(list(set([destination[0] for destination in destinations]))) # remove duplicates and convert to a sorted list
        return destinations


### change:
    def get_options_traveller(self, destination):
        session = self.start_session()
        attractions = session.query(Attraction).filter(Attraction.destination == destination).all()
        session.close()
        attractions = sorted(list(set([attraction.attraction_type for attraction in attractions]))) # remove duplicates and convert to a sorted list 
        return attractions

    def get_options_provider(self):
        return [{1: "1) add attraction"}, {2: "2) remove attraction"}, {3: "3) update attraction"}, {4: "4) view attractions"}, {5: "5) logout"}]
    
    def add_attraction(self, name, destination, attraction_type, price_range, description, contact, special_offer):
        session = self.start_session()
        existing_attraction = session.query(Attraction).filter(Attraction.name == name, Attraction.destination == destination).first()
        if existing_attraction: # check if the attraction already exists
            session.close()
            return None
        attraction = Attraction()
        attraction.name = name 
        attraction.destination = destination
        attraction.attraction_type = attraction_type
        attraction.price_range = price_range
        attraction.description = description
        attraction.contact = contact
        attraction.special_offer = special_offer
        session.add(attraction)
        session.commit()
        session.close()
        return attraction
        

    