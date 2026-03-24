import pytest
import os
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data import LOGIN_VALID, CHECKOUT_INFO
from utils.data_loader import invalid_checkout_info, valid_checkout_info

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")


class TestCheckout:

    @pytest.fixture(autouse=True)
    def login_and_add_item(self, page):
        LoginPage(page).login(LOGIN_VALID["username"], LOGIN_VALID["password"])
        inventory = InventoryPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

    def test_complete_checkout_flow(self, page):
        cart = CartPage(page)
        checkout = CheckoutPage(page)
        cart.proceed_to_checkout()
        checkout.fill_info(CHECKOUT_INFO["first_name"], CHECKOUT_INFO["last_name"], CHECKOUT_INFO["postal_code"])
        checkout.continue_to_overview()
        checkout.finish_order()
        assert checkout.is_order_complete()
        assert "Thank you" in checkout.get_success_message()

    @pytest.mark.parametrize("first, last, postal, expected_error", invalid_checkout_info())
    def test_checkout_validation_errors(self, page, first, last, postal, expected_error):
        """Each missing field combination should show the correct error."""
        cart = CartPage(page)
        checkout = CheckoutPage(page)
        cart.proceed_to_checkout()
        checkout.fill_info(first, last, postal)
        checkout.continue_to_overview()
        assert expected_error in checkout.get_error_message()

    @pytest.mark.parametrize("first, last, postal", valid_checkout_info())
    def test_checkout_succeeds_with_valid_data(self, page, first, last, postal):
        """Checkout should complete successfully for all valid info combinations."""
        cart = CartPage(page)
        checkout = CheckoutPage(page)
        cart.proceed_to_checkout()
        checkout.fill_info(first, last, postal)
        checkout.continue_to_overview()
        checkout.finish_order()
        assert checkout.is_order_complete()

    def test_checkout_overview_lists_items_and_calculates_total(self, page):
        page.goto(f"{BASE_URL}/inventory.html")
        inventory = InventoryPage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)
        inventory.add_item_to_cart("sauce-labs-bike-light")
        inventory.go_to_cart()
        cart.proceed_to_checkout()
        checkout.fill_info(CHECKOUT_INFO["first_name"], CHECKOUT_INFO["last_name"], CHECKOUT_INFO["postal_code"])
        checkout.continue_to_overview()
        names = checkout.get_overview_item_names()
        assert "Sauce Labs Backpack" in names
        assert "Sauce Labs Bike Light" in names
        item_total = checkout.get_item_total()
        assert item_total > 0
        tax = checkout.get_tax_amount()
        total = checkout.get_total()
        assert total == pytest.approx(item_total + tax, rel=1e-2)
