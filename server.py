from flask import Flask
from db.db_helpers import exec_db_query
from blueprints.cart.cart import cart_blueprint

app = Flask(__name__)


@app.get("/")
def base():
    return "Server is running!"


app.register_blueprint(cart_blueprint, url_prefix="/cart")


if __name__ == "server":
    exec_db_query(
        """CREATE TABLE IF NOT EXISTS cart (id SERIAL PRIMARY KEY, name TEXT, price NUMERIC, quantity NUMERIC)"""
    )
