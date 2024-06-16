# Assignment_2
### Summary:
A chat based Travel-Support-App

### Requierments
-An Attraction can not be added if another one with the same name & same destination already exists.

### Some notes on how to run the code via Terminal:
1. Create virtual environment, activate and install dependencies 
2. Direct into the Assignment_2 directory (root directory) and execute:
    python src.sockets.server
    (In visual Studio Code I had to use: python -m src.sockets.server)

3. Execute in a new terminal:
    python src.sockets.client
    (In visual Studio Code I had to use: python -m src.sockets.server)
    (I recomend to use Pycharm)
    
4. Simply follow the Steps in the terminal on the client side

- For testing the application, simply run pytest in the root directory

### Changes from the initional proposal:
Overall I made some slight changes to my initional proposal as I realised, that some ideas of mine weren't that practical and could be improved. For eample:
- I used one User class for travellers and provideres instead of two, for better usability (espicially when handeling the Database).
- I also omited the Destination Class and added it as a attribute of the Attraction class, as it makes the code less complicated, but achieves the same result.
- I added the option to store a travellers faviourite attractions instead of the booking option, since the user(traveller) can get all necessary informations to book a trip by requesting the details of a attraction and some attractions (e.g.: Bars) might not offer booking options.
- Instead of Subclasses (Bars, Tours, Restaurants and Hotels) for the Attractions, I used the attribute .attraction_type in the Attraction class. That way the Provider is able to add any kind of type, which will give more individual possibilites.


### Some additional notes on design choices:

- I defined the User and Attraction class in one file, because seperating them would have interfered with creating the many to many relationship between the Users-attraction and the Attractions-traveller_id. 
- In my initional Proposal I had a "Agency", which I reneamed to ServerHelper, as all it does is helping the Server. I also added a ClientHelper, as it made my code a lot shorter.

### Things I would change if I had more time:
Looking back and knowing what I know now I could have made some improvements/changes as I learned a lot along the way:
- I could have used a context manager to close the connection at the end of many functions
- there probably would have been a way to awoid the many to many relationship and the extra table for it in my Database 
- The tests fullfill their purpose, but I think there would have been better/easier ways to test my functions (using testdata). 
- generally I think there would have been more ocations to shorten my code, by adding additional functions
- I found out about the session.merge() function very late (to bind objects to a session). I believe it could have made my code on many ocations simpler and shorter
- Also, I believe there would have been better ways to test my client and server functions. I believe with more time and research I could have found a way to test the client and server functions more efficiently and thoroughly.

After all I think I learned a lot along the process, as many things were still new to me. So I believe this is not the optimal way to approach a travel-helper-app like my initional idea was, but it helped me a lot in my learning process and I hope it's good enough. :) 


# to do

- def test_get_attraction_details_loop(clienthelper):
    pass
    
- def test_view_attraction_details_loop(serverhelper):
    pass

- test_client
- test_server

- solve sql relationship overlaps




python -m src.sockets.server
python -m src.sockets.client
cd .venv
.\Scripts\activate