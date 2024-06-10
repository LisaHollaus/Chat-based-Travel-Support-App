import json


# functions to support the client side of the application

def yes_no_loop():
    answer = input(">>> ") or "-" # get "yes" or "no" from the user or "-" if the user just presses enter
    while answer.lower() != "yes" and answer.lower() != "no":
        print("please enter 'yes' or 'no'")
        answer = input(">>> ") or "-" # repeat until the user enters "yes" or "no"
    return answer

# print dictionary options and get the user's answer 
def print_menu_get_answer(options_str):
    options = json.loads(options_str) # convert the json string to a dictionary
    print("\nWhat do you want to do now?")
    for key, value in options.items():
        print(f"{key}) {value}")

    option = input("Enter the number\n>>> ") or "-"
    while option not in options.keys():
        print("Please enter a valid number")
        option = input("Enter the number\n>>> ") or "-"
    print("\n") # print a new line for better readability
    return option

# print all list items in a string
def print_list(list_str):
    for line in list_str.split(","): # convert string to a list and print the destinations
        print(f"{line}")
      
# get attraction details and print them for the traveller (includes adding the attraction to the faviorites list if wanted)
def get_attraction_details_loop(s, traveller = False): # s is the socket and traveller is an optional parameter to give the traveller the option to add the attraction to the faviorites list
    while True:
        print("Please enter the name of the attraction you would like to see:")
        name = input(">>> ") or "-"
        s.send(name.encode())
        print("Please enter the destination of the attraction you would like to see:")
        destination = input(">>> ") or "-"
        s.send(destination.encode())
        answer = s.recv(4096).decode()
        print(answer) # "Attraction not found!" or Attraction details

        # option to add attraction to faviorites list if traveller is logged in
        if traveller and answer != "Attraction not found!":
            print("\nWould you like to add this attraction to your favorites list? (yes/no)")
            faviorite = yes_no_loop()
            s.send(faviorite.encode())
            print(s.recv(4096).decode()) # "Attraction added to your favorites!" or "Attraction already in favourites!" or ""

                
        # see details of another attraction
        print("\nWould you like to see details of another attraction? (yes/no)")
        answer = yes_no_loop()
                    
        s.send(answer.encode())
        if answer.lower() == "no":
            break    

  