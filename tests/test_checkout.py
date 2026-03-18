import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data import LOGIN_VALID, CHECKOUT_INFO


class TestCheckout:

    @pytest.fixture(autouse=True)
    def login_and_add_item(self, page):
        login = LoginPage(page)
        login.login(LOGIN_VALID["username"], LOGIN_VALID["password"])
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
        assert checkout.is_order_complete(), "Order completion message not shown"
        assert "Thank you" in checkout.get_success_message()

    def test_checkout_missing_first_name(self, page):
        cart = CartPage(page)
        checkout = CheckoutPage(page)
        cart.proceed_to_checkout()
        checkout.fill_info("", CHECKOUT_INFO["last_name"], CHECKOUT_INFO["postal_code"])
        checkout.continue_to_overview()
        assert "First Name is required" in checkout.get_error_message()

    def test_checkout_missing_postal_code(self, page):
        cart = CartPage(page)
        checkout = CheckoutPage(page)
        cart.proceed_to_checkout()
        checkout.fill_info(CHECKOUT_INFO["first_name"], CHECKOUT_INFO["last_name"], "")
        checkout.continue_to_overview()
        assert "Postal Code is required" in checkout.get_error_message()

    def test_checkout_overview_lists_items_and_calculates_total(self, page):
        inventory = InventoryPage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)

        inventory.add_item_to_cart("sauce-labs-backpack")
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
        assert total == pytest.approx(item_total + tax, rel=1e-3)

