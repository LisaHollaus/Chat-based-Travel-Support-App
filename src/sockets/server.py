import socket
import threading
import json
from src.model.serverhelper import ServerHelper


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
    s.bind(("localhost", 9000))  # bind to an IP + port
    s.listen()  # listen for incoming connections
    return s


# main structure how to handle the conversation with the clients
def handle_client(conn, addr):  # delegates the conversation of clients
    type = login(conn, addr)
    if type == "traveller":
        traveller_loop(conn)
    else:  # type == "provider"
        provider_loop(conn)
    # conn.close()  # leaving the conversation open for other clients to connect


def login(conn, addr):
    print(f"new connection from {addr}")
    
    # "welcome to the App! \nAre you a traveller or a provider?"
    type = conn.recv(4096).decode().lower()
    while type != "provider" and type != "traveller":
        type = conn.recv(4096).decode().lower()
    
    # login or register
    while True:
        # "Are you a new user? (yes/no)"
        msg = conn.recv(4096)

        # create a new user:
        if msg.decode().lower() == "yes": 
            name = conn.recv(4096).decode()
            password = conn.recv(4096).decode()
            # if no input:
            if name == "-" or password == "-": 
                conn.send("please enter a username and password".encode())
                continue
            
            # create a new user with type & password if not jet existing
            user = ServerHelper.get_instance().create_user(name, type, password)
            if user == "user already exists":
                conn.send(user.encode())
                continue
            print(f"user: {name} logged in")
            msg = f"\nWelcome {name}!"
            conn.send(msg.encode())
            break

        # if user already exists: 
        elif msg.decode().lower() == "no": 
            name = conn.recv(4096).decode()
            password = conn.recv(4096).decode()
            if name == "-" or password == "-":
                conn.send("please enter a username and password".encode())
                continue

            # check if the user and password to the give type is existing
            user = ServerHelper.get_instance().get_user(name, password, type)
            if user is None:
                conn.send("user not found".encode())
                continue
            print(f"user: {name} logged in")
            welcome = f"\nWelcome back {name}!"
            conn.send(welcome.encode())
            break
    return type


# while logged in as traveller:
def traveller_loop(conn):

    # get the options for the traveller
    options = ServerHelper.get_instance().get_options_traveller()
    options_str = json.dumps(options)  # convert the dictionary to a JSON string
    conn.send(options_str.encode())

    while True:
        decision = conn.recv(4096).decode()

        # get destinations
        if decision == "1":
            # get all destinations
            destinations_str = ServerHelper.get_instance().get_destinations()
            conn.send(destinations_str.encode())
            destination = conn.recv(4096).decode()

            # get all attractions of the desired destination
            attractions_str = ServerHelper.get_instance().get_attractions_by_destination(destination)
            conn.send(attractions_str.encode())  # "No attractions found!" or list of attractions as a string separated by commas
            if attractions_str == "No attractions found!":
                continue

            # "Would you like to see details of any of these attractions? (yes/no)"
            answer = conn.recv(4096).decode()
            if answer.lower() == "yes":
                #ServerHelper.get_instance().view_attraction_details_loop(traveller=True, conn) # we don't use this function here because we don't need to ask for the destination as well
                while True:
                    name = conn.recv(4096).decode()
                    attraction = ServerHelper.get_instance().get_attraction(name, destination)
                    
                    if attraction == "Attraction not found!":
                        conn.send(attraction.encode())
                    else: 
                        attraction_details = ServerHelper.get_instance().get_attraction_details(attraction) 
                        conn.send(attraction_details.encode())
                        favourite = conn.recv(4096).decode() # "Would you like to add this attraction to your favourites? (yes/no)"
                        if favourite.lower() == "yes":
                            added = ServerHelper.get_instance().add_to_favourites(attraction)
                            conn.send(added.encode()) # "Attraction added to favourites!" or "Attraction already in favourites!"
                        else:
                            conn.send(" ".encode())
                        
                    # "Would you like to see details of another attraction? (yes/no)"
                    answer = conn.recv(4096).decode()
                    if answer.lower() == "no":
                        break
            
        # get details of a specific attraction
        elif decision == "2":
            ServerHelper.get_instance().view_attraction_details_loop(conn, traveller=True)

        # see favorite attractions
        elif decision == "3":
            favourites = ServerHelper.get_instance().get_favourites()
            favourites_str = ",".join(favourites)
            conn.send(favourites_str.encode())
            # "Would you like to see details of any attraction? (yes/no)"
            answer = conn.recv(4096).decode()
            if answer.lower() == "yes":
                ServerHelper.get_instance().view_attraction_details_loop(conn, traveller=True)

        # rate an attraction
        elif decision == "4":
            name = conn.recv(4096).decode()
            destination = conn.recv(4096).decode()

            attraction = ServerHelper.get_instance().get_attraction(name, destination)
            if attraction == "Attraction not found!":
                conn.send(f"Attraction {name} in {destination} not found!".encode())
                continue
                
            check = ServerHelper.get_instance().check_if_rated(attraction)
            if check: # true if the attraction was already rated (in visited attractions)
                conn.send("You already rated this attraction!".encode())
                continue
            else: 
                conn.send("Attraction found".encode())

            # get rating and review
            rating = conn.recv(4096).decode()
            rated = ServerHelper.get_instance().rate_attraction(attraction, rating)
            conn.send(rated.encode()) # "Attraction rated! Thank you for your feedback!"	

        # history of visited attractions
        elif decision == "5":
            visited = ServerHelper.get_instance().get_visited_attractions()
            visited_str = ",".join(visited)
            conn.send(visited_str.encode())

            # "Would you like to see details of any attraction? (yes/no)"
            answer = conn.recv(4096).decode()
            if answer.lower() == "yes":
                ServerHelper.get_instance().view_attraction_details_loop(conn, traveller=True)

        # logout
        elif decision == "6":
            break

# while logged in as provider:
def provider_loop(conn):
    options = ServerHelper.get_instance().get_options_provider()
    options_str = json.dumps(options)  # convert the dictionary to a JSON string
    conn.send(options_str.encode())
    
    while True:
        decision = conn.recv(4096).decode()

        # add a new attraction
        if decision == "1":
            name = conn.recv(4096).decode()
            destination = conn.recv(4096).decode()
            type = conn.recv(4096).decode()
            price = conn.recv(4096).decode()
            description = conn.recv(4096).decode()
            contact = conn.recv(4096).decode()
            special_offer = conn.recv(4096).decode()
            
            # check if name and destination were entered:
            if name == "-" or destination == "-":
                conn.send("Please try again and don't forget to add at least a name and a destination!".encode())
                continue

            # add the attraction
            attraction = ServerHelper.get_instance().add_attraction(name, destination, type, price, description, contact, special_offer)
            if attraction:
                conn.send("Attraction added!".encode())
            else:
                msg = f"A attraction with the name '{name}' already exists in {destination}!"
                conn.send(msg.encode())

        # view attractions
        elif decision == "2":
            attractions_str = ServerHelper.get_instance().get_attractions()
            conn.send(attractions_str.encode())
            
            # "Would you like to see details of any attraction? (yes/no)"
            answer = conn.recv(4096).decode() 
            if answer.lower() == "yes":
                ServerHelper.get_instance().view_attraction_details_loop(conn) # get attraction details of one or more attractions and print them

        # update attraction
        elif decision == "3":
            # get attraction
            # "What is the name of the attraction would you like to update? "
            name = conn.recv(4096).decode()
            # "What is the destination of the attraction you would like to update? "
            destination = conn.recv(4096).decode()
            attraction = ServerHelper.get_instance().get_attraction(name, destination)
            
            if attraction == "Attraction not found!":
                conn.send(attraction.encode()) # "Attraction not found!"
                continue
            
            # provider can only update his own attractions
            current_user_id = ServerHelper.get_instance().get_id()
            if current_user_id != attraction.provider_id:
                conn.send("Attraction belongs to another provider!".encode())
                continue

            # ask for the new values to update the attraction
            contact = f"Your current contact information: {attraction.contact}\nPlease enter the new contact information or press 'enter' for no change: "
            conn.send(contact.encode())
            new_contact = conn.recv(4096).decode()
            if new_contact.lower() != "-":
                attraction.contact = new_contact

            price = f"Your current price range: {attraction.price_range}\nPlease enter the new price range or press 'enter' for no change: "
            conn.send(price.encode())
            new_price = conn.recv(4096).decode()
            if new_price.lower() != "-":
                attraction.price_range = new_price

            description = f"Your current description: {attraction.description}\nPlease enter the new description or press 'enter' for no change: "
            conn.send(description.encode())
            new_description = conn.recv(4096).decode()
            if new_description.lower() != "-":
                attraction.description = new_description

            special_offer = f"Your current special offer: {attraction.special_offer}\nPlease enter the new special offer or press 'enter' for no change: "
            conn.send(special_offer.encode())
            new_special_offer = conn.recv(4096).decode()
            if new_special_offer.lower() != "-":
                attraction.special_offer = new_special_offer
            
            # update the attraction
            update = ServerHelper.get_instance().update_attraction(attraction)
            conn.send(update.encode()) # "Attraction updated!" 

        # remove attraction
        elif decision == "4":
            name = conn.recv(4096).decode()
            destination = conn.recv(4096).decode()
            
            # check if the attraction exists 
            attraction = ServerHelper.get_instance().get_attraction(name, destination)
            if attraction == "Attraction not found!":
                conn.send(attraction.encode())
                continue
            
            # remove the attraction
            conformation = ServerHelper.get_instance().remove_attraction(attraction)
            if conformation:
                conn.send(conformation.encode())  # "Attraction belongs to another provider!"
            else:  # if the attraction was removed successfully (conformation == None)
                conn.send("Attraction removed!".encode()) # sends none if removed           

        # logout 
        elif decision == "5":
            break
    

if __name__ == "__main__":
    s = start_server()
    print("server started")
    print("waiting for connections")

    # to handle multiple clients
    while True:
        conn, addr = s.accept()  # this waits for a client to connect
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # create a new thread
        thread.start()  # start the thread


