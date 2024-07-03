from server import app
from unittest.mock import patch
from db.db_helpers import DatabaseHelper


class TestShoppingCartAPI:
    def test_shopping_cart_item_get(self):
        with patch.object(
            DatabaseHelper, "execute_query", return_value=[(1, "apple", 10, 2)]
        ):
            response = app.test_client().get("/cart/items")
            assert response.json == [
                {"id": 1, "name": "apple", "price": 10, "quantity": 2}
            ]
            assert response.status_code == 200

    def test_shopping_cart_item_post(self):
        with patch.object(DatabaseHelper, "execute_query"):
            response = app.test_client().post(
                "/cart/items",
                json={"name": "banana", "price": 10, "quantity": 2},
            )
            assert response.json == {
                "message": "Item added to cart!",
                "data": {"name": "banana", "price": 10, "quantity": 2},
            }
            assert response.status_code == 200

    def test_shopping_cart_item_post_file_error(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            response = app.test_client().post("/cart/items")
            assert response.data == b"Schema file not found."

    def test_shopping_cart_item_post_validation_error(self):
        response = app.test_client().post(
            "/cart/items", json={"name": "banana", "price": -5, "quantity": "two"}
        )
        assert b"Schema validation failed" in response.data
