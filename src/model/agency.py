from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
#from uuid import uuid1

#from .user import *
from .attraction import * # import the Attraction and User class and create the tables in the database



class Agency(object):
    singleton_instance = None
    

    # lists needed?
    def __init__(self, travellers=[], providers=[], destinations=[]):
        #self.travellers = travellers
        #self.providers = providers
        #self.destinations = destinations
        self.engine = create_engine('sqlite:///travel_app.db', echo=True)
        #self.connection = self.engine.connect() # connect to the database
        self.loged_in_user_id = None # to keep track of the loged in user

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
        # closing the session is done in the functions that use it
        
        
    def create_user(self, name, type, password):
        session = self.start_session() # create a session
        
        try:
            user = User()
            #user.id = uuid1()
            user.name = name
            user.type = type
            user.password = password

            session.add(user)
            session.commit() 
        except:
            return user # return None if the user already exists

        user = session.query(User).filter(User.name == name, User.password == password).first() # get the user from the database to access the id
        self.loged_in_user_id = user.id # set the loged in user
        session.close() 
        return user
    
    def get_user(self, name, password):
        session = self.start_session()
        user = session.query(User).filter(User.name == name, User.password == password).first() # get the user from the database .first() returns the first result or None
        
        self.loged_in_user_id = user.id
        session.close()
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




# provider functions:

    def get_options_provider(self):
        return {1: "add attraction", 2: "remove attraction", 3: "update attraction", 4: "view attractions", 5: "logout"}
    
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


        attraction.provider_id = self.loged_in_user_id

        session.add(attraction)
        session.commit()
        
        # Load the currentlly loged in user
        loged_in_user = session.query(User).get(self.loged_in_user_id)

        # Refresh loged_in_user to make sure it has the latest data
        #session.refresh(loged_in_user)

        loged_in_user.attractions.append(attraction)

        session.close()
        return attraction
        
    def remove_attraction(self, name, destination):
        session = self.start_session()
        attraction = session.query(Attraction).filter(Attraction.name == name, Attraction.destination == destination).first()
        if attraction and (attraction in self.loged_in_user_id.attractions): # check if the attraction exists and if it belongs to the provider
            session.delete(attraction)
            session.commit()
            session.close()
            return attraction
        session.close()
        return None
    
    def get_attraction(self, name, destination):
        session = self.start_session()
        attraction = session.query(Attraction).filter(Attraction.name == name, Attraction.destination == destination).first()
        session.close()
        if attraction:
            return attraction
        return "Attraction not found!"
    
    def get_attractions(self):
        #session = self.start_session()
        #attractions = session.query(Attraction).filter(Attraction in self.loged_in_user.attractions).all() # get all attractions from the provider
        #session.close()
        #attractions = sorted([attraction.name for attraction in attractions]) # get the names of the attractions
        
        ##### does this work? :
        attractions = sorted([f"{attraction.name} in {attraction.destination}" for attraction in self.loged_in_user_id.attractions]) # get the names of the attractions
        return attractions
    
    def get_attraction_details(attraction):
        return f"Name: {attraction.name}\nDestination: {attraction.destination}\nType: {attraction.attraction_type}\nPrice range: {attraction.price_range}\nDescription: {attraction.description}\nContact: {attraction.contact}\nSpecial offer: {attraction.special_offer}\n" 

    
    