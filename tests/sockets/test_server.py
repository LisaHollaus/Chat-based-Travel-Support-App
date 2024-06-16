from src.sockets.server import *
from sqlalchemy.orm import Session
import pytest
from unittest.mock import patch, Mock, MagicMock  # for replacing socket connection with a function that returns a value
import socket
from tests.fixtures import serverhelper
from src.model.tables import User
from src.model.tables import *


def test_start_server():
    # test if the server is started
    with patch('socket.socket') as socket:
        s = start_server()
        assert s == socket.return_value
        s.close()


# Using the mock socket to test the socket connection based functions
# It simulates the client's input

@patch('socket.socket', new_callable=Mock)  # mock socket.socket
def test_login_new_user(mock_socket, serverhelper):
    # prepare
    # delete the user from the database if he exists already
    session = serverhelper.start_session()
    # delete test user if he already exists
    delete_user = session.query(User).filter(User.name == 'Bob', User.type == 'provider', User.password == 'Bobs_password').first()
    if delete_user:  # if the user exists, delete him
        session.delete(delete_user)
        session.commit()
    session.close()

    # Set up the mock socket's recv method to return the values that the login function expects
    mock_socket.recv.side_effect = [
        "provider".encode(),  # user type
        "yes".encode(),  # new user
        "Bob".encode(),  # username
        "Bobs_password".encode()  # password
    ]

    # Call the login function with the mock socket
    user_type = login(mock_socket, ("localhost", 9000))

    # Check that the login function returned the correct user type
    assert user_type == "provider"

    # Check that the mock socket's send method was called with the correct arguments
    mock_socket.send.assert_any_call("\nWelcome Bob!".encode())


@patch('socket.socket', new_callable=Mock)  # mock socket.socket
def test_login(mock_socket):
    # Set up the mock socket's recv method to return the values that the login function expects
    mock_socket.recv.side_effect = [
        "provider".encode(),  # user type
        "no".encode(),  # new user
        "Alex".encode(),  # username
        "my_password".encode()  # password
    ]

    # Call the login function with the mock socket
    user_type = login(mock_socket, ("localhost", 9000))

    # Check that the login function returned the correct user type
    assert user_type == "provider"

    # Check that the mock socket's send method was called with the correct arguments
    mock_socket.send.assert_any_call("\nWelcome back Alex!".encode())


## provider loop:
# 1. decision to add attraction
@patch('src.sockets.server.ServerHelper')  # mock ServerHelper class, to check if the add_attraction method is called
@patch('socket.socket', new_callable=MagicMock)  # mock socket.socket
def test_provider_loop_add_attraction(mock_socket, mock_server_helper): # mock the provider_loop function, to check if it is called and to avoid an infinite loop
    # Set up the mock socket's recv method to return the values that the provider_loop function expects
    mock_socket.recv.side_effect = [
        "1".encode(),  # decision
        "Puzzles".encode(),  # name
        "New York".encode(),  # destination
        "Bar".encode(),  # type
        "5-10".encode(),  # price
        "A typical Bar, with lot's of different drinks".encode(),  # description
        "puzzles.com".encode(),  # contact
        "2 for 1 Cocktails on Mondays!".encode(),  # special_offer
        "5".encode()  # log-out
    ]

    # Set up the mock ServerHelper's add_attraction method to return a truth value,
    mock_server_helper.get_instance().add_attraction.return_value = True

    # Set up the mock ServerHelper's get_options_provider method to return a value that can be serialized to JSON
    mock_server_helper.get_instance().get_options_provider.return_value = {"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}

    # Call the provider_loop function with the mock socket
    provider_loop(mock_socket)

    # Check that the add_attraction method was called with the correct arguments
    mock_server_helper.get_instance().add_attraction.assert_called_once_with(
        "Puzzles", "New York", "Bar", "5-10", "A typical Bar, with lot's of different drinks", "puzzles.com", "2 for 1 Cocktails on Mondays!"
    )

    # Check that the send method of the mock socket was called with the correct argument
    mock_socket.send.assert_any_call("Attraction added!".encode())

# 2. decision to view attractions
@patch('src.sockets.server.ServerHelper') # mock ServerHelper class, to check if the get_attractions method is called
@patch('socket.socket', new_callable=MagicMock) # using a MagicMock to avoid an infinite loop
def test_provider_loop_view_attractions(mock_socket, mock_server_helper):
    # Set up the mock socket's recv method to return the values that the provider_loop function expects
    mock_socket.recv.side_effect = [
        "2".encode(),  # decision
        "yes".encode(),  # answer to "Would you like to see details of any attraction? (yes/no)"
        "Puzzles".encode(),  # name
        "New York".encode(),  # destination
        "no".encode(),  # answer to "Would you like to see details of any attraction? (yes/no)"
        "5".encode()  # log-out
    ]

    # Set up the mock ServerHelper's get_attractions method to return a string of attractions
    mock_server_helper.get_instance().get_attractions.return_value = "Attraction1, Attraction2, Attraction3" # return a string of attractions (for example)

    # Set up the mock ServerHelper's get_options_provider method to return a value that can be serialized to JSON
    mock_server_helper.get_instance().get_options_provider.return_value = {"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}

    # Call the provider_loop function with the mock socket
    provider_loop(mock_socket)

    # Check that the get_attractions method was called
    mock_server_helper.get_instance().get_attractions.assert_called_once()

    # Check that the view_attraction_details_loop method was called with the correct argument
    mock_server_helper.get_instance().view_attraction_details_loop.assert_called_once_with(mock_socket)

    # Check that the send method of the mock socket was called with the correct argument
    mock_socket.send.assert_any_call("Attraction1, Attraction2, Attraction3".encode())


# 3. decision to update attraction
@patch('src.sockets.server.ServerHelper')  # mock ServerHelper class, to check if the update_attraction method is called
@patch('socket.socket', new_callable=MagicMock) # using a MagicMock to avoid an infinite loop
def test_provider_loop_update_attraction(mock_socket, mock_server_helper):
    # Set up the mock socket's recv method to return the values that the provider_loop function expects
    mock_socket.recv.side_effect = [
        "3".encode(),  # decision
        "Puzzles".encode(),  # name
        "New York".encode(),  # destination
        "-".encode(),  # new contact
        "-".encode(),  # new price
        "-".encode(),  # new description
        "Updated!".encode(),  # new special_offer
        "5".encode()  # log-out
    ]

    # Create a mock Attraction object with a provider_id attribute
    mock_attraction = MagicMock()
    mock_attraction.provider_id = 1  # replace 1 with the id of the current user

    # Set up the mock ServerHelper's get_attraction method to return the mock Attraction object
    mock_server_helper.get_instance().get_attraction.return_value = mock_attraction

    # Set up the mock ServerHelper's get_id method to return the id of the current user
    mock_server_helper.get_instance().get_id.return_value = 1  # replace 1 with the id of the current user

    # Set up the mock ServerHelper's update_attraction method to return a string
    mock_server_helper.get_instance().update_attraction.return_value = "Attraction updated!"

    # Set up the mock ServerHelper's get_options_provider method to return a value that can be serialized to JSON
    mock_server_helper.get_instance().get_options_provider.return_value = {"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}

    # Call the provider_loop function with the mock socket
    provider_loop(mock_socket)

    # Check that the update_attraction method was called with the correct arguments
    mock_server_helper.get_instance().update_attraction.assert_called_once_with(mock_attraction)  # mock_attraction is the attraction that was returned by the get_attraction method


# 4. decision to remove attraction
@patch('src.sockets.server.ServerHelper')  # mock ServerHelper class, to check if the remove_attraction method is called
@patch('socket.socket', new_callable=MagicMock)  # using a MagicMock to avoid an infinite loop
def test_provider_loop_remove_attraction(mock_socket, mock_server_helper, serverhelper):
    # prepare
    # adding a new attraction to the database to test the remove_attraction method
    serverhelper.add_attraction(name="Prinz", destination="New York", attraction_type="Restaurant", price_range="15-20", description="Burger Restaurant", contact="prinz.com", special_offer="Free drink to every menu on Tuesdays!")

    # Set up the mock socket's recv method to return the values that the provider_loop function expects
    mock_socket.recv.side_effect = [
        "4".encode(),  # decision
        "Prinz".encode(),  # name
        "New York".encode(),  # destination
        "5".encode()  # log-out
    ]

    # Create a mock Attraction object with a provider_id attribute
    mock_attraction = MagicMock()
    mock_attraction.provider_id = 1 # replace 1 with the id of the current user for testing

    # Set up the mock ServerHelper's get_attraction method to return the mock Attraction object
    mock_server_helper.get_instance().get_attraction.return_value = mock_attraction

    # Set up the mock ServerHelper's get_id method to return the id of the current user
    mock_server_helper.get_instance().get_id.return_value = 1

    # Set up the mock ServerHelper's remove_attraction method to return a string
    mock_server_helper.get_instance().remove_attraction.return_value = "Attraction removed!"

    # Set up the mock ServerHelper's get_options_provider method to return a value that can be serialized to JSON
    mock_server_helper.get_instance().get_options_provider.return_value = {"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}

    # Call the provider_loop function with the mock socket
    provider_loop(mock_socket)

    # Check that the remove_attraction method was called with the correct arguments
    mock_server_helper.get_instance().remove_attraction.assert_called_once_with(mock_attraction) # mock_attraction is the attraction that was returned by the get_attraction method

    # Check that the send method of the mock socket was called with the correct argument
    mock_socket.send.assert_any_call("Attraction removed!".encode())


# 5. decision to log-out
@patch('socket.socket', new_callable=MagicMock) # using a MagicMock to avoid an infinite loop
def test_provider_loop_logout(mock_socket):
    # Set up the mock socket's recv method to return the values that the provider_loop function expects
    mock_socket.recv.side_effect = [
        "5".encode()  # decision
    ]

    # Call the provider_loop function with the mock socket
    provider_loop(mock_socket)

    # Check that the recv method of the mock socket was called only once (to get the decision and exit the loop)
    assert mock_socket.recv.call_count == 1


## traveller loop:
# 1. decision to explore attractions
@patch('src.sockets.server.ServerHelper')  # mock ServerHelper class
@patch('socket.socket', new_callable=MagicMock) # using a MagicMock to avoid an infinite loop
def test_traveller_loop_explore_attractions(mock_socket, mock_server_helper):
    # Create a mock user object to simulate a logged-in user as a traveller
    mock_user = MagicMock()
    mock_user.name = "Andi"
    mock_user.password = "saver"
    mock_user.type = "traveller"

    # Set up the mock ServerHelper's create_user and get_user methods to return the mock user
    mock_server_helper.get_instance().create_user.return_value = mock_user
    mock_server_helper.get_instance().get_user.return_value = mock_user


    # Set up the mock socket's recv method to return the values that the traveller_loop function expects
    mock_socket.recv.side_effect = [
        "1".encode(),  # decision
        "Tokio".encode(),  # destination decision
        "yes".encode(),  # answer to "Would you like to see details of any attraction? (yes/no)"
        "Kimsy".encode(),  # name of the attraction
        "yes".encode(),  # answer to "Would you like to add this attraction to your favorites list? (yes/no)"
        "no".encode(),  # answer to "Would you like to see details of any attraction? (yes/no)"
        "6".encode()  # log-out
    ]

    # Set up the mock ServerHelper's methods to return expected values
    #mock_server_helper.get_instance
    mock_server_helper.get_instance().get_attractions_by_desetination.return_value = "Attraction1, Attraction2, Attraction3"
    mock_server_helper.get_instance().get_attraction.return_value = "Attraction details"
    mock_server_helper.get_instance().get_options_traveller.return_value = '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'
    mock_server_helper.get_instance().view_attraction_details_loop = MagicMock()

    # Call the traveller_loop function with the mock socket
    traveller_loop(mock_socket)

    # Check that the methods were called with the correct arguments
    mock_server_helper.get_instance().get_attractions.assert_called_once()
    mock_server_helper.get_instance().view_attraction_details_loop.assert_called_once_with(mock_socket)
    mock_socket.send.assert_any_call("Attraction1, Attraction2, Attraction3".encode())
    mock_socket.send.assert_any_call("Attraction added to favorites!".encode())

