from app import Restaurant, Customer, Review, session
from sqlalchemy.orm import sessionmaker

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
review5 = Review(restaurant=restaurant1, customer=customer1, star_rating=5)

session.add_all([restaurant1, restaurant2, restaurant3, customer1, customer2, customer3, review1, review2, review3, review4, review5])
Session = sessionmaker()
session.commit()
