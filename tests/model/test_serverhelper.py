from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock  # for simulating user input and output
from src.model.tables import *
from tests.fixtures import serverhelper


def test_singleton_instance(serverhelper):
    # test that the singleton instance is created
    assert serverhelper is not None


def test_start_session(serverhelper):
    session = serverhelper.start_session()
    # check if the returned session is an instance of the session class
    assert isinstance(session, Session) 


def test_create_user(serverhelper):
    # prepare
    session = serverhelper.start_session()
    # delete test user if he already exists
    delete_user = session.query(User).filter(User.name == 'Maximilian', User.type == 'traveller', User.password == 'password').first()
    if delete_user:  # if the user exists, delete him
        session.delete(delete_user)
        session.commit()

    # test
    user = serverhelper.create_user(name='Maximilian', type='traveller', password='password')
    # check if the user has the correct attributes
    assert user.name == 'Maximilian'
    assert user.type == 'traveller'
    assert user.password == 'password'
    # check if the user is in the database
    user_query = session.query(User).filter(User.name == 'Maximilian').first()
    assert user_query is not None  # user should be in the database

    # make sure the user can only be created once
    user2 = serverhelper.create_user(name='Maximilian', type='traveller', password='password')
    assert user2 == "user already exists"  # user2 function should return None since user already exists
    session.close()


def test_get_user(serverhelper):
    # test if the function returns the correct user
    user_query = serverhelper.get_user(name='Maximilian', type='traveller', password='password')  # user added in the previous test
    assert user_query.name == 'Maximilian'
    assert user_query.type == 'traveller'
    assert user_query.password == 'password'

    # test if the function returns None if the user does not exist
    user_query = serverhelper.get_user(name='Maximilian', type='traveller', password='wrong_password')
    assert user_query == None


def test_get_attraction(serverhelper):
    # test if the function returns the correct attractions
    # prepare (add an attraction to the database)
    session = serverhelper.start_session()
    serverhelper.add_attraction(name='Joes', description='-', contact='joe@jams.com', price_range='20-30', special_offer='-', destination='Malibu', attraction_type='Surfing lessons')
    
    attraction = serverhelper.get_attraction(name='Joes', destination='Malibu')
    assert attraction.name == 'Joes'
    assert attraction.description == '-'
    assert attraction.contact == 'joe@jams.com'
    assert attraction.price_range == '20-30'
    assert attraction.special_offer == '-'
    assert attraction.destination == 'Malibu'
    assert attraction.attraction_type == 'Surfing lessons'
    session.close()

    # test if function returns "Attraction not found" if the attraction does not exist
    attraction = serverhelper.get_attraction(name='J', destination='Malibu')
    assert attraction == "Attraction not found!"


def test_get_attraction_details(serverhelper):
    # test if the function returns the correct attraction details
    # using the attraction added in the previous test

    attraction = serverhelper.get_attraction(name='Joes', destination='Malibu')
    attraction_details = serverhelper.get_attraction_details(attraction)
    assert "Name: Joes" in attraction_details
    assert "Destination: Malibu" in attraction_details
    assert "Type: Surfing lessons" in attraction_details
    assert "Price range: 20-30" in attraction_details
    assert "Description: -" in attraction_details
    # not asserting the whole string since the rating and visited by might change
    # assert attraction_details == "\nName: Joes\nDestination: Malibu\nType: Surfing lessons\nPrice range: 20-30\nDescription: -\nContact: joe@jams.com\nSpecial offer: -\nRating: None \nVisited by at least 0 travellers"


@patch('src.sockets.server.ServerHelper')  # mock ServerHelper class
@patch('socket.socket', new_callable=MagicMock)
def test_view_attraction_details_loop(mock_server_helper, mock_socket, serverhelper):
    # Set up the mock socket's recv method to return the values that the view_attraction_details_loop function expects
    mock_socket.recv.side_effect = [
        "Attraction1".encode(),  # name of the attraction
        "Location1".encode(),  # location of the attraction
        "no".encode(),  # decision to add to favourites
        "no".encode()  # decision to not continue
    ]

    # Set up the mock socket's send method to return a value
    mock_socket.send.return_value = None  # the return value is not important

    # Mock the get_attraction and get_attraction_details methods to return a specific attraction
    mock_server_helper.get_instance().get_attraction.return_value = Attraction()
    mock_server_helper.get_instance().get_attraction_details.return_value = "Attraction details"
    mock_server_helper.get_instance().add_to_favourites.return_value = "Attraction added to favourites!"

    # Call the view_attraction_details_loop function with the mock socket
    serverhelper.view_attraction_details_loop(mock_socket, traveller=True)

    # Check that the recv method was called to get the user's decisions
    assert mock_socket.recv.call_count == 3
    # Check that the send method was called to send the attraction details and the result of adding to favourites
    assert mock_socket.send.call_count == 1


## traveller functions
def test_get_options_traveller(serverhelper):
    # test if the function returns the correct options for a traveller
    options = serverhelper.get_options_traveller()
    assert options == {1: "Explore attractions", 2: "Get details of a specific attraction", 3: "See favorite attractions", 4: "Rate visited attraction", 5: "See history of visited attractions", 6: "Logout"}


def test_get_destinations(serverhelper):
    # test if the function returns the correct destinations
    # prepare
    # adding another destination to the database, to test if the function returns the correct destinations
    serverhelper.add_attraction(name='Jimmys', description='Local food', destination='Hawaii', attraction_type='Restaurants', price_range='10-20', contact='j@j.com', special_offer='-')

    # get the destinations from the database
    session = serverhelper.start_session()
    destinations = session.query(Attraction.destination).all()  # get all destinations from the database as a list of tuples
    session.close()
    destinations_database = [destination[0] for destination in destinations]  # convert the list of tuples to a list of strings

    # test
    destinations_function = serverhelper.get_destinations()
    for destination in destinations_database:
        assert destination in destinations_function
        # assert 'Hawaii' in destinations_function
        # assert 'Malibu' in destinations_function


def test_get_attractions_by_destination(serverhelper):
    # test if the function returns the correct attractions by destination
    # prepare
    # add another attraction to the database, for better testing
    attraction = serverhelper.add_attraction(name='JJs', description='Cheap Boat Tours', destination='Hawaii', attraction_type='Tours', price_range='20-50', contact='j.j@boats.com', special_offer='children under 12 free')

    # get the attractions from the database
    session = serverhelper.start_session()
    attractions = session.query(Attraction).filter(Attraction.destination == 'Hawaii').all()  # get all attractions in Hawaii
    session.close()
    attractions_database = [attraction.name for attraction in attractions]  # convert the list of attractions to a list of attraction names
    
    # test
    attractions_function = serverhelper.get_attractions_by_destination('Hawaii')
    for attraction in attractions_database:
        assert attraction in attractions_function

    # test if the function returns "No attractions found!" if the destination is not in the database
    attractions_function = serverhelper.get_attractions_by_destination('Paris')
    assert attractions_function == "No attractions found!"


def test_add_to_favourites(serverhelper):
    # test if the function adds an attraction to the favourites
    # prepare
    session = serverhelper.start_session()
    attraction = serverhelper.get_attraction(name='JJs', destination='Hawaii')  # attraction added in the previous test
    
    # create a new user and get the user from the database
    serverhelper.create_user(name='Timmy', type='traveller', password='pass')  # create a new user and set him as logged in
    serverhelper.get_user(name='Timmy', type='traveller', password='pass')  # this will set the user as logged-in in case the user was already created in a previous test run
    user = session.query(User).filter(User.name == 'Timmy').first()  # get the user from the database, so we can perform the test
    
    # make sure the attraction is not in the favourites
    assert attraction not in user.favourite_attractions
    
    # test
    answer = serverhelper.add_to_favourites(attraction)
    assert answer == "Attraction added to favourites!"

    session.refresh(user)  # refresh the user to get the updated favourites
    favourite_attractions_names = [attraction.name for attraction in user.favourite_attractions]
    
    assert "JJs" in favourite_attractions_names

    # test if the function returns "Attraction already in favourites!" if the attraction is already in the favourites
    answer = serverhelper.add_to_favourites(attraction)
    assert answer == "Attraction already in favourites!"
    session.close()


def test_get_favourites(serverhelper):
    # create a new user to insure there are no favourite attractions
    session = serverhelper.start_session()
    serverhelper.create_user(name='Joey', type='traveller', password='password123')  # create a new user and set him as logged in
    serverhelper.get_user(name='Joey', type='traveller', password='password123')  # this will set the user as logged-in in case the user was already created in a previous test run
    user = session.query(User).filter(User.name == 'Joey').first()  # get the user from the database, so we can perform the test
   
    # test if the function returns the correct favourite attractions if there are favourite attractions
    attraction = serverhelper.get_attraction(name='JJs', destination='Hawaii')  # attraction added in a previous test
    serverhelper.add_to_favourites(attraction)
    session.commit()
    session.refresh(user)  # refresh the user to get the updated favourites
    favourite_attractions = serverhelper.get_favourites()
    assert "JJs in Hawaii" in favourite_attractions
    session.close()

    # test if the function returns "No favourite attractions found!" if there are no favourite attractions
    # create a new user to insure there are no favourite attractions
    serverhelper.create_user(name='Kate', type='traveller', password='word123')
    serverhelper.get_user(name='Kate', type='traveller', password='word123')  # this will set the user as logged-in in case the user was already created in a previous test run
    favourite_attractions = serverhelper.get_favourites()
    assert favourite_attractions == ["No favourite attractions found!"]
        

def test_check_if_rated_false(serverhelper):
    # prepare (Kate logged in)
    session = serverhelper.start_session()
    attraction = serverhelper.get_attraction(name='JJs', destination='Hawaii')  # attraction added in a previous test
    serverhelper.get_user(name='Timmy', type='traveller', password='pass')  # this will set the Timmy as logged in
    user = session.query(User).filter(User.name == 'Timmy').first()  # get the user from the database, so we can perform tests
    
    # make sure the attraction is not in the visited attractions
    visited_attractions_names = [a.name for a in user.visited_attractions]
    assert 'JJs' not in visited_attractions_names

    # test if the function returns the correct value if the attraction is not rated
    answer = serverhelper.check_if_rated(attraction)
    assert answer == False  # the attraction is not rated
    session.close()
    # test if the function returns the correct value if the attraction is rated
    # see next test


def test_rate_attraction(serverhelper):
    # prepare (Timmy logged in)
    session = serverhelper.start_session()
    attraction = serverhelper.get_attraction(name='JJs', destination='Hawaii')  # attraction added in a previous test
    serverhelper.get_user(name='Kate', type='traveller', password='word123')  # this will set the Kate as logged in
    user = session.query(User).filter(User.name == 'Kate').first()  # get the user from the database, so we can perform tests

    # test if the function rates the attraction
    answer = serverhelper.rate_attraction(attraction, "5")
    session.refresh(user)  # refresh the user to get the updated visited attractions
    visited_attractions_names = [a.name for a in user.visited_attractions]
    assert 'JJs' in visited_attractions_names
    assert answer == "\nAttraction rated! \nThank you for your feedback!"
     
    # test if the function returns the correct value if the attraction is rated
    answer = serverhelper.check_if_rated(attraction)
    assert answer == True  # the attraction is rated
    session.close()


def test_get_visited_attractions(serverhelper): 
    # prepare (Kate logged in)
    session = serverhelper.start_session()
    session.query(User).filter(User.name == 'Kate').first()  # get the user from the database, so we can perform tests
    # attraction rated in the previous test

    # test if the function returns the correct visited attractions if there are visited attractions
    visited_attractions = serverhelper.get_visited_attractions()
    assert "JJs in Hawaii" in visited_attractions
    session.close()

    # test if the function returns "No visited attractions found!" if there are no visited attractions
    # create a new user to insure there are no visited attractions
    serverhelper.create_user(name='Lara', type='traveller', password='word123')
    serverhelper.get_user(name='Lara', type='traveller', password='word123')  # this will set the user as logged-in in case the user was already created in a previous test run
    
    visited_attractions = serverhelper.get_visited_attractions()
    assert visited_attractions == ["No visited attractions found!"]
    session.close()


## provider functions
def test_get_options_provider(serverhelper):
    # test if the function returns the correct options for a provider
    options = serverhelper.get_options_provider()
    assert options == {1: "Add attraction", 2: "View attractions", 3: "Update attraction", 4: "Remove attraction", 5: "Logout"}


def test_add_attraction(serverhelper):
    # prepare
    # create a provider (needs to be logged in to add an attraction)
    serverhelper.create_user(name='Clark', type='provider', password='p')
    serverhelper.get_user(name='Clark', type='provider', password='p')  # this will set the user as logged-in in case the user was already created in a previous test run
    
    # delete the attraction if it already exists
    attraction = serverhelper.get_attraction(name='Kimsy', destination='Tokio')
    if attraction != "Attraction not found!":
        serverhelper.remove_attraction(attraction)

    session = serverhelper.start_session()
    # test if the function adds an attraction
    answer = serverhelper.add_attraction(name='Kimsy', description='Ramen Restaurant', destination='Tokio', attraction_type='Restaurant', price_range='5-10', contact='kims.ramen@gmail.com', special_offer='special offers for students')
    attraction = serverhelper.get_attraction(name='Kimsy', destination='Tokio')
    
    # Merge the objects into the session
    answer = session.merge(answer)
    attraction = session.merge(attraction)
    assert answer.name == attraction.name

    # test if the function returns None if the attraction already exists
    answer = serverhelper.add_attraction(name='Kimsy', description='Ramen Restaurant', destination='Tokio', attraction_type='Restaurant', price_range='5-10', contact='kims.ramen@gmail.com', special_offer='special offers for students')
    assert answer == None
    session.close()


def test_get_id(serverhelper):
    # test if the function returns the correct id
    # prepare (Clark logged in)
    session = serverhelper.start_session()
    user = session.query(User).filter(User.name == 'Clark').first()  # get the user from the database, so we can perform tests
    
    # test
    id = serverhelper.get_id()
    assert id == user.id
    session.close()


def test_update_attraction(serverhelper):
    # prepare (Clark logged in)
    session = serverhelper.start_session()
    session.query(User).filter(User.name == 'Clark').first()  # get the user from the database, so we can perform tests
    attraction = serverhelper.get_attraction(name='Kimsy', destination='Tokio')  # attraction added in a previous test
    attraction = session.merge(attraction)
    
    # making sure the attraction is in database and not updated
    assert attraction.description != 'New description'

    # testing only the description, since the function takes the whole object (therefore it's the same for all attributes)
    updated_attraction = attraction
    updated_attraction.description = 'New description'

    # test if the function updates the attraction
    answer = serverhelper.update_attraction(updated_attraction)
    assert answer == "Attraction updated!"

    # check if the attraction is updated in the database
    attraction = serverhelper.get_attraction(name='Kimsy', destination='Tokio')
    assert attraction.description == 'New description'
    session.close()


def test_remove_attraction(serverhelper):
    # prepare (Clark logged in)
    session = serverhelper.start_session()
    session.query(User).filter(User.name == 'Clark').first()  # get the user from the database, so we can perform tests
    # create an attraction to remove 
    serverhelper.add_attraction(name='Sweet and Spicy', description='quick and delicious', destination='Tokio', attraction_type='Restaurant', price_range='5-10', contact='sweet.spicy@gmail.com', special_offer='-')
    attraction = serverhelper.get_attraction(name='Sweet and Spicy', destination='Tokio')  # get the attraction from the database if already created

    # making sure the attraction is in database
    assert attraction != "Attraction not found!"

    # test if the function removes the attraction
    answer = serverhelper.remove_attraction(attraction)
    assert answer == None

    # check if the attraction is removed from the database
    attraction = serverhelper.get_attraction(name='Sweet and Spicy', destination='Tokio')
    assert attraction == "Attraction not found!"
    session.close()


def test_get_attractions(serverhelper):
    # test if the function returns only the attractions added by the provider
    # prepare (Clark logged in)
    session = serverhelper.start_session()
    attractions = session.query(Attraction).all()
    attractions_database = [attraction.name for attraction in attractions if attraction.provider_id == serverhelper.get_id()]
   
    # test
    attractions_function = serverhelper.get_attractions()
    for attraction in attractions_database:
        assert attraction in attractions_function

    # test if the function returns "No attractions found!" if the provider has not added any attractions
    # create a new provider to insure there are no attractions
    serverhelper.create_user(name='Laura', type='provider', password='word1234')
    serverhelper.get_user(name='Laura', type='provider', password='word1234')  # this will set the user as logged-in in case the user was already created in a previous test run
    attractions = serverhelper.get_attractions()
    assert attractions == "No attractions found!"
    session.close()
    