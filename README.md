# Assignment_2
### Summary:
A chat based Travel-Support-App

### Requierments
-An Attraction can not be added if another one with the same name & same destination already exists.

### Some notes on how to run the code via Terminal:
1. Direct into the Assignment_2/src directory and execute:
    python -m sockets.server
2. run Assignment_2/src/client.py file and
3. simply follow the Steps in the terminal

### Changes from the initional proposal:
- I used one User class for travellers and provideres instead of two, for better usability (espicially when handeling the Database).
- I also omited the Destination Class and added it as a attribute of the Attraction class, as it makes the code less complicated, but achieves the same result.
- Instead of Subclasses (Bars, Tours, Restaurants and Hotels) for the Attractions, I used the attribute .attraction_type in the Attraction class. That way the Provider is able to add any kind of type, which will give more individual possibilites.


- Storing all the Attractions in one table might not be the best solution when it comes to big data, but this was the best I could come up with in this limited time.


### Some additional notes on design choices:
- I decided to keep the "conversation questions" between server and client mainly on the server side. 
Although it might have saved some computing power if I would have just printed some on the client side, I thought it would be more clear and readable if I keep it in this "conversation" style 

- I defined the User and Attraction class in one file, because seperating them would have interfered with creating the many to many relationship between the Users attractions and the Attractions travller ids. 



# to do
- switch remove and update order
- settle on only asking questions from the server or keeping them in the client (explain decission in readme)
- rename attraction.py to Tables or Database? 
- figure out how to deal with null entries in client (try except?)



cd C:/Users/lisah/Assignment_2/src
python -m sockets.server