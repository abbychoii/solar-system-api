from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.planet import Planet

# class Planet:
#     def __init__(self, id, name, description, moon):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.moon = moon

# solar_system = [
#     Planet(1, "Mercury", "closest planet to the sun", 0),
#     Planet(2, "Venus", "hottest planet in our solar system", 0),
#     Planet(3, "Earth", "home planet", 1),
#     Planet(4, "Mars", "cold desert like planet, maybe the next earth?", 2),
#     Planet(5, "Jupiter", "more than twice as massive than the other planets of our solar system combined", 79),
#     Planet(6, "Saturn", "if you like it then you better put a ring on it, famous for its distinctive ring system", 83),
#     Planet(7, "Uranus", "rotates at a nearly 90-degree angle from the plane of its orbit", 27),
#     Planet(8, "Neptune", "coldest planet in the solar system with supersonic strong winds", 14),
#     Planet(9, "Pluto", "no longer a planet :(", 5)

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

def validate_planet_id(id):
    try:
        id = int(id)
    except:
        abort(make_response(f"Invalid Planet ID: {id}. Please enter an integer.", 400))
    
    planet = Planet.query.get(id)

    if not planet:
        abort(make_response(f"Planet ID {id} does not exist.", 404))
    
    return planet
@planets_bp.route("", methods=["POST"])
def add_planet():
    request_body = request.get_json()

    new_planet = Planet(
        name=request_body["name"], 
        description=request_body["description"], 
        moon= request_body["moons"]
        )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(f"Planet {new_planet.name} successfully created"), 201

# @planets_bp.route("", methods=["GET"])
# def get_all_planets():
#     planets = Planet.query.all()
#     response = []
#     for planet in planets:
#         planet_dict = {
#             "id": planet.id,
#             "name": planet.name,
#             "description": planet.description,
#             "moons": planet.moon
#         }
#         response.append(planet_dict)
        
#     return jsonify(response), 200
    

@planets_bp.route("<planet_id>", methods=["GET"])
def get_one_planet_by_id(planet_id):
    planet = validate_planet_id(planet_id)

    planet_dict = {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "moons": planet.moon
    }

    return jsonify(planet_dict), 200

@planets_bp.route("<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet_id(planet_id)

    request_body = request.get_json()

    if "name" not in request_body or \
        "description" not in request_body or \
        "moons" not in request_body:
            return jsonify({"message": "Request must include name, description, and moons"}), 400

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.moons = request_body["moons"]
    
    db.session.commit()

    return jsonify({"message": f"Successfully replaced planet with id of {planet_id}"}), 200

@planets_bp.route("<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet_id(planet_id)
    
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": f"Planet {planet_id} successfully deleted."}), 200

@planets_bp.route("", methods=["GET"])
def read_planet():

    # this code replaces the previous query all code
    name_query = request.args.get("name")
    if name_query:
        planet = Planet.query.filter_by(name=name_query)
    else:
        planets = Planet.query.all()
    # end of the new code

    planets_response = []
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "moons": planet.moon
        })

    return jsonify(planets_response)

@planets_bp.route("/name/<planet_name>", methods=["GET"])
def get_planet_by_name(planet_name):
    planet_name = planet_name.capitalize()
    planets = Planet.query.filter_by(name=planet_name)

    planets_response = []
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.id,
            "description": planet.description,
            "moons": planet.moon
        })
    return jsonify(planets_response)

# @planets_bp.route("/name/<planet_name>", methods=["GET"])
# def get_planet_by_name(planet_name):
#     if planet_name.isalpha():
#         planet_name = planet_name.capitalize()
#         for planet in solar_system:
#             if planet_name == planet.name:
#                 return {
#                     "id": planet.id,
#                     "name": planet.name,
#                     "description": planet.description,
#                     "moons": planet.moon
#                 }, 200
#                 # response = {
#                 #     "id": planet.id,
#                 #     "name": planet.name,
#                 #     "description": planet.description,
#                 #     "moons": planet.moon
#                 # }
#                 # return jsonify(response), 200
#         return {"message": f"planet {planet_name} not found"}, 404 #isalpha not found
#     return {"message": f"{planet_name} invalid, not alpha"}, 400 #not alpha can't check

# @planets_bp.route("/id/<planet_id>", methods=["GET"])
# def get_planet_by_id(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         return jsonify(f"invalid planet id: {planet_id}. ID must be an integer")
    
#     for planet in solar_system:
#         if planet.id == planet_id:
#             return {
#                     "id": planet.id,
#                     "name": planet.name,
#                     "description": planet.description,
#                     "moons": planet.moon
#                 }, 200
#     response_message = f"Could not find planet with ID {planet_id}"
#     return jsonify({"message": response_message}), 404q