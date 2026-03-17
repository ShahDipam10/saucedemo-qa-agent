import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.test_data import LOGIN_VALID, LOGIN_LOCKED, LOGIN_INVALID, LOGIN_EMPTY


class TestLogin:

    def test_valid_login(self, page):
        """Standard user should log in successfully."""
        login = LoginPage(page)
        inventory = InventoryPage(page)
        login.login(LOGIN_VALID["username"], LOGIN_VALID["password"])
        assert inventory.is_loaded(), "Inventory page did not load after valid login"
        assert inventory.get_title() == "Products"

    def test_invalid_login(self, page):
        """Wrong credentials should show an error message."""
        login = LoginPage(page)
        login.login(LOGIN_INVALID["username"], LOGIN_INVALID["password"])
        assert login.is_error_visible(), "Error message not shown for invalid login"
        assert "Username and password do not match" in login.get_error_message()

    def test_locked_user_login(self, page):
        """Locked out user should see a specific error."""
        login = LoginPage(page)
        login.login(LOGIN_LOCKED["username"], LOGIN_LOCKED["password"])
        assert login.is_error_visible(), "Error message not shown for locked user"
        assert "locked out" in login.get_error_message().lower()

    def test_empty_credentials(self, page):
        """Empty fields should trigger a validation error."""
        login = LoginPage(page)
        login.login(LOGIN_EMPTY["username"], LOGIN_EMPTY["password"])
        assert login.is_error_visible(), "Error message not shown for empty credentials"
        assert "Username is required" in login.get_error_message()
