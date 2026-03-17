from utils.config import (
    VALID_USERNAME, VALID_PASSWORD,
    LOCKED_USER, INVALID_USERNAME, INVALID_PASSWORD
)

LOGIN_VALID = {"username": VALID_USERNAME, "password": VALID_PASSWORD}
LOGIN_LOCKED = {"username": LOCKED_USER, "password": VALID_PASSWORD}
LOGIN_INVALID = {"username": INVALID_USERNAME, "password": INVALID_PASSWORD}
LOGIN_EMPTY = {"username": "", "password": ""}
CHECKOUT_INFO = {"first_name": "Test", "last_name": "User", "postal_code": "380001"}
