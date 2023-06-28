from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
connection_string = "sqlite:///database.db"
db = create_engine(connection_string)
base = declarative_base()

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza')

    def __repr__(self):
        return f'<Restaurant {self.name} for {self.address}>'


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizza')

    def __repr__(self):
        return f'<Pizza {self.name} for {self.ingredients}>'


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurant.id'), primary_key=True)
    price = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    pizza_id = db.Column(db.Integer, db.ForeignKey(
        'pizza.id'), primary_key=True)
    restaurant = db.relationship('Restaurant', backref=db.backref(
        'restaurant_pizza', cascade='all, delete-orphan'))
    pizza = db.relationship('Pizza', backref=db.backref(
        'restaurant_pizza', cascade='all, delete-orphan'))

    @validates('price')
    def validate_email(self, key, restaurant_pizzas):
        if restaurant_pizzas.price not in range(1, 30):
            raise ValueError("please enter price between 1 and 30")
        return restaurant_pizzas.price


Session = sessionmaker(db)
session = Session()
# def __repr__(self):
#     return f'<RestaurantPizza {self.title} for {self.platform}>'


# add any models you may need.
