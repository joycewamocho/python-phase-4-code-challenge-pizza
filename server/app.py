#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        restaurants = []
        for restaurant in Restaurant.query.all():
            # Convert the restaurant to a dict and remove the 'restaurant_pizzas' field
            restaurant_dict = restaurant.to_dict()
            if 'restaurant_pizzas' in restaurant_dict:
                del restaurant_dict['restaurant_pizzas']
            restaurants.append(restaurant_dict)

        response = make_response(restaurants, 200)
        return response
api.add_resource(Restaurants,'/restaurants')

class RestaurantsByID(Resource):
    def get(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            response =make_response(jsonify(restaurant.to_dict()),200)
            return response
        else:
            return make_response({"error":"Restaurant not found"},404)
    def delete(self,id):
        restaurant= Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response(f"restaurant {restaurant.name} deleted!",204)
        else:
            return make_response({"error":"Restaurant not found"},404)

api.add_resource(RestaurantsByID,'/restaurants/<int:id>')


class Pizzas(Resource):
    def get(self):
        pizzas = []
        for pizza in Pizza.query.all():
            # Convert the pizza to a dict and remove the 'restaurant_pizzas' field
            pizza_dict = pizza.to_dict()
            if 'restaurant_pizzas' in pizza_dict:
                del pizza_dict['restaurant_pizzas']
            pizzas.append(pizza_dict)

        response = make_response(pizzas, 200)
        return response

api.add_resource(Pizzas,'/pizzas')

class Restaurant_Pizza(Resource):
    def post(self):
        try:
            data=request.get_json()
            new_restaurant_pizza = RestaurantPizza(
                price=data["price"],
                pizza_id =data["pizza_id"],
                restaurant_id=data['restaurant_id'],
            )

            db.session.add(new_restaurant_pizza)
            db.session.commit()

        
            response= make_response(new_restaurant_pizza.to_dict(),201)
            return response
        except:
            response = make_response({"errors":["validation errors"]},400)
            return response
api.add_resource(Restaurant_Pizza,'/restaurant_pizzas')





if __name__ == "__main__":
    app.run(port=5555, debug=True)
