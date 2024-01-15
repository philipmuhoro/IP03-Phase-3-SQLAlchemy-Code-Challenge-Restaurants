from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import desc

# Create a database engine and session
engine = create_engine('sqlite:///restaurants.db')  # Use the appropriate database URL
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship('Review', back_populates='restaurant')

    def customers(self):
        # Collect all the customers who reviewed the Restaurant
        return [review.customer for review in self.reviews]
    
    @classmethod
    def fanciest(cls):
        # Find the restaurant with the highest price
        return session.query(cls).order_by(desc(cls.price)).first()

    def all_reviews(self):
        # Get all reviews for this restaurant as formatted strings
        return [review.full_review() for review in self.reviews]

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship('Review', back_populates='customer')

    def restaurants(self):
        # Collect all the restaurants that the Customer has reviewed
        return [review.restaurant for review in self.reviews]
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        # Find the restaurant with the highest star rating from this customer
        return max(self.reviews, key=lambda review: review.star_rating).restaurant if self.reviews else None

    def add_review(self, restaurant, rating):
        # Create a new review for the restaurant with the given rating
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
        # Remove all reviews for this restaurant
        reviews_to_delete = [review for review in self.reviews if review.restaurant == restaurant]
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

Base.metadata.create_all(engine)
