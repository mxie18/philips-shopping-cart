from flask import Flask
from blueprints.cart import cart_blueprint
from db.db_helpers import DatabaseHelper


class Server:
    def __init__(self):
        self._app = Flask(__name__)
        self.register_blueprints()

    @property
    def app(self):
        return self._app

    def register_blueprints(self):
        self.app.register_blueprint(cart_blueprint)


if __name__ == "server":
    app = Server().app
    DatabaseHelper().create_table()
