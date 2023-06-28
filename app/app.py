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


@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant == None:
        response_body = {
            "message": "Restaurant not found"
        }
        response = make_response(jsonify(response_body), 404)

        return response
    else:
        if request.method == 'GET':
            restaurant_dict = restaurant.to_dict()

            response = make_response(
                jsonify(restaurant_dict),
                200
            )

            return response
        elif request.method == 'DELETE':
            db.session.delete(restaurant)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message":  "Restaurant not found"
            }

            response = make_response(
                jsonify(response_body), 200
            )

            return response

    restaurant_dict = restaurant.to_dict()

    response = make_response(
        jsonify(restaurant_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/pizzas')
def pizzas():
    if request.method == 'GET':
        pizzas = []
        for pizza in Pizza.query.all():
            pizza_dict = pizza.to_dict()
            pizzas.append(pizza_dict)

    response = make_response(
        jsonify(pizzas),
        200
    )

    return response


@app.route('/restaurant_pizzas', methods=['GET', 'POST'])
def restaurant_pizzas():

    if request.method == 'GET':
        restaurant_pizzas = []
        for restaurant_pizza in RestaurantPizza.query.all():
            restaurant_pizza_dict = restaurant_pizza.to_dict()
            reviews.append(restaurant_pizza_dict)

        response = make_response(
            jsonify(restaurant_pizzas),
            200
        )

        return response

    elif request.method == 'POST':
        new_restaurant_pizza = RestaurantPizza(
            price=request.form.get("price"),

            restaurant_id=request.form.get("restaurant_id"),
            pizza_id=request.form.get("pizza_id"),
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        review_dict = new_restaurant_pizza.to_dict()

        response = make_response(
            jsonify(restaurant_pizza_dict),
            201
        )

        return response


if __name__ == '__main__':
    app.run(port=5555)
