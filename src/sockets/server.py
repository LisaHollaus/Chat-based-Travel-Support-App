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
    ## to do: check if user exists
    while True:
        msg = conn.recv(4096)  # receive a answer from the client
        if msg.decode().lower() == "yes": ### using .lower?
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
            if user == "user already exists":
                conn.send("user already exists".encode())
                continue
            msg = f"welcome {name.decode()}!"
            conn.send(msg.encode())
            break
            
        elif msg.decode().lower() == "no": 
            conn.send("please enter your username: ".encode())
            name = conn.recv(4096)
            conn.send("please enter your password: ".encode())
            password = conn.recv(4096)
            # check if the user and id is existing
            user = Agency.get_user(name.decode(), password.decode())
            
            
            ##### get the user and id from the database
            
            if user is None:
                conn.send("user not found".encode())
                continue
            print(f"user: {id.decode()} logged in")
            conn.send("welcome back! ".encode())
            break
        




# to handle multiple clients
while True:
    conn, addr = s.accept()  # this waits for a client to connect
    thread = threading.Thread(target=handle_client, args=(conn, addr))  # create a new thread
    thread.start()  # start the thread