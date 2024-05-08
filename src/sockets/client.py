import socket
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
s.connect(("localhost", 9000))  # connect to the server

msg = s.recv(4096)  # receive "welcome to the App! Are you a traveller or a provider?"
print(msg.decode())
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
        user_question = s.recv(4096)  # "please enter your username: "
        print(user_question.decode())
        user = input(">>> ")  # input a username
        s.send(user.encode())  
        password_question = s.recv(4096)  # "please enter you new password: "
        print(password_question.decode())
        password = input(">>> ")  # input a password
        s.send(password.encode()) 
        welcome = s.recv(4096)  # "welcome {username}!"
        if welcome.decode() != "user already exists":
            print(welcome.decode())
            break

        print(welcome.decode()) # user already exists
    
    # if user already exists:
    elif msg.lower() == "no":
        s.send(msg.encode())  # send the "no" to the server
        question = s.recv(4096)  # receive "please enter your username: "
        print(question.decode())
        user = input(">>> ")
        s.send(user.encode())
        question = s.recv(4096)
        print(question.decode()) # receive "please enter your password: "
        password = input(">>> ")
        s.send(password.encode())
        welcome = s.recv(4096)
        if welcome.decode() != "user not found":
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
    while True:
        options_str = s.recv(4096)  # receive the options
        options = json.loads(options_str.decode()) # convert the json string to a dictionary
        print("What do you want to do now?")
        print(options)
        for option in options.values():
            print(f"{option}\n")
        option = input("Enter the number\n>>> ")
        s.send(option.encode())

        # add a new attraction
        if option == "1":
            print("Please fill out this form to add an attraction:")
            question = s.recv(4096) # "Name of the attraction: "
            print(question.decode())
            name = input(">>> ")
            s.send(name.encode())
            question = s.recv(4096) # "Destination (e.g. Vienna): "
            destination = input(">>> ")
            s.send(destination.encode())
            question = s.recv(4096) # "Type of the attraction (e.g. Restaurant): "
            type = input(">>> ")
            s.send(type.encode())
            question = s.recv(4096) # "Price range: "
            price_range = input(">>> ")
            s.send(price_range.encode())
            question = s.recv(4096) # "Description of the attraction: "
            description = input(">>> ")
            s.send(description.encode())
            question = s.recv(4096) # "Contact: "
            contact = input(">>> ")
            s.send(contact.encode())
            question = s.recv(4096) # "Special offer: "
            special_offer = input(">>> ")
            s.send(special_offer.encode())

            # receive the confirmation
            confirmation = s.recv(4096)
            if confirmation.decode():
                print(confirmation.decode()) # "Attraction added!"
            else:
                print(f"A attraction with the name '{name}' already exists in {destination}!")


        elif option == "2":
            pass
        elif option == "3":
            pass
        elif option == "4":
            pass
        elif option == "5":
            break


print("Goodbye!")
s.close()  # close the connection



