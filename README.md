# Assignment_2
### Summary:
A chat based Travel-Support-App

### Requierments
-An Attraction can not be added if it another one with the same name & same destination already exists.

### Some notes on how to run the code via Terminal:
1. Direct into the Assignment_2/src directory and execute:
    python -m sockets.server
2. run Assignment_2/src/client.py file and
3. simply follow the Steps in the terminal

### Changes from the initional proposal:
- I used one User class for travellers and provideres instead of two, for better usability (espicially when handeling the Database).
- I also omited the Destination Class and added it as a attribute of the Attraction class, as it makes the code less complicated, but achieves the same result.
- Instead of Subclasses (Bars, Tours, Restaurants and Hotels) for the Attractions, I used the attribute .attraction_type in the Attraction class. That way the Provider is able to add any kind of type, which will give more possibilites.




cd C:/Users/lisah/Assignment_2/src
python -m sockets.server