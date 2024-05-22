import socket
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
s.connect(("localhost", 9000))  # connect to the server

# receive "welcome to the App! Are you a traveller or a provider?"
print(s.recv(4096) .decode())
type = input(">>> ")  # input "traveller" or "provider"
while type.lower() != "provider" and type.lower() != "traveller":
    print("please enter 'provider' or 'traveller'")
    type = input(">>> ")
s.send(type.encode())  # send the type to the server


# login or register
while True:
    msg = input("Are you new here? \n>>> ")  # input "yes" or "no"

    # create a new user:
    if msg.lower() == "yes": 
        s.send(msg.encode())  # send the "yes" to the server
        print(s.recv(4096).decode())  # "please enter your username: "
        user = input(">>> ") or "-"  # input a username
        s.send(user.encode()) # send the username to the server or "-" if no input
        print(s.recv(4096).decode())  # "please enter you new password: "
        password = input(">>> ") or "-"  # input a password
        s.send(password.encode()) 
        welcome = s.recv(4096)  # "welcome {username}!"
        if welcome.decode() != "user already exists" and welcome.decode() != "please enter a username and password":
            print(welcome.decode())
            break
        print(welcome.decode()) # user already exists
    
    # if user already exists:
    elif msg.lower() == "no":
        s.send(msg.encode())  # send the "no" to the server
        print(s.recv(4096).decode()) # "please enter your username: "
        user = input(">>> ") or "-"  # input a username
        s.send(user.encode())
        print(s.recv(4096).decode()) # "please enter your password: "
        password = input(">>> ") or "-"  # input a password
        s.send(password.encode())
        welcome = s.recv(4096)
        if welcome.decode() != "user not found" and welcome.decode() != "please enter a username and password":
            print(welcome.decode())
            break
        print(welcome.decode()) # user not found

    
    print("\nplease, try again from the start\n")





# while logged in as traveller:
if type.lower() == "traveller":
    while True:
        
        ##### listing the options of what to do:



        destinations = s.recv(4096)  # receive the destinations
        print("Where would you like to go?")
        for destination in destinations.decode().split(","): # .split(",") converts the string to a list
            print(f"{destination}\n")
        destination = input(">>> ")
        s.send(destination.encode())
        





        # listing the options
        options = s.recv(4096)
        print("What are you looking for?")
        for option in options.decode().split(","): # "bars, restaurants, tours, hotels"
            print(f"{option}s\n")
        option = input(">>> ")
        s.send(option.encode())

        # listing the specific attractions 
        #attractions = s.recv(4096)



# while logged in as provider:
elif type.lower() == "provider":
    options_str = s.recv(4096)  # receive the options
    options = json.loads(options_str.decode()) # convert the json string to a dictionary
    while True:    
        print("\nWhat do you want to do now?")
        for key, value in options.items():
            print(f"{key}) {value}")
        option = input("Enter the number\n>>> ")
        s.send(option.encode())

        # add a new attraction
        if option == "1":
            print("\nPlease fill out this form to add an attraction: ")
            print(s.recv(4096).decode()) # "Name of the attraction: "
            name = input(">>> ") or "-" 
            s.send(name.encode())
            print(s.recv(4096).decode()) # "Destination (e.g. Vienna): "
            destination = input(">>> ") or "-"
            s.send(destination.encode())
            print(s.recv(4096).decode()) # "Type of the attraction (e.g. Restaurant): "
            type = input(">>> ") or "-"
            s.send(type.encode())
            print(s.recv(4096).decode()) # "Price range: "
            price_range = input(">>> ") or "-"
            s.send(price_range.encode())
            print(s.recv(4096).decode()) # "Description of the attraction: "
            description = input(">>> ") or "-"
            s.send(description.encode())
            print(s.recv(4096).decode()) # "Contact: "
            contact = input(">>> ") or "-"
            s.send(contact.encode())
            print(s.recv(4096).decode()) # "Special offer: "
            special_offer = input(">>> ") or "-"
            s.send(special_offer.encode())

            # receive the confirmation or missing data message
            confirmation = s.recv(4096)
            if confirmation.decode() == "Please try again and don't forget to add at least a name and a destination!":
                print(confirmation.decode())
                continue
            print(confirmation.decode()) # "Attraction added!" or "A attraction with the name '{attraction}' already exists in {destination}!"
            
        # remove an attraction
        elif option == "2":  
            print(s.recv(4096).decode()) # "What is the name of the attraction you would like to remove?"
            name = input(">>> ") or "-"
            s.send(name.encode())
            print(s.recv(4096).decode()) # "What is the destination of the attraction you would like to remove?"
            destination = input(">>> ") or "-"
            s.send(destination.encode())

            confirmation = s.recv(4096)
            print(confirmation.decode()) # "Attraction removed!", "Attraction not found!", "Attraction belongs to another provider!"
            
                

        # update an attraction
        elif option == "3":
            print(s.recv(4096).decode()) # "What is the name of the attraction you would like to update?"
            name = input(">>> ")
            s.send(name.encode())
            print(s.recv(4096).decode()) # "What is the destination of the attraction you would like to update?"
            destination = input(">>> ")
            s.send(destination.encode())
            confirmation = s.recv(4096)
            if confirmation.decode() == "Attraction not found!":
                print(confirmation.decode())
                continue
            print(s.recv(4096).decode()) # "Your current contact information: {attraction.contact}\nPlease enter the new contact information or 'skip' for no change: "
            new_contact = input(">>> ")
            s.send(new_contact.encode())
            print(s.recv(4096).decode()) # "Your current price range: {attraction.price_range}\nPlease enter the new price range or 'skip' for no change: "
            new_price = input(">>> ")
            s.send(new_price.encode())
            print(s.recv(4096).decode()) # "Your current description: {attraction.description}\nPlease enter the new description or 'skip' for no change: "
            new_description = input(">>> ")
            s.send(new_description.encode())
            print(s.recv(4096).decode()) # "Your current special offer: {attraction.special_offer}\nPlease enter the new special offer or 'skip' for no change: "
            new_special_offer = input(">>> ")
            s.send(new_special_offer.encode())
            print(s.recv(4096).decode()) # "Attraction updated!"
            
        # view attractions
        elif option == "4":
            attractions = s.recv(4096)
            for attraction in attractions.decode().split(","):
                print(f"{attraction}")
            print("Would you like to see details of one of your attractions? (yes/no)")
            answer = input(">>> ")
            s.send(answer.encode())
            while True:
                if answer.lower() == "yes":
                    print("Please enter the name of the attraction you would like to see:")
                    name = input(">>> ")
                    s.send(name.encode())
                    print("Please enter the destination of the attraction you would like to see:")
                    destination = input(">>> ")
                    s.send(destination.encode())
                    print(s.recv(4096).decode()) # "Attraction not found!" or Attraction details
                    break
                
                elif answer.lower() == "no":
                    break 

                print("please enter 'yes' or 'no'") 

        # logout
        elif option == "5": 
            break
        print("\nplease enter a number\n")


print("Goodbye!")
s.close()  # close the connection



