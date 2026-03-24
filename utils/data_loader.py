import json
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.json")


def load():
    with open(_DATA_PATH, "r") as f:
        return json.load(f)


def valid_users():
    """Returns list of (username, password) tuples for parametrize."""
    return [(u["username"], u["password"]) for u in load()["login"]["valid_users"]]


def invalid_users():
    """Returns list of (username, password, expected_error) tuples for parametrize."""
    return [(u["username"], u["password"], u["error"]) for u in load()["login"]["invalid_users"]]


def valid_checkout_info():
    """Returns list of (first_name, last_name, postal_code) tuples for parametrize."""
    return [(d["first_name"], d["last_name"], d["postal_code"]) for d in load()["checkout"]["valid_info"]]


def invalid_checkout_info():
    """Returns list of (first_name, last_name, postal_code, expected_error) tuples for parametrize."""
    return [(d["first_name"], d["last_name"], d["postal_code"], d["error"]) for d in load()["checkout"]["invalid_info"]]


def products():
    """Returns list of (product_id, product_name, price) tuples for parametrize."""
    return [(p["id"], p["name"], p["price"]) for p in load()["products"]]
