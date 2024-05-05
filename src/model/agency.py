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


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()
            #engine = create_engine('sqlite:///travel_app.db', echo=True)
            #Base.metadata.create_all(engine) # create the tables in the database    

        return Agency.singleton_instance
    
    # def session(self):
    #     Session = sessionmaker(bind=self.engine)
    #     session = Session()
    #     Base = declarative_base() # All custom classes must inherit from a known Base
    #     Base.metadata.create_all(self.engine) # create the tables in the database    
    #     yield session
    #     session.close()
        
    def create_user(self, name, type, password):
            ### into init?
        SessionClass = sessionmaker(bind=self.engine)  # bind engine to a session
        session = SessionClass()  # create a Class
        #check = session.query(User).filter(User.name == name)  # check name already exists
        
        # ## if it works use try except
        # if check:
        #    user = "user already exists"
        # else: 
        #     user = User(name=name, type=type, password=password)

        #     session.add(user)
        #     session.commit()  
        try:
            user = User()
            user.name = name
            user.type = type
            user.password = password

            session.add(user)
            session.commit() 
        except:
            user = "user already exists"

        session.close() 

        #self.connection.execute(Traveller.insert().values(name=user.name, type=user.type, password=user.password))        
        #self.connection.commit()
            
        #self.connection.close()
        return user

        

    