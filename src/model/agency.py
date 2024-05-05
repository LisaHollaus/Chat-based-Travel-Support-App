from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from .traveller import *




class Agency(object):
    singleton_instance = None
    

    # lists needed?
    def __init__(self, travellers=[], providers=[], destinations=[]):
        #self.travellers = travellers
        #self.providers = providers
        #self.destinations = destinations
        self.engine = create_engine('sqlite:///travel_app.db', echo=True)
        #self.connection = self.engine.connect() # connect to the database
    
        self.loged_in_users = None

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
        user = session.query(User).filter(User.name == name, User.password == password) # get the user from the database 
        print("user:", user) ###check output
        session.close()
        self.loged_in_users = user
        return user



        

    