import random
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
#from uuid import uuid1

#from .user import *
from .tables import * # import the Attraction and User class and create the tables in the database if they don't exist


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
        if user:
            self.loged_in_user_id = user.id # set the loged in user
        session.close()
        return user
    

# traveller functions:

    def get_options_traveller(self):
        return {1: "explore attractions", 2: "get details of a specific attraction", 3: "rate visited attraction", 4: "logout"}

    def get_destinations(self):
        session = self.start_session()
        destinations = session.query(Attraction.destination).all() # get all destinations from the database as a list of tuples
        session.close()
        # no if/else needed because there should always be destinations in the database
        destinations = sorted(list(set([destination[0] for destination in destinations]))) # remove duplicates and convert to a sorted list
        return destinations 
    
    def get_attractions_by_destination(self, destination):
        session = self.start_session()
        if destination == "everywhere": # get a random attractions
            destinations = session.query(Attraction.destination).distinct().all() # get all destinations from the database as a list of tuples without duplicates
            destination = random.choice(destinations)[0] # get a random destination
        attractions = session.query(Attraction).filter(Attraction.destination == destination).all() # get all attractions in the destination
        session.close()
        if attractions:
            attractions = sorted([f"{attraction.attraction_type}: {attraction.name}" for attraction in attractions]) 
        else:
            attractions = ["no attractions found!"]
        return attractions

    def visit_attraction(self, attraction):
        session = self.start_session()
        user = session.query(User).get(self.loged_in_user_id)
        user.visited_attractions.append(attraction)
        session.commit()
        session.close()
        return "Attraction visited!"

        
   # def get_destinations(self):
    #    session = self.start_session()
     #   destinations = session.query(Attraction.destination).all() # get all destinations from the database as a list of tuples
      #  session.close()
       # destinations = sorted(list(set([destination[0] for destination in destinations]))) # remove duplicates and convert to a sorted list
        #return destinations










# provider functions:

    def get_options_provider(self):
        return {1: "add attraction", 2: "view attractions", 3: "update attraction", 4: "remove attraction", 5: "logout"}
    

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
    
    def get_attraction(self, name, destination):
        session = self.start_session()
        attraction = session.query(Attraction).filter(Attraction.name == name, Attraction.destination == destination).first() # get the attraction from the database or None
        session.close()
        if attraction:
            return attraction
        return "Attraction not found!"

    def get_id(self):
        return self.loged_in_user_id

    def update_attraction(self, updated_attraction):
        session = self.start_session()
        session.merge(updated_attraction) # update the attraction
        session.commit()
        session.close()
        return "Attraction updated!"
        
    def remove_attraction(self, attraction): 
        session = self.start_session()

        # check if the attraction belongs to the provider
        if attraction.provider_id == self.loged_in_user_id: # check if it belongs to the provider
            session.delete(attraction)
            session.commit()
                
            attraction = session.query(Attraction).get(attraction.id)
            session.close()
            return attraction # return None if the attraction was removed
        
        session.close()
        return "Attraction belongs to another provider!"
            
    
    
    def get_attractions(self):
        session = self.start_session()
       
        user = session.query(User).get(self.loged_in_user_id)
        if user.attractions:
            attractions = sorted([f"{attraction.name} in {attraction.destination}" for attraction in user.attractions]) # get the names and their destination of the attractions
        else: 
            attractions = ["no attractions found!"] # return this in a list to be able to iterate over it
        session.close()
        return attractions
    
    def get_attraction_details(self, attraction):
        return f"\nName: {attraction.name}\nDestination: {attraction.destination}\nType: {attraction.attraction_type}\nPrice range: {attraction.price_range}\nDescription: {attraction.description}\nContact: {attraction.contact}\nSpecial offer: {attraction.special_offer}\n Rating: {attraction.rating} \nVisited by: {len(attraction.visitors)} travellers \nReviews: {attraction.reviews}\n" 

    
    