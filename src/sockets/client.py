import socket
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
s.connect(("localhost", 9000))  # connect to the server

print("welcome to the App! Are you a traveller or a provider?")
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
        welcome = s.recv(4096)  # "welcome {username}!"
        if welcome.decode() != "user already exists" and welcome.decode() != "please enter a username and password":
            print(welcome.decode())
            break
        print(welcome.decode()) # user already exists
    
    # if user already exists:
    elif msg.lower() == "no":
        s.send(msg.encode())  # send the "no" to the server
        print("please enter your username: ")
        user = input(">>> ") or "-"  # input a username
        s.send(user.encode())
        print("please enter your password: ")
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
        # listing the options of what to do:
        options_str = s.recv(4096)  # receive the options
        options = json.loads(options_str.decode()) # convert the json string to a dictionary
        while True:    
            print("\nWhat do you want to do now?")
            for key, value in options.items():
                print(f"{key}) {value}")
            option = input("Enter the number\n>>> ") or "-"
            s.send(option.encode())

            # explore attractions
            if option == "1":
                destinations_str = s.recv(4096).decode()  # receive the destinations
                print("\nWhere would you like to go?")
                for destination in destinations_str.split(","): # convert string to a list and print the destinations
                    print(f"{destination}")
                
                destination = input("Enter a destination or 'everywhere' for a random search \n>>> ") or "-"
                s.send(destination.encode())
                
                attractions_str = s.recv(4096).decode()  # receive the attractions or "no attractions found!"
                if attractions_str == "no attractions found!":
                    print(attractions_str)
                    continue
                
                print(f"Here's a list of all attractions in {destination}:")
                for attraction in attractions_str.split(","):
                    print(f"{attraction}")
                
                print("Would you like to see details of any of these attractions? (yes/no)")
                answer = input(">>> ") or "-"
                
                while answer.lower() != "yes" and answer.lower() != "no":
                    print("please enter 'yes' or 'no'")
                    answer = input(">>> ") or "-"
                s.send(answer.encode()) # send the answer to the server if it is "yes" or "no"
                
                while True:
                    if answer.lower() == "yes":
                        print("Please enter the name of the attraction you would like to see:")
                        name = input(">>> ") or "-"
                        s.send(name.encode())
                        print(s.recv(4096).decode()) # "Attraction not found!" or Attraction details
                        
                        print("\nWould you like to see details of another attraction? (yes/no)")
                        answer = input(">>> ") or "-" # set the answer to "-" if no input
                        s.send(answer.encode())

                        if answer.lower() == "no":
                            break
                    
                    elif answer.lower() == "no":
                        break 

                print("Did you visited any of these attractions? (yes/no)")
                answer = input(">>> ") or "-"
                while answer.lower() != "yes" and answer.lower() != "no":
                    print("please enter 'yes' or 'no'")
                    answer = input(">>> ") or "-"
                s.send(answer.encode()) # send the answer only if "yes" or "no"
                if answer.lower() == "yes":
                    print("Please enter the name of the attraction you have visited:")
                    name = input(">>> ") or "-"
                    s.send(name.encode())
                    print(s.recv(4096).decode()) # "Attraction not found!" or "Attraction added to your visited attractions!"
        ####################

                elif answer.lower() == "no":
                    break



        # destinations = s.recv(4096).decode()  # receive the destinations
        # print("Where would you like to go?")
        # for destination in destinations.split(","): # .split(",") converts the string to a list
        #     print(f"{destination}\n")
        # destination = input(">>> ")
        # s.send(destination.encode())
        





        # # listing the options
        # options = s.recv(4096)
        # print("What are you looking for?")
        # for option in options.decode().split(","): # "bars, restaurants, tours, hotels"
        #     print(f"{option}s")
        # option = input(">>> ")
        # s.send(option.encode())

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
        option = input("Enter the number\n>>> ") or "-"
        s.send(option.encode())

        # add a new attraction
        if option == "1":
            print("\nPlease fill out this form to add an attraction: \nName of the attraction: ")
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
        elif option == "2":
            attractions = "\n" + s.recv(4096).decode() # receive the attractions as a string
            for attraction in attractions.split(","): # .split(",") converts the string back to a list
                print(f"{attraction}")
            
            
            print("Would you like to see details of any attraction? (yes/no)")
            answer = input(">>> ") or "-" 
            

            while True:
                while answer.lower() != "yes" and answer.lower() != "no":
                    print("please enter 'yes' or 'no'")
                    answer = input(">>> ") or "-"
                    
                s.send(answer.encode()) # send the answer to the server if it is "yes" or "no"


                if answer.lower() == "yes":
                    print("Please enter the name of the attraction you would like to see:")
                    name = input(">>> ") or "-"
                    s.send(name.encode())
                    print("Please enter the destination of the attraction you would like to see:")
                    destination = input(">>> ") or "-"
                    s.send(destination.encode())
                    print(s.recv(4096).decode()) # "Attraction not found!" or Attraction details
                    
                    print("\nWould you like to see details of another attraction? (yes/no)")
                    answer = input(">>> ") or "-" # set the answer to "-" if no input
                    s.send(answer.encode())

                    if answer.lower() == "no":
                        break
                
                elif answer.lower() == "no":
                    break 

                #print("please enter 'yes' or 'no'") 

        # update an attraction
        elif option == "3":
            print("\nWhat is the name of the attraction you would like to update?")
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
        elif option == "4":  
            print("\nWhat is the name of the attraction you would like to remove?")
            name = input(">>> ") or "-"
            s.send(name.encode())
            print("What is the destination of the attraction you would like to remove?")
            destination = input(">>> ") or "-"
            s.send(destination.encode())

            print(s.recv(4096).decode()) # "Attraction removed!", "Attraction not found!", "Attraction belongs to another provider!"
            


        # logout
        elif option == "5": 
            break
        
        
        #print("\nplease enter a number\n")


print(f"\nGoodbye {user}!")
s.close()  # close the connection



