from unittest.mock import patch, MagicMock
from src.sockets.client import *


def test_connect():
    with patch('socket.socket') as socket:  # mock socket.socket
        s = connect()
        assert s == socket.return_value
        s.close()


# log in new user
# this replaces the input() function with a function that returns 'traveller', 'yes', 'Alice', 'my_password'
@patch('builtins.input', side_effect=['provider', 'yes', 'Alice', 'my_password'])
def test_start_client_new(s):
    type, user = start_client(s)
    assert type == 'provider'
    assert user == 'Alice'


# log in existing user
# this replaces the input() function with a function that returns 'traveller', 'no', 'Alice', 'my_password'
@patch('builtins.input', side_effect=['provider', 'no', 'Alice', 'my_password'])
def test_start_client_existing(s):
    type, user = start_client(s)
    assert type == 'provider'
    assert user == 'Alice'


# try to log in with wrong password
# this replaces the input() function with a function that returns 'traveller', 'no', 'Alice', 'wrong_password'
@patch('builtins.input', side_effect=['provider', 'no', 'Alice', 'wrong_password'])
def test_start_client_wrong_password(s):
    type, user = start_client(s)
    assert type == 'provider'
    assert user == 'Alice'


# creat new user with existing username
# this replaces the input() function with a function that returns 'traveller', 'yes', 'Alice', 'my_password'
# and then 'traveller', 'yes', 'Alice', 'my_password' again to end the loop
@patch('builtins.input', side_effect=['provider', 'yes', 'Alice', 'my_password', 'provider', 'yes', 'Alice', 'my_password'])
def test_start_client_existing_username(s):
    type, user = start_client(s)
    assert type == 'provider'
    assert user == 'Alice'


## provider menu
# 1. decision to add attraction
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '1',  # decision
    'Olli',  # name
    'Miami',  # destination
    'Bar',  # type
    '5-20',  # price range
    'Hidden bar',  # description
    'ollis.com',  # contact
    'Happy hour every day from 8 to 9 pm!',  # special offer
    '5',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_provider_add_attraction(mock_socket, mock_input):
    # Mock the recv method to simulate a server response
    # return a JSON string that represents the menu options
    mock_socket.recv.side_effect = [
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
        'Attraction added!'.encode(),
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
    ]
    # Call the provider function with the mock socket
    provider(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('1'.encode())  # decision
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('Miami'.encode())
    mock_socket.send.assert_any_call('Bar'.encode())
    mock_socket.send.assert_any_call('5-20'.encode())
    mock_socket.send.assert_any_call('Hidden bar'.encode())
    mock_socket.send.assert_any_call('ollis.com'.encode())
    mock_socket.send.assert_any_call('Happy hour every day from 8 to 9 pm!'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 9

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 9


# 2. decision to view attractions
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '2',
    'yes',  # decision to view attraction details
    'Olli',  # name
    'Miami',  # destination
    'NO',  # decision to view another attraction
    '5',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_provider_view_attractions(mock_socket, mock_input):
    # Mock the recv method to return a JSON string that represents the menu options
    mock_socket.recv.side_effect = [
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
        'Attraction1, Attraction2, Attraction3'.encode(),
        'Attraction details'.encode(),
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
    ]
    # Call the provider function with the mock socket
    provider(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('2'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('Miami'.encode())
    mock_socket.send.assert_any_call('yes'.encode())
    mock_socket.send.assert_any_call('NO'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 6

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 6


# 3. decision to update attraction
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '3',  # decision
    'Olli',  # name
    'Miami',  # destination
    'updated',  # contact
    'updated',  # price range
    'updated',  # description
    '-',  # special offer
    '5',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_provider_update_attraction(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
        'Your current contact information: {attraction.contact}\nPlease enter the new contact information or press "enter" for no change: '.encode(),
        'Your current price range: {attraction.price_range}\nPlease enter the new price range or press "enter" for no change: '.encode(),
        'Your current description: {attraction.description}\nPlease enter the new description or press "enter" for no change: '.encode(),
        'Your current special offer: {attraction.special_offer}\nPlease enter the new special offer or press "enter" for no change: '.encode(),
        'Attraction updated!'.encode(),
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
    ]
    # Call the provider function with the mock socket
    provider(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('3'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('Miami'.encode())
    mock_socket.send.assert_any_call('updated'.encode())
    mock_socket.send.assert_any_call('updated'.encode())
    mock_socket.send.assert_any_call('updated'.encode())
    mock_socket.send.assert_any_call('-'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 8

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 8


# 4. decision to remove attraction
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '4',  # decision
    'Olli',  # name
    'Miami',  # destination
    '5',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_provider_remove_attraction(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
        'Attraction removed!'.encode(),
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
    ]
    # Call the provider function with the mock socket
    provider(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('4'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('Miami'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 4

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 4


# 5. decision to log out
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '5',  # decision
])
@patch('socket.socket', new_callable=MagicMock)
def test_provider_logout(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Add attraction", "2": "View attractions", "3": "Update attraction", "4": "Remove attraction", "5": "Logout"}'.encode(),
    ]
    # Call the provider function with the mock socket
    provider(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('5'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 1

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 1


## traveller menu
# 1. decision to explore attractions
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '1',  # decision
    'Miami',  # destination decision
    'yes',  # decision to view attraction details
    'Olli',  # name
    'yes',  # decision to add attraction to favourites
    'no',  # decision to view another attraction
    '6',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_traveller_explore_attractions(mock_socket, mock_input):
    # Mock the recv methode to simulate the menu options, the destinations and the attractions,...
    mock_socket.recv.side_effect = [
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
        'Destination1, Destination2, Destination3'.encode(),
        'Attraction1, Attraction2, Attraction3'.encode(),
        'Attraction details'.encode(),
        'Attraction added to your favorites!'.encode(),
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
    ]

    # Calling the traveller function with the mock socket
    traveller(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('1'.encode())
    mock_socket.send.assert_any_call('Miami'.encode())
    mock_socket.send.assert_any_call('yes'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('yes'.encode())
    mock_socket.send.assert_any_call('no'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 7

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 7


# 2. decision to get details of a specific attraction
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '2',  # decision
    'Olli',  # name
    'Miami',  # destination
    'yes',  # decision to view attraction details
    'no',  # decision to add attraction to favourites
    'no',  # decision to view another attraction
    '6',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_traveller_get_details(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
        'Attraction details'.encode(),
        ''.encode(),  # for not adding the attraction to the favourites
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
    ]
    # Call the traveller function with the mock socket
    traveller(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('2'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('Miami'.encode())
    mock_socket.send.assert_any_call('yes'.encode())
    mock_socket.send.assert_any_call('no'.encode())
    mock_socket.send.assert_any_call('no'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 7

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 6


# 3. decision to see favorite attractions
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '3',  # decision
    'yes',  # decision to view attraction
    'Olli',  # name
    'Miami',  # destination
    'no',  # decision to add attraction to favourites
    'no',  # decision to view another attraction
    '6',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_traveller_see_favourites(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
        'FavAttraction1, FavAttraction2, FavAttraction3'.encode(),
        'Attraction details'.encode(),
        ''.encode(),  # for not adding the attraction to the favourites
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
    ]
    # Call the traveller function with the mock socket
    traveller(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('3'.encode())
    mock_socket.send.assert_any_call('yes'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('no'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 7

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 7


# 4. decision to rate visited attraction
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '4',  # decision
    'Olli',  # name
    'Miami',  # destination
    '5',  # rating
    '6',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_traveller_rate_attraction(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
        'Attraction found'.encode(),  # needed to stay in the loop
        'Attraction rated! Thank you for your feedback!'.encode(),
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
    ]
    # Call the traveller function with the mock socket
    traveller(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('4'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('Miami'.encode())
    mock_socket.send.assert_any_call('5'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 5

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 5


# 5. decision to see history of visited attractions
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '5',  # decision
    'yes',  # decision to view attraction
    'Olli',  # name
    'Miami',  # destination
    'no',  # decision to add attraction to favourites
    'no',  # decision to view another attraction
    '6',  # logout
])
@patch('socket.socket', new_callable=MagicMock)
def test_traveller_see_history(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
        'VisitedAttraction1, VisitedAttraction2, VisitedAttraction3'.encode(),
        'Attraction details'.encode(),
        ''.encode(),  # for not adding the attraction to the favourites
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
    ]
    # Call the traveller function with the mock socket
    traveller(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('5'.encode())
    mock_socket.send.assert_any_call('Olli'.encode())
    mock_socket.send.assert_any_call('no'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 7

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 6


# 6. decision to log out
# using the mock socket to simulate the user response (replacing the input() function)
@patch('builtins.input', side_effect=[
    '6',  # decision
])
@patch('socket.socket', new_callable=MagicMock)
def test_traveller_logout(mock_socket, mock_input):
    # Mock the recv method to simulate the server response
    mock_socket.recv.side_effect = [
        '{"1": "Explore attractions", "2": "Get details of a specific attraction", "3": "See favorite attractions", "4": "Rate visited attraction", "5": "See history of visited attractions", "6": "Logout"}'.encode(),
    ]
    # Call the traveller function with the mock socket
    traveller(mock_socket)

    # Check that the send method was called with the correct arguments
    mock_socket.send.assert_any_call('6'.encode())

    # Check that the input method was called to get the user's decision
    assert mock_input.call_count == 1

    # Check that the print method was called to print the menu options
    assert mock_socket.send.call_count == 1
