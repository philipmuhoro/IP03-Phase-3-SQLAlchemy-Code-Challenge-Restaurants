from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import desc

Base = declarative_base()
engine = create_engine('sqlite:///restaurant.db')
session = Session(engine)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship('Review', back_populates='customer')
    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def favorite_restaurant(self):
        return max(self.reviews, key=lambda review: review.star_rating).restaurant
    
    def add_review(self, restaurant, rating):
        review = review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(review)
        session.commit()
        
    def delete_reviews(self, restaurant):
        for review in self.reviews:
            if review.restaurant == restaurant:
                session.delete(review)
        session.commit()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    reviews = relationship('Review', back_populates='restaurant')
    
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(desc(cls.price)).first()
    
    def all_reviews(self):
        review_strings = [
            f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars."
            for review in self.reviews
        ]
        return review_strings
    
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')





    