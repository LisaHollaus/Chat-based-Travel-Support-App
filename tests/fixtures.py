import pytest
from sqlalchemy import create_engine
from src.model.clienthelper import ClientHelper
from src.model.serverhelper import ServerHelper
from unittest.mock import patch
from src.sockets.client import connect
from src.sockets.server import start_server

# create a singleton instance of the ClientHelper class
@pytest.fixture
def clienthelper(): 
    instance = ClientHelper.get_instance()
    yield instance 


# create a singleton instance of the ServerHelper class
@pytest.fixture
def serverhelper():
    instance = ServerHelper.get_instance()
    yield instance


@pytest.fixture
def socket_connection():
    with patch('socket.socket') as socket:  # mock socket.socket
        s = connect()
        yield s  # provide the connection
        s.close()  # cleanup after test


@pytest.fixture
def server_connection():
    s = start_server()
    yield s
    s.close()

 #   with patch('socket.socket') as socket:
  #      s = start_server()
   #     yield s
    #    s.close()

    # to handle multiple clients
   # while True:
    #    conn, addr = s.accept()  # this waits for a client to connect
     #   thread = threading.Thread(target=handle_client, args=(conn, addr))  # create a new thread
      #  thread.start()  # start the thread

# @pytest.fixture
# def engine():
#     engine = create_engine('sqlite:///./travel_app.db')
#     yield engine
#     engine.dispose()




