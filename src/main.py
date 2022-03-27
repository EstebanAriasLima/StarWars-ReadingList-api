"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import Person, Vehicle, Planet, Item, Base
# from create_people import create_people

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

base_url = "https://www.swapi.tech/api/"
@app.route('/people', methods=[ 'GET', 'POST'])
def handle_people():
    if request.method == 'GET':
        persons = Person.query.all()
        return jsonify(list(map(
            lambda person: person.serialize(),
            persons)
        )), 200
    else: 
        body = request.json
        person = Person.create(
            name=body['name'],
            eye_color=body['eye_color']
        )
        dictionary = person.serialize()
        return jsonify(dictionary), 201

@app.route('/people/<int:id>', methods=['GET'])
def more_details_person(id):
    #buscar en base de datos al personaje cuya id corresponde a la suya
    person = Person.query.get(id)
    if isinstance(person, Person):
        #enviar una vista detallada del personaje
        print(person)
        dictionary = person.serialize(long=True)
        return jsonify(dictionary), 200
    return 404


@app.route('/populate-people', methods=['POST'])
def populate_persons():
    response = requests.get(
        f"{base_url}{'people'}"
    )
    body = response.json()
    all_people = []
    for result in body['results']:
        response = requests.get(result['url'])
        body = response.json()
        all_people.append(body['result']['properties'])
    instances = []
    for person in all_people:
        instance = Person.create(person)
        instances.append(instance)
    return jsonify(list(map(
        lambda inst:inst.serialize(),
        instances
    ))), 200

@app.route('/planets', methods=[ 'GET', 'POST'])
def handle_planets():
    if request.method == 'GET':
        planets = Planet.query.all()
        return jsonify(list(map(
            lambda person: planet.serialize(),
            planets)
        )), 200
    else: 
        body = request.json
        planet = Planet.create(
            name=body['name'],
            climate=body['climate']
        )
        dictionary = planet.serialize()
        return jsonify(dictionary), 201

@app.route('/populate-planets', methods=['POST'])
def populate_planets():
    response = requests.get(
        f"{base_url}{'planets'}"
    )
    body = response.json()
    all_planets = []
    for result in body['results']:
        response = requests.get(result['url'])
        body = response.json()
        all_planets.append(body['result']['properties'])
    instances = []
    for planet in all_planets:
        instance = Planet.create(planet)
        instances.append(instance)
    return jsonify(list(map(
        lambda inst:inst.serialize(),
        instances
    ))), 200

@app.route('/vehicles', methods=[ 'GET', 'POST'])
def handle_vehicles():
    if request.method == 'GET':
        vehicles = Vehicle.query.all()
        return jsonify(list(map(
            lambda person: vehicle.serialize(),
            vehicles)
        )), 200
    else: 
        body = request.json
        vehicle = Vehicle.create(
            name=body['name'],
            max_atmosphering_speed=body['max_atmosphering_speed']
        )
        dictionary = vehicle.serialize()
        return jsonify(dictionary), 201

@app.route('/populate-vehicles', methods=['POST'])
def populate_vehicles():
    response = requests.get(
        f"{base_url}{'vehicles'}"
    )
    body = response.json()
    all_vehicles = []
    for result in body['results']:
        response = requests.get(result['url'])
        body = response.json()
        all_vehicles.append(body['result']['properties'])
    instances = []
    for vehicle in all_vehicles:
        instance = Vehicle.create(vehicle)
        instances.append(instance)
    return jsonify(list(map(
        lambda inst:inst.serialize(),
        instances
    ))), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
