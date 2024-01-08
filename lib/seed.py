from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib import Base, Restaurant, Customer, Review
from restaurant import Base, engine, session, Customer, Restaurant, Review
# Assuming you have created the engine and session
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Seed data for testing
restaurant1 = Restaurant(name='Origin Coffee House', price=3000)
restaurant2 = Restaurant(name='Views Coffee House', price=4500)
restaurant3 = Restaurant(name='Kilimanjaro Restaurant', price=9500)

customer1 = Customer(first_name='Linda', last_name='Mukami')
customer2 = Customer(first_name='Philip', last_name='Muhoro')
customer3 = Customer(first_name='Peter', last_name='Drury')

review1 = Review(restaurant=restaurant1, customer=customer1, star_rating=5)
review2 = Review(restaurant=restaurant1, customer=customer2, star_rating=4)
review3 = Review(restaurant=restaurant2, customer=customer1, star_rating=3)
review4 = Review(restaurant=restaurant3, customer=customer3, star_rating=5)

# Add instances to the session
session.add_all([restaurant1, restaurant2, restaurant3, customer1, customer2, customer3, review1, review2, review3, review4])
session.commit()