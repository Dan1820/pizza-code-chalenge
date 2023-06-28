#!/usr/bin/env python3

from flask import Flask, make_response,  jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return 'my website and other short stories'


@app.route('/restaurants')
def restaurants():

    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "name": restaurant.name,
            "address": restaurant.genre,

        }
        restaurants.append(restaurant_dict)

    response = make_response(
        jsonify(restaurants),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/restaurants/<int:id>')
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    restaurant_dict = restaurant.to_dict()

    response = make_response(
        jsonify(restaurant_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == '__main__':
    app.run(port=5555)
