
class Attraction():
    def __init__(self, id, name, address, email_address, phone_number, price_range, special_offer):
        self.id = id
        self.name = name
        self.address = address
        self.email_address = email_address
        self.phone_number = phone_number
        self.price_range = price_range
        self.rating = 0 
        self.reviews = []
        self.bookings = []
        self.visited = False
        self.special_offer = special_offer
