import socket
import json
from model.clienthelper import *

def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
    s.connect(("localhost", 9000))  # connect to the server

    print("welcome to the App! \nAre you a traveller or a provider?")
    type = input(">>> ")  # input "traveller" or "provider"
    while type.lower() != "provider" and type.lower() != "traveller":
        print("please enter 'provider' or 'traveller'")
        type = input(">>> ")
    s.send(type.encode())  # send the type to the server


    # login or register
    while True:
        msg = input("Are you new here? (yes/no) \n>>> ")  # input "yes" or "no"
        
        # sending the message to the server only when the user enters "yes" or "no"
        
        # create a new user:
        if msg.lower() == "yes": 
            s.send(msg.encode())  # sends "yes" to the server
            print("please enter your username: ")
            user = input(">>> ") or "-"  # input a username
            s.send(user.encode()) # send the username to the server or "-" if no input
            print("please enter your new password: ")
            password = input(">>> ") or "-"  # input a password
            s.send(password.encode()) 
            welcome = s.recv(4096).decode() # "welcome {username}!" or "user already exists" or "please enter a username and password"
            if welcome != "user already exists" and welcome != "please enter a username and password":
                print(welcome)
                break
            print(welcome) # user already exists
        
        # if user already exists:
        elif msg.lower() == "no":
            s.send(msg.encode())  # send the "no" to the server
            print("please enter your username: ")
            user = input(">>> ") or "-"  # input a username
            s.send(user.encode())
            print("please enter your password: ")
            password = input(">>> ") or "-"  # input a password
            s.send(password.encode())
            welcome = s.recv(4096).decode() # "welcome {username}!" or "user not found" or "please enter a username and password"
            if welcome != "user not found" and welcome != "please enter a username and password":
                print(welcome) # "welcome {username}!"
                break
            print(welcome) # user not found or please enter a username and password

        
        print("\nplease, try again from the start\n")





    # while logged in as traveller:
    if type.lower() == "traveller":
        
        options_str = s.recv(4096).decode()  # receive the options

        while True:
        # listing the decissions of what to do:
            decission = print_menu_get_answer(options_str) # get the user's decission
            s.send(decission.encode())

            # explore attractions
            if decission == "1":
                # find destination
                destinations_str = s.recv(4096).decode()  # receive the destinations
                print("Where would you like to go?")
                print_list(destinations_str) # converts string to a list and print the destinations
                    
                destination = input("Enter a destination or 'everywhere' for a random search \n>>> ") or "-"
                s.send(destination.encode())
                    
                # see attractions
                attractions_str = s.recv(4096).decode()  # receive the attractions or "no attractions found!"
                if attractions_str == "No attractions found!":
                    print(attractions_str)
                    continue
                  
                # "Here's a list of all attractions in {destination}:"
                print_list(attractions_str) # converts string to a list and print the attractions or "No attractions found!"
                  
                    
                # see details of the attractions
                print("\nWould you like to see details of any of these attractions? (yes/no)")
                answer = yes_no_loop() # make sure the user enters "yes" or "no"
                    
                s.send(answer.encode()) # send the answer to the server if it is "yes" or "no"
                    
                if answer.lower() == "yes":
                    #  get_attraction_details_loop(s, traveller=True) # we don't use this function here because we don't need to ask for the destination as well
                    while True:    
                        print("Please enter the name of the attraction you would like to see:")
                        name = input(">>> ") or "-"
                        s.send(name.encode())
                        answer = s.recv(4096).decode() # "Attraction not found!" or Attraction details
                        print(answer) # "Attraction not found!" or Attraction details
                            

                        # add attraction to faviorites list if found
                        if answer != "Attraction not found!":
                            print("Would you like to add this attraction to your favorites list? (yes/no)")
                            faviorite = yes_no_loop()
                            s.send(faviorite.encode())
                            print(s.recv(4096).decode()) # "Attraction added to your favorites!" or "Attraction already in favourites!" or ""
                                
                        # see details of another attraction
                        print("\nWould you like to see details of another attraction? (yes/no)")
                        answer = yes_no_loop()
                        s.send(answer.encode())

                        if answer.lower() == "no":
                            break
                        
                
            # get details of a specific attraction
            elif decission == "2":
                get_attraction_details_loop(s, traveller=True) # get details of a specific attraction (see clienthelper.py for the function)
                    
                
            # see favorite attractions
            elif decission == "3":
                attractions = s.recv(4096).decode()
                print("Your favorite attractions:")
                print_list(attractions) # print the favorite attractions

                # see details
                print("Would you like to see details of any attractions? (yes/no)")
                answer = yes_no_loop() # make sure the user enters "yes" or "no"
                    
                s.send(answer.encode()) # send the answer to the server if it is "yes" or "no"
                    
                if answer.lower() == "yes":
                    get_attraction_details_loop(s, traveller=True) 


            # rate an attraction
            elif decission == "4":
                print("Please enter the name of the attraction you would like to rate:")
                name = input(">>> ") or "-"
                s.send(name.encode())
                print("Please enter the destination of the attraction you would like to rate:")
                destination = input(">>> ") or "-"
                s.send(destination.encode())
                    
                # check if the attraction exists or is already rated
                found = s.recv(4096).decode() 
                if found != "Attraction found":
                    print(found) # "Attraction not found!" or "Attraction already rated!"
                    continue

                # get the rating from the user
                print("Please enter your rating (0-5):")
                rating = input(">>> ") or "-"
                while not rating.isnumeric() or float(rating) < 0 or float(rating) > 5:
                    print("Please enter a number between 0 and 5")
                    rating = input(">>> ") or "-"
                s.send(rating.encode())
                print(s.recv(4096).decode()) # "Attraction rated! Thank you for your feedback!"
                    
            # history of visited attractions
            elif decission == "5":
                print("Your visited attractions:")
                visited = s.recv(4096).decode()
                print_list(visited) # print the visited attractions

                # see details
                print("Would you like to see details of any attractions? (yes/no)")
                answer = yes_no_loop() # make sure the user enters "yes" or "no"
                if answer.lower() == "yes":
                    get_attraction_details_loop(s, traveller=True)

            # logout
            elif decission == "6":
                break     



    # while logged in as provider:
    elif type.lower() == "provider":
        decissions_str = s.recv(4096).decode()  # receive the decissions
        #decissions = json.loads(decissions_str.decode()) # convert the json string to a dictionary
        while True:    
            #print("\nWhat do you want to do now?")
            #for key, value in decissions.items():
            #   print(f"{key}) {value}")
            #decission = input("Enter the number\n>>> ") or "-"
            decission = print_menu_get_answer(decissions_str)
            s.send(decission.encode())

            # add a new attraction
            if decission == "1":
                print("Please fill out this form to add an attraction: \nName of the attraction: ")
                name = input(">>> ") or "-" 
                s.send(name.encode())
                print("Destination (e.g. Vienna): ")
                destination = input(">>> ") or "-"
                s.send(destination.encode())
                print("Type of the attraction (e.g. Restaurant): ")
                type = input(">>> ") or "-"
                s.send(type.encode())
                print("Price range: ")
                price_range = input(">>> ") or "-"
                s.send(price_range.encode())
                print("Description of the attraction: ")
                description = input(">>> ") or "-"
                s.send(description.encode())
                print("Contact: ")
                contact = input(">>> ") or "-"
                s.send(contact.encode())
                print("Special offer: ")
                special_offer = input(">>> ") or "-"
                s.send(special_offer.encode())

                # receive the confirmation or missing data message
                confirmation = s.recv(4096).decode()
                if confirmation == "Please try again and don't forget to add at least a name and a destination!":
                    print(confirmation)
                    continue
                print(confirmation) # "Attraction added!" or "A attraction with the name '{attraction}' already exists in {destination}!"
                
            
            # view attractions
            elif decission == "2":
                attractions = "Your attractions:\n" + s.recv(4096).decode() # receive the attractions as a string
                print_list(attractions) # print the attractions
                #for attraction in attractions.split(","): # .split(",") converts the string back to a list
                #   print(f"{attraction}")
                
                
                print("Would you like to see details of any attraction? (yes/no)")
                answer = yes_no_loop()
                s.send(answer.encode())
                
                if answer.lower() == "yes":
                    get_attraction_details_loop(s) # get details of a specific attraction (see clienthelper.py for the function)
               
            

            # update an attraction
            elif decission == "3":
                print("What is the name of the attraction you would like to update?")
                name = input(">>> ") or "-"
                s.send(name.encode())
                print("What is the destination of the attraction you would like to update?")
                destination = input(">>> ") or "-"
                s.send(destination.encode())
                confirmation = s.recv(4096).decode()
                if confirmation == "Attraction not found!" or confirmation == "Attraction belongs to another provider!":
                    print(confirmation)
                    continue

                # form to update the attraction:
                print(confirmation) # "Your current contact information: {attraction.contact}\nPlease enter the new contact information or press 'enter' for no change: "
                new_contact = input(">>> ") or "-"
                s.send(new_contact.encode())
                print(s.recv(4096).decode()) # "Your current price range: {attraction.price_range}\nPlease enter the new price range or press 'enter' for no change: "
                new_price = input(">>> ") or "-"
                s.send(new_price.encode())
                print(s.recv(4096).decode()) # "Your current description: {attraction.description}\nPlease enter the new description or press 'enter' for no change: "
                new_description = input(">>> ") or "-"
                s.send(new_description.encode())
                print(s.recv(4096).decode()) # "Your current special offer: {attraction.special_offer}\nPlease enter the new special offer or press 'enter' for no change: "
                new_special_offer = input(">>> ") or "-"
                s.send(new_special_offer.encode()) 
                print(s.recv(4096).decode()) # "Attraction updated!" 
                


            # remove an attraction
            elif decission == "4":  
                print("What is the name of the attraction you would like to remove?")
                name = input(">>> ") or "-"
                s.send(name.encode())
                print("What is the destination of the attraction you would like to remove?")
                destination = input(">>> ") or "-"
                s.send(destination.encode())

                print(s.recv(4096).decode()) # "Attraction removed!", "Attraction not found!", "Attraction belongs to another provider!"
                


            # logout
            elif decission == "5": 
                break
            
            
            #print("\nplease enter a number\n")


    print(f"Goodbye {user}!")
    s.close()  # close the connection


if __name__ == "__main__":
    start_client()