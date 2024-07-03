import json

from flask import request, Blueprint
from flask.views import MethodView
from jsonschema import validate, ValidationError
from db.db_helpers import DatabaseHelper


class ShoppingCartItemsAPI(MethodView):
    def get(self):
        """Return the items currently in the cart as a JSON object."""
        items = DatabaseHelper().execute_query("""SELECT * FROM cart""", fetch=True)
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

    def post(self):
        """Add item in request body to the cart."""
        try:
            with open("cart_item_schema.json") as f:
                item_schema = json.load(f)
            data = request.get_json()
            validate(instance=data, schema=item_schema)
            DatabaseHelper().execute_query(
                """INSERT INTO cart (name, price, quantity) VALUES (%s, %s, %s)""",
                (data["name"], data["price"], data["quantity"]),
            )
            return {"message": "Item added to cart!", "data": {**data}}
        except FileNotFoundError:
            return "Schema file not found."
        except ValidationError as e:
            return "Schema validation failed: " + str(e)


cart_blueprint = Blueprint("cart", __name__)
cart_blueprint.add_url_rule(
    "/cart/items", view_func=ShoppingCartItemsAPI.as_view("cart")
)
