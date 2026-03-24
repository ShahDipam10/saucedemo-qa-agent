import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.data_loader import valid_users, invalid_users


class TestLogin:

    @pytest.mark.parametrize("username, password", valid_users())
    def test_valid_login(self, page, username, password):
        """All valid user types should land on the inventory page."""
        LoginPage(page).login(username, password)
        inventory = InventoryPage(page)
        assert inventory.is_loaded(), f"Inventory did not load for user: {username}"
        assert inventory.get_title() == "Products"

    @pytest.mark.parametrize("username, password, expected_error", invalid_users())
    def test_invalid_login(self, page, username, password, expected_error):
        """Each invalid credential set should show the correct error message."""
        login = LoginPage(page)
        login.login(username, password)
        assert login.is_error_visible(), f"No error shown for user: {username!r}"
        assert expected_error in login.get_error_message()
