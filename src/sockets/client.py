import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
s.connect(("localhost", 9000))  # connect to the server

msg = s.recv(4096)  # receive "welcome to the App!"
print(msg.decode())


# login or register
## to do: check if user exists and add password 
while True:
    msg = input("Are you new here? \n>>> ")  # input "yes" or "no"

    # create a new user:
    if msg.lower() == "yes": 
        s.send(msg.encode())  # send the "yes" to the server
        type_question = s.recv(4096) # receive "Are you a provider or a traveller? "
        print(type_question.decode())
        type = input(">>> ")
        s.send(type.encode())
        if type.lower() != "provider" and type.lower() != "traveller":
            print("please enter 'provider' or 'traveller'\n try again from the start \n")
            continue
        user_question = s.recv(4096)  # receive "please enter your username: "
        print(user_question.decode())
        user = input(">>> ")  # input a username
        s.send(user.encode())  # send the username to the server
        password_question = s.recv(4096)  # receive "please enter you new password: "
        print(password_question.decode())
        password = input(">>> ")  # input a password
        s.send(password.encode()) # send the password to the server
        welcome = s.recv(4096)  # receive "welcome {username}!"
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
        print("user not found")
    
    print("please, try again and enter 'yes' or 'no'")
   


## calling a menu function

