import json

from flask import request, Blueprint
from jsonschema import validate, ValidationError
from db.db_helpers import exec_db_query

cart_blueprint = Blueprint("cart", __name__)


@cart_blueprint.route("/add", methods=["POST"])
def add_item_to_cart():
    """Add item in request body to the cart."""
    try:
        with open("cart_item_schema.json") as f:
            item_schema = json.load(f)
        data = request.get_json()
        validate(instance=data, schema=item_schema)
        exec_db_query(
            """INSERT INTO cart (name, price, quantity) VALUES (%s, %s, %s)""",
            (data["name"], data["price"], data["quantity"]),
        )
        return {"message": "Item added to cart!", "data": {**data}}
    except FileNotFoundError:
        return "Schema file not found."
    except ValidationError as e:
        return "Schema validation failed: " + str(e)


@cart_blueprint.route("/view", methods=["GET"])
def view_cart():
    """Return the items currently in the cart as a JSON object."""
    items = exec_db_query("""SELECT * FROM cart""", fetch=True)
    results = []
    for item in items:
        item_dict = {
            "id": item[0],
            "name": item[1],
            "price": item[2],
            "quantity": item[3],
        }
        results.append(item_dict)
    return results
