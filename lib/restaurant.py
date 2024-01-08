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


    