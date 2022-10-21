from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, moon):
        self.id = id
        self.name = name
        self.description = description
        self.moon = moon

solar_system = [
    Planet(1, "Mercury", "closest planet to the sun", 0),
    Planet(2, "Venus", "hottest planet in our solar system", 0),
    Planet(3, "Earth", "home planet", 1),
    Planet(4, "Mars", "cold desert like planet, maybe the next earth?", 2),
    Planet(5, "Jupiter", "more than twice as massive than the other planets of our solar system combined", 79),
    Planet(6, "Saturn", "if you like it then you better put a ring on it, famous for its distinctive ring system", 83),
    Planet(7, "Uranus", "rotates at a nearly 90-degree angle from the plane of its orbit", 27),
    Planet(8, "Neptune", "coldest planet in the solar system with supersonic strong winds", 14),
    Planet(9, "Pluto", "no longer a planet :(", 5)
]

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    response = []
    for planet in solar_system:
        planet_dict = {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "moons": planet.moon
        }
        response.append(planet_dict)
        
    return jsonify(response), 200