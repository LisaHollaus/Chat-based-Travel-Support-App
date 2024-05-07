import socket
import threading

from model.agency import Agency

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
s.bind(("localhost", 9000))  # bind to an IP + port

s.listen()  # listen for incoming connections

def handle_client(conn, addr): # delegates the conversation of clients
    print(f"new connection from {addr}")
    conn.send("welcome to the App!".encode()) 
    
    
    # login or register
    while True:
        msg = conn.recv(4096)  # receive a answer from the client
        if msg.decode().lower() == "yes": 
            conn.send("Are you a provider or a traveller? ".encode())
            type = conn.recv(4096)
            if type.decode().lower() != "provider" and type.decode().lower() != "traveller":
                continue

            conn.send("please enter your username: ".encode())
            name = conn.recv(4096)
            conn.send("please enter you new password: ".encode())
            password = conn.recv(4096)

            ### create a new user with type & password if not jet existing
            user = Agency.get_instance().create_user(name.decode(), type.decode(), password.decode())
            if user is None:
                conn.send("user already exists".encode())
                continue
            print(f"user: {name.decode()} logged in")
            msg = f"welcome {name.decode()}!"
            conn.send(msg.encode())
            break
            
        elif msg.decode().lower() == "no": 
            conn.send("please enter your username: ".encode())
            name = conn.recv(4096)
            conn.send("please enter your password: ".encode())
            password = conn.recv(4096)

            # check if the user and password is existing
            user = Agency.get_instance().get_user(name.decode(), password.decode())
            if user is None:
                conn.send("user not found".encode())
                continue
            print(f"user: {name.decode()} logged in")
            welcome = f"welcome back {name.decode()}!"
            conn.send(welcome.encode())
            break

    type = Agency.get_instance().loged_in_user.type

    # while logged in as traveller:
    if type == "traveller":
        while True:
            destinations = Agency.get_instance().get_destinations()
            conn.send(destinations.encode())
            destination = conn.recv(4096)
            options = Agency.get_instance().get_options_traveller(destination.decode())
            conn.send(options.encode())
    
    # while logged in as provider:
    elif type == "provider":
        while True:
            options = Agency.get_instance().get_options_provider()
            conn.send(options.encode())
            decission = conn.recv(4096)

            # add a new attraction
            if decission.decode() == "1": 
                conn.send("Name of the attraction: ".encode())
                attraction = conn.recv(4096)
                conn.send("Destination (e.g. Vienna): ".encode())
                destination = conn.recv(4096)
                conn.send("Type of the attraction (e.g. Restaurant): ".encode())
                type = conn.recv(4096)
                conn.send("Price range: ".encode())
                price = conn.recv(4096)
                conn.send("Description of the attraction: ".encode())
                description = conn.recv(4096)
                conn.send("Contact information (e.g. addresse, email, website,..): ".encode())
                address = conn.recv(4096)
                conn.send("Special offers: ".encode())
                special_offer = conn.recv(4096)
                # add the attraction
                attraction = Agency.get_instance().add_attraction(attraction.decode(), destination.decode(), type.decode(), price.decode(), description.decode(), address.decode(), special_offer.decode())
                return attraction # return the attraction (none if not added)

            
            
            # remove attraction
            elif decission.decode() == "2": 
                pass
            elif decission.decode() == "3": # update attraction
                pass
            elif decission.decode() == "4": # view attractions
                pass 






    
    # conn.close()  # leaving the conversation open for other clients to connect


# to handle multiple clients
while True:
    conn, addr = s.accept()  # this waits for a client to connect
    thread = threading.Thread(target=handle_client, args=(conn, addr))  # create a new thread
    thread.start()  # start the thread