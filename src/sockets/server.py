import socket
import threading
import json

from model.agency import Agency

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
    s.bind(("localhost", 9000))  # bind to an IP + port
    s.listen()  # listen for incoming connections
    return s


def handle_client(conn, addr): # delegates the conversation of clients
    print(f"new connection from {addr}")
    
    # "welcome to the App! \nAre you a traveller or a provider?"
    type = conn.recv(4096).decode()
    while type.lower() != "provider" and type.lower() != "traveller":
        type = conn.recv(4096).decode()
    

    # login or register
    while True:
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
            user = Agency.get_instance().create_user(name, type, password)
            if user is None:
                conn.send("user already exists".encode())
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
            user = Agency.get_instance().get_user(name, password, type)
            if user is None:
                conn.send("user not found".encode())
                continue
            print(f"user: {name} logged in")
            welcome = f"\nWelcome back {name}!"
            conn.send(welcome.encode())
            break

    


    # while logged in as traveller:
    if type == "traveller":
        while True:
            # get the options for the traveller
            options = Agency.get_instance().get_options_traveller()
            options_str = json.dumps(options)  # convert the dictionary to a JSON string
            conn.send(options_str.encode())

            while True:
                decission = conn.recv(4096).decode()

                # get destinations
                if decission == "1": 
                    destinations_str = Agency.get_instance().get_destinations()
                    #destinations_str = ",".join(destinations)
                    
                    conn.send(destinations_str.encode())
                    destination = conn.recv(4096).decode()

                    # get all attractions of the desired destination
                    attractions_str = Agency.get_instance().get_attractions_by_destination(destination)
                    #attractions_str = ",".join(attractions)  # convert the list to a string and add it to the message 
                    conn.send(attractions_str.encode())

                    # "Would you like to see details of any attraction? (yes/no)"
                    answer = conn.recv(4096).decode()
                    if answer.lower() == "yes":
                        #view_attraction_details_loop(traveller=True) # we don't use this function here because we don't need to ask for the destination as well
                        while True:
                            name = conn.recv(4096).decode()
        
                            attraction = Agency.get_instance().get_attraction(name, destination)
                            if attraction == "Attraction not found!":
                                conn.send(attraction.encode())
                            else: 
                                attraction_details = Agency.get_instance().get_attraction_details(attraction) 
                                conn.send(attraction_details.encode())
                                favourite = conn.recv(4096).decode() # "Would you like to add this attraction to your favourites? (yes/no)"
                                if favourite.lower() == "yes":
                                    added = Agency.get_instance().add_to_favourites(attraction)
                                    conn.send(added.encode()) # "Attraction added to favourites!" or "Attraction already in favourites!"
                                else:
                                    conn.send("\n".encode())
                            
                            # "Would you like to see details of another attraction? (yes/no)"
                            answer = conn.recv(4096).decode()
                            if answer.lower() == "no":
                                break

                
              

                
                # get details of a specific attraction
                elif decission == "2":
                    view_attraction_details_loop(traveller=True)
                    # while True:
                    #     name = conn.recv(4096).decode()
                    #     destination = conn.recv(4096).decode()
                    #     attraction = Agency.get_instance().get_attraction(name, destination)
                    #     if attraction == "Attraction not found!":
                    #         conn.send(attraction.encode())
                    #     else: 
                    #         attraction_details = Agency.get_instance().get_attraction_details(attraction) 
                    #         conn.send(attraction_details.encode())
                    #         favourite = conn.recv(4096).decode() # "Would you like to add this attraction to your favourites? (yes/no)"
                    #         if favourite.lower() == "yes":
                    #             added = Agency.get_instance().add_to_favourites(attraction)
                    #             conn.send(added.encode()) # "Attraction added to favourites!" or "Attraction already in favourites!"
                    #         else:
                    #             conn.send("\n".encode())
                            
                    #     # "Would you like to see details of another attraction? (yes/no)"
                    #     answer = conn.recv(4096).decode()
                    #     if answer.lower() == "no":
                    #         break
        
                # see favorite attractions
                elif decission == "3":
                    favourites = Agency.get_instance().get_favourites()
                    favourites_str = ",".join(favourites)
                    conn.send(favourites_str.encode())
                    # "Would you like to see details of any attraction? (yes/no)"
                    answer = conn.recv(4096).decode()
                    if answer.lower() == "yes":
                        view_attraction_details_loop(traveller=True)

                # rate an attraction
                elif decission == "4":
                    name = conn.recv(4096).decode()
                    destination = conn.recv(4096).decode()

                    attraction = Agency.get_instance().get_attraction(name, destination)
                    if attraction == "Attraction not found!":
                        conn.send(f"Attraction {name} in {destination} not found!".encode())
                        continue
                    
                    check = Agency.get_instance().check_if_rated(attraction)
                    if check: # true if the attraction was already rated (in visited attractions)
                        conn.send("You already rated this attraction!".encode())
                        continue
                    else: 
                        conn.send("Attraction found".encode())

                    # get rating and review
                    rating = conn.recv(4096).decode()
                    rated = Agency.get_instance().rate_attraction(attraction, rating)
                    conn.send(rated.encode()) # "Attraction rated! Thank you for your feedback!"	


                # history of visited attractions
                elif decission == "5":
                    visited = Agency.get_instance().get_visited_attractions()
                    visited_str = ",".join(visited)
                    conn.send(visited_str.encode())

                    # "Would you like to see details of any attraction? (yes/no)"
                    answer = conn.recv(4096).decode()
                    if answer.lower() == "yes":
                        view_attraction_details_loop(traveller=True)

                # logout
                elif decission == "6":
                    break




        





 # while logged in as provider:
    elif type == "provider":
        options = Agency.get_instance().get_options_provider()
        options_str = json.dumps(options)  # convert the dictionary to a JSON string
        conn.send(options_str.encode())
        
        while True:
            decission = conn.recv(4096).decode()

            # add a new attraction
            if decission == "1": 
                name = conn.recv(4096).decode()
                destination = conn.recv(4096).decode()
                type = conn.recv(4096).decode()
                price = conn.recv(4096).decode()
                description = conn.recv(4096).decode()
                address = conn.recv(4096).decode()
                special_offer = conn.recv(4096).decode()
                
                # check if name and destination were entered:
                if name == "-" or destination == "-":
                    conn.send("Please try again and don't forget to add at least a name and a destination!".encode())
                    continue

                # add the attraction
                attraction = Agency.get_instance().add_attraction(name, destination, type, price, description, address, special_offer)
                if attraction:
                    conn.send("Attraction added!".encode())
                else:
                    msg = f"A attraction with the name '{name}' already exists in {destination}!"
                    conn.send(msg.encode())
            
            
            # view attractions
            elif decission == "2": 
                attractions = Agency.get_instance().get_attractions()
                attractions_str = ",".join(attractions) # convert the list to a string
                conn.send(attractions_str.encode())
                
                # "Would you like to see details of any attraction? (yes/no)"
                answer = conn.recv(4096).decode() 
                if answer.lower() == "yes":
                    view_attraction_details_loop() # get attraction details of one or more attractions and print them

                # while True:
                #     if answer.lower() == "yes":
                #         name = conn.recv(4096)
                #         destination = conn.recv(4096)
                #         attraction = Agency.get_instance().get_attraction(name.decode(), destination.decode())
                #         if attraction == "Attraction not found!":
                #             conn.send(attraction.encode())
                #         else: 
                #             attraction_details = Agency.get_instance().get_attraction_details(attraction) 
                #             conn.send(attraction_details.encode())
                        
                #         # "Would you like to see details of another attraction? (yes/no)"
                #         answer = conn.recv(4096).decode()
                #         if answer.lower() == "no":
                #             break

                #     elif answer.lower() == "no":
                #         break


            
            # update attraction
            elif decission == "3": 
                # get attraction
                # "What is the name of the attraction would you like to update? "
                name = conn.recv(4096).decode()
                # "What is the destination of the attraction you would like to update? "
                destination = conn.recv(4096).decode()
                attraction = Agency.get_instance().get_attraction(name, destination)
                
                if attraction == "Attraction not found!":
                    conn.send(attraction.encode()) # "Attraction not found!"
                    continue
                
                # provider can only update his own attractions
                current_user_id = Agency.get_instance().get_id()
                if current_user_id != attraction.provider_id:
                    conn.send("Attraction belongs to another provider!".encode())
                    continue


                contact = f"Your current contact information: {attraction.contact}\nPlease enter the new contact information or press 'enter' for no change: "
                conn.send(contact.encode())
                #updated_attraction = attraction.copy()
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
                
                update = Agency.get_instance().update_attraction(attraction)
                conn.send(update.encode()) # "Attraction updated!" 


            # remove attraction
            elif decission == "4": 
                name = conn.recv(4096).decode()
                destination = conn.recv(4096).decode()
                
                # check if the attraction exists 
                attraction = Agency.get_instance().get_attraction(name, destination)
                if attraction == "Attraction not found!":
                    conn.send(attraction.encode())
                    continue
            
                
                # remove the attraction
                conformation = Agency.get_instance().remove_attraction(attraction)
                if conformation:
                    conn.send(conformation.encode())  # "Attraction belongs to another provider!"
                else: # if the attraction was removed successfully (conformation == None)
                    conn.send("Attraction removed!".encode()) # sends none if removed           


            #### needed?
            # logout 
            elif decission == "5": 
                break
    
    # conn.close()  # leaving the conversation open for other clients to connect


# def view_attraction_details_loop():
#     while True:
#         #if answer.lower() == "yes":
#         name = conn.recv(4096)
#         destination = conn.recv(4096)
#         attraction = Agency.get_instance().get_attraction(name.decode(), destination.decode())
#         if attraction == "Attraction not found!":
#             conn.send(attraction.encode())
#         else: 
#             attraction_details = Agency.get_instance().get_attraction_details(attraction) 
#             conn.send(attraction_details.encode())
                        
#         # "Would you like to see details of another attraction? (yes/no)"
#         answer = conn.recv(4096).decode()
#         if answer.lower() == "no":
#             break



def view_attraction_details_loop(traveller = False): # traveller is an optional parameter to give the traveller the option to add the attraction to the faviorites list
    while True:
        name = conn.recv(4096).decode()
        destination = conn.recv(4096).decode()
        attraction = Agency.get_instance().get_attraction(name, destination)
        if attraction == "Attraction not found!":
            conn.send(attraction.encode())
        else: 
            attraction_details = Agency.get_instance().get_attraction_details(attraction) 
            conn.send(attraction_details.encode())
            if traveller: # if the user is a traveller
                favourite = conn.recv(4096).decode() # "Would you like to add this attraction to your favourites? (yes/no)"
                if favourite.lower() == "yes":
                    added = Agency.get_instance().add_to_favourites(attraction)
                    conn.send(added.encode()) # "Attraction added to favourites!" or "Attraction already in favourites!"
                else:
                    conn.send(" ".encode()) # send a blank message to keep the conversation going
                            
        # "Would you like to see details of another attraction? (yes/no)"
        answer = conn.recv(4096).decode()
        if answer.lower() == "no":
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


