import socket
import threading
import json

from model.agency import Agency

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
s.bind(("localhost", 9000))  # bind to an IP + port

s.listen()  # listen for incoming connections

def handle_client(conn, addr): # delegates the conversation of clients
    print(f"new connection from {addr}")
    
    # "welcome to the App! \nAre you a traveller or a provider?"
    type = conn.recv(4096)
    while type.decode().lower() != "provider" and type.decode().lower() != "traveller":
        type = conn.recv(4096)
    

    # login or register
    while True:
        msg = conn.recv(4096) 
        # create a new user:
        if msg.decode().lower() == "yes": 
            name = conn.recv(4096)
            password = conn.recv(4096)
            # if no input:
            if name.decode() == "-" or password.decode() == "-": 
                conn.send("please enter a username and password".encode())
                continue
            
            # create a new user with type & password if not jet existing
            user = Agency.get_instance().create_user(name.decode(), type.decode().lower(), password.decode())
            if user is None:
                conn.send("user already exists".encode())
                continue
            print(f"user: {name.decode()} logged in")
            msg = f"\nWelcome {name.decode()}!"
            conn.send(msg.encode())
            break

        # if user already exists: 
        elif msg.decode().lower() == "no": 
            name = conn.recv(4096)
            password = conn.recv(4096)
            if name.decode() == "-" or password.decode() == "-":
                conn.send("please enter a username and password".encode())
                continue

            # check if the user and password is existing
            user = Agency.get_instance().get_user(name.decode(), password.decode())
            if user is None:
                conn.send("user not found".encode())
                continue
            print(f"user: {name.decode()} logged in")
            welcome = f"\nWelcome back {name.decode()}!"
            conn.send(welcome.encode())
            break

    


    # while logged in as traveller:
    if type.decode() == "traveller":
        while True:
            destinations = Agency.get_instance().get_destinations()
            destinations_str = ",".join(destinations)  # convert the list to a string
            conn.send(destinations_str).encode()
            destination = conn.recv(4096)
            options = Agency.get_instance().get_options_traveller(destination.decode())
            options_str = ",".join(options)  # convert the list to a string
            conn.send(options_str).encode()
    

    # while logged in as provider:
    elif type.decode() == "provider":
        options = Agency.get_instance().get_options_provider()
        options_str = json.dumps(options)  # convert the dictionary to a JSON string
        conn.send(options_str.encode())
        
        while True:
            decission = conn.recv(4096)

            # add a new attraction
            if decission.decode() == "1": 
                name = conn.recv(4096)
                destination = conn.recv(4096)
                type = conn.recv(4096)
                price = conn.recv(4096)
                description = conn.recv(4096)
                address = conn.recv(4096)
                special_offer = conn.recv(4096)
                
                # check if name and destination were entered:
                if name.decode() == "-" or destination.decode() == "-":
                    conn.send("Please try again and don't forget to add at least a name and a destination!".encode())
                    continue

                # add the attraction
                attraction = Agency.get_instance().add_attraction(name.decode(), destination.decode(), type.decode(), price.decode(), description.decode(), address.decode(), special_offer.decode())
                if attraction:
                    conn.send("Attraction added!".encode())
                else:
                    msg = f"A attraction with the name '{attraction.decode()}' already exists in {destination.decode()}!"
                    conn.send(msg.encode())
            
            
            # view attractions
            elif decission.decode() == "2": 
                attractions = Agency.get_instance().get_attractions()
                attractions_str = ",".join(attractions) # convert the list to a string
                conn.send(attractions_str.encode())
                # "Would you like to see details of any attraction? (yes/no)"
                answer = conn.recv(4096).decode() 

                while True:
                    if answer.lower() == "yes":
                        name = conn.recv(4096)
                        destination = conn.recv(4096)
                        attraction = Agency.get_instance().get_attraction(name.decode(), destination.decode())
                        if attraction == "Attraction not found!":
                            conn.send(attraction.encode())
                        else: 
                            attraction_details = Agency.get_instance().get_attraction_details(attraction) 
                            conn.send(attraction_details.encode())
                        
                        # "Would you like to see details of another attraction? (yes/no)"
                        answer = conn.recv(4096).decode()
                        if answer.lower() == "no":
                            break

                    elif answer.lower() == "no":
                        break


            
            # update attraction
            elif decission.decode() == "3": 
                # get attraction
                # "What is the name of the attraction would you like to update? "
                name = conn.recv(4096)
                # "What is the destination of the attraction you would like to update? "
                destination = conn.recv(4096)
                attraction = Agency.get_instance().get_attraction(name.decode(), destination.decode())
                
                if attraction == "Attraction not found!":
                    conn.send(attraction.encode()) # "Attraction not found!"
                    continue
                
                # provider can only update his own attractions
                current_user_id = Agency.get_instance().get_id()
                if current_user_id != attraction.provider_id:
                    conn.send("Attraction belongs to another provider!".encode())
                    continue


                contact = f"Your current contact information: {attraction.contact}\nPlease enter the new contact information or 'skip' for no change: "
                conn.send(contact.encode())
                new_contact = conn.recv(4096)
                if new_contact.decode().lower() != "skip":
                    attraction.contact = new_contact.decode()

                price = f"Your current price range: {attraction.price_range}\nPlease enter the new price range or 'skip' for no change: "
                conn.send(price.encode())
                new_price = conn.recv(4096)
                if new_price.decode().lower() != "skip":
                    attraction.price_range = new_price.decode()

                description = f"Your current description: {attraction.description}\nPlease enter the new description or 'skip' for no change: "
                conn.send(description.encode())
                new_description = conn.recv(4096)
                if new_description.decode().lower() != "skip":
                    attraction.description = new_description.decode()

                special_offer = f"Your current special offer: {attraction.special_offer}\nPlease enter the new special offer or 'skip' for no change: "
                conn.send(special_offer.encode())
                new_special_offer = conn.recv(4096)
                if new_special_offer.decode().lower() != "skip":
                    attraction.special_offer = new_special_offer.decode()
                
                update = Agency.get_instance().update_attraction(attraction)
                conn.send(update.encode()) # "Attraction updated!" or "A attraction with the name {name} already at the destination {destination}!"


            # remove attraction
            elif decission.decode() == "4": 
                name = conn.recv(4096)
                conn.send("What is the destination of the attraction you would like to remove? ".encode())
                destination = conn.recv(4096)
                
                #### not really needed as the user can only remove his own attractions
                # check if the name and destination were entered
                #if name.decode() == "-" or destination.decode() == "-":
                 #   conn.send("Please try again and don't forget to add a name and a destination!".encode())
                  #  continue
                
                # check if the attraction exists 
                attraction = Agency.get_instance().get_attraction(name.decode(), destination.decode())
                if attraction == "Attraction not found!":
                    conn.send(attraction.encode())
                    continue
            
                
                # remove the attraction
                conformation = Agency.get_instance().remove_attraction(attraction)
                if conformation:
                    conn.send(attraction.encode())  # "Attraction belongs to another provider!"
                else: # if the attraction was removed successfully (conformation == None)
                    conn.send("Attraction removed!".encode()) # sends none if removed           


            








    
    # conn.close()  # leaving the conversation open for other clients to connect


# to handle multiple clients
while True:
    conn, addr = s.accept()  # this waits for a client to connect
    thread = threading.Thread(target=handle_client, args=(conn, addr))  # create a new thread
    thread.start()  # start the thread