# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship

# from .attraction import Attraction

# Base = declarative_base() # All custom classes must inherit from a known Base:


# class Bar(Attraction):
#     __tablename__ = 'bar_table'

#     def __init__(self):
#         pass

#     def __init__(self, id, name, address, email_address, phone_number, price_range, special_offer, happy_hour):
#         super().__init__(id, name, address, email_address, phone_number, price_range, special_offer)
#         self.happy_hour = happy_hour


# class Restaurant(Attraction):
#     def __init__(self, id, name, address, email_address, phone_number, price_range, special_offer, cuisine):
#         super().__init__(id, name, address, email_address, phone_number, price_range, special_offer)
#         self.cuisine = cuisine


# class Tours(Attraction):
#     def __init__(self, id, name, address, email_address, phone_number, price_range, special_offer, tour_type):
#         super().__init__(id, name, address, email_address, phone_number, price_range, special_offer)
#         self.tour_type = tour_type


# class Hotels(Attraction):
#     def __init__(self, id, name, address, email_address, phone_number, price_range, special_offer, stars):
#         super().__init__(id, name, address, email_address, phone_number, price_range, special_offer)
#         self.stars = stars'