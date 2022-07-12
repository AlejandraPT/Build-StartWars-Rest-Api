"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Favourites
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all() #le pido info a la tabla User
    usersList = list(map(lambda obj: obj.serialize(),users))
   
    response_body = {
        "results": userList
    }

    return jsonify(response_body), 200



# Sacar la Lista  de todos los characters

@app.route('/characters', methods=['GET'])
def handle_characters():

    characters = Characters.query.all() #le pido info a la tabla User
    charactersList = list(map(lambda obj: obj.serialize(),characters))
   
    response_body = {
        "results": charactersList
    }

    return jsonify(response_body), 200



# Sacar la info de todos los SINGLEcharacters

@app.route('/characters/<int:id>', methods=['GET'])
def handle_singlecharacters(id):
    characters_id = Characters.query.get(id)
    characters = characters_id.serialize()
    response_body = {
        "results": characters
    }
    return jsonify(response_body), 200



# Sacar la Lista  de todos los planets

@app.route('/planets', methods=['GET'])
def handle_planets():

    planets = Planets.query.all() #le pido info a la tabla 
    planetsList = list(map(lambda obj: obj.serialize(),planets))
   
    response_body = {
        "results": planetsList
    }

    return jsonify(response_body), 200



# Sacar la info de todos los SINGLEplanets

@app.route('/planets/<int:id>', methods=['GET'])
def handle_singleplanets(id):
    planets_id = Planets.query.get(id)
    planets = planets_id.serialize()
    response_body = {
        "results": planets
    }
    return jsonify(response_body), 200

# Sacar la Lista  de todos los Favourites


@app.route('/favourites', methods=['GET'])
def handle_favourites():

    favourites = Favourites.query.all() #le pido info a la tabla User
    favouritesList = list(map(lambda obj: obj.serialize(),favourites))
   
    response_body = {
        "results": favouritesList
    }

    return jsonify(response_body), 200


@app.route('/favourites/<int:id>', methods=['GET'])
def handle_singlefavourites(id):
    favourites_id = Favourites.query.get(id)
    favourites = favourites_id.serialize()
    response_body = {
        "results": favourites
    }
    return jsonify(response_body), 200


# Añadir a favoritos

@app.route('/user/<int:id>', methods=['POST'])
def handle_addfavourites(id):
    body = json.loads(request.data)
    print(body)
    favourites = Favourites(user_id = body["user_id"],characters_id = body["characters_id"],planets_id = body["planets_id"])
    db.session.add(favourites)
    db.session.commit()
    response_body = {
        "results": "Favourite was succesfully added"
    }
    return jsonify(response_body), 200


# Eliminar Favoritos
@app.route('/user/<int:id>/favourites/<int:user_id>', methods=['DELETE'])
def handle_(id, user_id):
    favourite = Favourites.query.filter_by(id = user_id).all()
    print(favourite)
    db.session.delete(favourite[1])
    db.session.commit()
    response_body = {
        "results": "Favourite was removed"
    }
    return jsonify(response_body), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)