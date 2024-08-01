# Assignment_2
### Summary:
A chat based Travel-Support-App

### Requierments
- An Attraction can not be added if another one with the same name & same destination already exists.
- A User can not be added if another one with the same name already exists.
- An Attraction can not be added to a User's favourite list if it is already in there.
- A traveller can not rate an Attraction more than once.
- A provider can not add an Attraction if another one with the same name at the same destination already exists.
- A provider can not update an Attraction if it doesn't belong to him.
- A provider can not delete an Attraction if it doesn't belong to him.
- A provider can not change the rating of an Attraction.

### Some notes on how to run the code via Terminal:
1. Create virtual environment, activate and install dependencies 
2. Direct into the Assignment_2 directory (root directory) and execute:
    python src.sockets.server
    (In visual Studio Code I had to use: python -m src.sockets.server, therefore I recommend to use Pycharm)

3. Execute in a new terminal:
    python src.sockets.client
    (In visual Studio Code I had to use: python -m src.sockets.client, therefore I recommend to use Pycharm)
    
4. Simply follow the Steps in the terminal on the client side

- For testing the application, you can find all necessary files in the test folder.
- To run the tests, simply execute the test files in the test folder. (e.g.: python test_client.py)




### Things I would change if I had more time:
Looking back and knowing what I know now I could have made some improvements/changes as I learned a lot along the way:
- I maybe could have used decorators to close the connection at the end of many functions
- There probably would have been better ways to handle the databases relationships, as I had some problems with the many-to-many relationship between the Users-attraction and the Attractions-traveller_id. I had to use a workaround to make it work, but I believe there would have been a better way to do it.
- I found out about the session.merge() function very late (to bind objects to a session). It could have made my code on many occasions simpler and shorter
- Also, I believe there would have been better ways to test my client and server functions. With more time and research on mocking I could have found a way to test the client and server functions more efficiently and thoroughly

After all I think I learned a lot along the process, as many things were still new to me. So I believe this is not the optimal way to approach a travel-helper-app, but it helped me a lot in my learning process. :) 
