import random
from sqlalchemy.orm import sessionmaker
from src.model.tables import *


# Functions to support the server side of the application
class ServerHelper(object):
    singleton_instance = None 
    
    def __init__(self):
        self.engine = create_engine('sqlite:///../../travel_app.db')  # to connect to the database
        self.logged_in_user_id = None  # to keep track of the logged-in user

    @staticmethod
    def get_instance():
        if ServerHelper.singleton_instance is None:
            ServerHelper.singleton_instance = ServerHelper()

        return ServerHelper.singleton_instance
    
    def start_session(self):
        SessionClass = sessionmaker(bind=self.engine)
        session = SessionClass()
        return session
        # closing the session is done in the functions that use it (yield was not supported in the functions)    
    
    def create_user(self, name, type, password):
        session = self.start_session()  # create a session
        try:  # if the user does not exist already
            user = User()
            user.name = name
            user.type = type
            user.password = password

            session.add(user)
            session.commit()

        # catch the exception if the user already exists
        except Exception as e:
            session.close() 
            return "user already exists" 
        
        user = session.query(User).filter(User.name == name, User.password == password).first()  # get the user from the database to access the id
        self.logged_in_user_id = user.id  # set the logged in user
        session.close() 
        return user
    
    def get_user(self, name, password, type):
        session = self.start_session()
        user = session.query(User).filter(User.name == name, User.password == password, User.type == type).first()  # get the user from the database .first() returns the first result or None
        if user:
            self.logged_in_user_id = user.id  # set the logged in user
        session.close()
        return user
    
    def get_attraction(self, name, destination):
        session = self.start_session()
        attraction = session.query(Attraction).filter(Attraction.name == name, Attraction.destination == destination).first()  # get the attraction from the database or None
        session.close()
        if attraction:
            return attraction
        return "Attraction not found!"

    def get_attraction_details(self, attraction):
        session = self.start_session()
        attraction = session.query(Attraction).filter(Attraction.id == attraction.id).first()  # get the attraction from the database again to access the visitors
        
        # get the visitors of the attraction or an empty list
        visitors = attraction.visitors if attraction.visitors else [] 
        session.close()
        return f"\nName: {attraction.name}\nDestination: {attraction.destination}\nType: {attraction.attraction_type}\nPrice range: {attraction.price_range}\nDescription: {attraction.description}\nContact: {attraction.contact}\nSpecial offer: {attraction.special_offer}\nRating: {attraction.rating} \nVisited by at least {len(visitors)} travellers" 

    # loop to view the details of as many attractions as the user wants
    def view_attraction_details_loop(self, conn, traveller=False):  # traveller is an optional parameter to give the traveller the option to add the attraction to the favourites list
        while True:
            # receive the name and destination of the attraction
            name = conn.recv(4096).decode()
            destination = conn.recv(4096).decode()
            # get the attraction
            attraction = self.get_attraction(name, destination)
            
            # send the attraction details or "Attraction not found!"
            if attraction == "Attraction not found!":
                conn.send(attraction.encode())
            else: 
                attraction_details = self.get_attraction_details(attraction) 
                conn.send(attraction_details.encode())

                # if the user is a traveller and the attraction was found he can add it to his favourites
                if traveller: 
                    favourite = conn.recv(4096).decode()  # "Would you like to add this attraction to your favourites? (yes/no)"
                    if favourite.lower() == "yes":
                        added = self.add_to_favourites(attraction)
                        conn.send(added.encode())  # "Attraction added to favourites!" or "Attraction already in favourites!"
                    else:
                        conn.send(" ".encode())  # send a blank message to keep the conversation going
                                
            # "Would you like to see details of another attraction? (yes/no)"
            answer = conn.recv(4096).decode()
            if answer.lower() == "no":
                break

## traveller functions:
    def get_options_traveller(self):
        return {1: "Explore attractions", 2: "Get details of a specific attraction", 3: "See favorite attractions", 4: "Rate visited attraction", 5: "See history of visited attractions", 6: "Logout"}

    def get_destinations(self):
        session = self.start_session()
        destinations = session.query(Attraction.destination).all()  # get all destinations from the database as a list of tuples
        session.close()
        # There should always be destinations in the database
        destinations = sorted(list(set([destination[0] for destination in destinations])))  # remove duplicates and convert to a sorted list
        return ",".join(destinations)  # return the destinations as a string separated by commas, so we can send it to the client
    
    def get_attractions_by_destination(self, destination):
        session = self.start_session()
        # if the user wants to explore a random attraction (types-in "everywhere")
        if destination == "everywhere":  # get a random attractions
            destinations = session.query(Attraction.destination).distinct().all()  # get all destinations from the database as a list of tuples without duplicates
            destination = random.choice(destinations)[0]  # get a random destination
        
        # check if there are attractions in the given destination
        attractions = session.query(Attraction).filter(Attraction.destination == destination).all()  # get all attractions in the destination
        session.close()

        if attractions:
            attractions = sorted([f"{attraction.attraction_type}: {attraction.name}" for attraction in attractions]) 
            attractions = f"Here's a list of all attractions in {destination}:\n" + ",".join(attractions)  # add the destination to the list and return it as a string separated by commas
        else:
            attractions = "No attractions found!"
        return attractions
    
    def add_to_favourites(self, attraction):
        session = self.start_session()
        user = session.get(User, self.logged_in_user_id)
        try:
            # adding the attraction to the user's favourite attractions only works if the attraction is not already in the list
            user.favourite_attractions.append(attraction)  # raises an exception if the attraction is already in the list
            session.commit()
            return "Attraction added to favourites!"

        except Exception as e:
            return "Attraction already in favourites!"

        finally:
            session.close()
        
    def get_favourites(self):
        session = self.start_session()
        user = session.get(User, self.logged_in_user_id)
        if user.favourite_attractions:
            favourites = sorted([f"{attraction.name} in {attraction.destination}" for attraction in user.favourite_attractions])  # get the names and their destination of the attractions
        else:
            favourites = ["No favourite attractions found!"]  # return this in a list to be able to iterate over it
        session.close()
        return favourites

    def check_if_rated(self, attraction):
        session = self.start_session()
        user = session.get(User, self.logged_in_user_id)
        attraction = session.get(Attraction, attraction.id)
        visited_attractions_names = [a.name for a in user.visited_attractions]
        # check if the attraction was already rated
        if attraction.name in visited_attractions_names:
            session.close()
            return True
        session.close()
        return False
    
    def rate_attraction(self, attraction, rating):
        session = self.start_session()
        attraction = session.merge(attraction)  # bind the attraction to the session to be able to commit the changes
        
        # update the rating of the attraction
        if attraction.rating == None:  # if the attraction has no rating yet set the rating to the given rating
            attraction.rating = rating
        else:
            attraction.rating = (float(attraction.rating) + float(rating)) / 2  # calculate the new rating
        
        # add the user to the visitors of the attraction
        user = session.get(User, self.logged_in_user_id)
        attraction.visitors.append(user)  # add the user to the visitors
        session.commit()
        
        # add the attraction to the visited attractions of the user
        user.visited_attractions.append(attraction)
        session.commit()
        session.close()
        return "\nAttraction rated! \nThank you for your feedback!"

    def get_visited_attractions(self):
        session = self.start_session()
        user = session.get(User, self.logged_in_user_id)
        if user.visited_attractions:  # check if the user has visited any attractions
            visited_attractions = sorted([f"{attraction.name} in {attraction.destination}" for attraction in user.visited_attractions])  # get the names and their destination of the attractions
        else:
            visited_attractions = ["No visited attractions found!"]  # return this in a list to be able to iterate over it
        session.close()
        return visited_attractions

### provider functions:
    def get_options_provider(self):
        return {1: "Add attraction", 2: "View attractions", 3: "Update attraction", 4: "Remove attraction", 5: "Logout"}

    def add_attraction(self, name, destination, attraction_type, price_range, description, contact, special_offer):
        session = self.start_session()
        existing_attraction = session.query(Attraction).filter(Attraction.name == name, Attraction.destination == destination).first()
        if existing_attraction:  # check if the attraction already exists
            session.close()
            return None
        
        # create a new attraction
        attraction = Attraction()
        attraction.name = name 
        attraction.destination = destination
        attraction.attraction_type = attraction_type
        attraction.price_range = price_range
        attraction.description = description
        attraction.contact = contact
        attraction.special_offer = special_offer
        attraction.provider_id = self.logged_in_user_id

        session.add(attraction)
        session.commit()
        
        # Load the currently logged in user
        logged_in_user = session.get(User, self.logged_in_user_id)
        logged_in_user.attractions.append(attraction)
        session.commit()

        session.close()
        return attraction
    
    def get_id(self):
        return self.logged_in_user_id

    def update_attraction(self, updated_attraction):
        session = self.start_session()
        session.merge(updated_attraction)  # update/merge the attraction
        session.commit()
        session.close()
        return "Attraction updated!"
        
    def remove_attraction(self, attraction): 
        session = self.start_session()

        # check if the attraction belongs to the provider
        if attraction.provider_id == self.logged_in_user_id:  # check if it belongs to the provider
            session.delete(attraction)
            session.commit()
                
            attraction = session.get(Attraction, attraction.id)
            session.close()
            return attraction  # return None if the attraction was removed
        
        session.close()
        return "Attraction belongs to another provider!"
    
    def get_attractions(self):  # get all attractions of the provider
        session = self.start_session()
        user = session.get(User, self.logged_in_user_id)

        if user.attractions:
            attractions = sorted([f"{attraction.name} in {attraction.destination}" for attraction in user.attractions])  # get the names and their destination of the attractions
        else: 
            attractions = ["No attractions found!"]  # return this in a list to be able to iterate over it
        session.close()
        return ",".join(attractions)  # return the attractions as a string separated by commas, so we can send it to the client
    

   