# Assignment_2
### Summary:
A chat based Travel-Support-App

### Requierments
-An Attraction can not be added if another one with the same name & same destination already exists.

### Some notes on how to run the code via Terminal:
1. Direct into the Assignment_2/src directory and execute:
    python -m sockets.server
2. Execute in a new terminal:
    python -m sockets.client
3. Simply follow the Steps in the terminal on the client side

### Changes from the initional proposal:
Overall I made some slight changes to my initional proposal as I realised, that some ideas of mine weren't that practical and could be improved. For eample:
- I used one User class for travellers and provideres instead of two, for better usability (espicially when handeling the Database).
- I also omited the Destination Class and added it as a attribute of the Attraction class, as it makes the code less complicated, but achieves the same result.
- I added the option to store a travellers faviourite attractions instead of the booking option, since the user(traveller) can get all necessary informations to book a trip by requesting the details of a attraction and some attractions (e.g.: Bars) might not offer booking options.
- Instead of Subclasses (Bars, Tours, Restaurants and Hotels) for the Attractions, I used the attribute .attraction_type in the Attraction class. That way the Provider is able to add any kind of type, which will give more individual possibilites.


### Some additional notes on design choices:

- I defined the User and Attraction class in one file, because seperating them would have interfered with creating the many to many relationship between the Users-attraction and the Attractions-traveller_id. 




# to do

- when leaving a review/rating the attraction gets added to visited attractions

- get rid of reviews and only keep rating

- run pytest over everything (add to instructions)

cd C:/Users/lisah/Assignment_2/src
python -m sockets.server
python -m sockets.client