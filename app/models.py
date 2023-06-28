from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = 'Restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza')


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizza')


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


# add any models you may need.
