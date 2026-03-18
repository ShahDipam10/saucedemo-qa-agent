import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.test_data import LOGIN_VALID


class TestCart:

    @pytest.fixture(autouse=True)
    def login_first(self, page):
        login = LoginPage(page)
        login.login(LOGIN_VALID["username"], LOGIN_VALID["password"])

    def test_add_single_item_to_cart(self, page):
        inventory = InventoryPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1

    def test_add_multiple_items_to_cart(self, page):
        inventory = InventoryPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.add_item_to_cart("sauce-labs-bike-light")
        assert inventory.get_cart_count() == 2

    def test_remove_item_from_cart(self, page):
        inventory = InventoryPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1
        inventory.remove_item_from_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 0

    def test_cart_page_shows_added_items(self, page):
        inventory = InventoryPage(page)
        cart = CartPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()
        assert cart.is_loaded()
        assert cart.get_item_count() == 1
        assert "Sauce Labs Backpack" in cart.get_item_names()

    def test_add_items_list_and_verify_cart(self, page):
        inventory = InventoryPage(page)
        cart = CartPage(page)
        items = ["sauce-labs-backpack", "sauce-labs-bike-light"]

        inventory.add_items_to_cart(items)
        assert inventory.get_cart_count() == len(items)

        inventory.go_to_cart()
        assert cart.get_item_count() == len(items)
        assert cart.has_item("Sauce Labs Backpack")
        assert cart.has_item("Sauce Labs Bike Light")

