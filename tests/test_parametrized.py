"""
Data-driven tests - reads from data/test_data.json via utils/data_loader.py.
One test function runs for every entry in the JSON automatically.
"""
import pytest
import os
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data_loader import valid_users, products, invalid_checkout_info, valid_checkout_info
from utils.test_data import LOGIN_VALID

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")


class TestDataDriven:

    @pytest.mark.parametrize("username, password", valid_users())
    def test_all_valid_users_see_6_products(self, page, username, password):
        LoginPage(page).login(username, password)
        assert len(InventoryPage(page).get_product_names()) == 6

    @pytest.mark.parametrize("username, password", valid_users())
    def test_all_valid_users_can_add_to_cart(self, page, username, password):
        LoginPage(page).login(username, password)
        inventory = InventoryPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1

    @pytest.mark.parametrize("product_id, product_name, expected_price", products())
    def test_each_product_detail_shows_correct_info(self, page, product_id, product_name, expected_price):
        LoginPage(page).login("standard_user", "secret_sauce")
        InventoryPage(page).click_product(product_name)
        product = ProductPage(page)
        assert product.get_name() == product_name
        assert product.get_price_as_float() == expected_price

    @pytest.mark.parametrize("product_id, product_name, expected_price", products())
    def test_each_product_can_be_added_from_detail_page(self, page, product_id, product_name, expected_price):
        LoginPage(page).login("standard_user", "secret_sauce")
        InventoryPage(page).click_product(product_name)
        product = ProductPage(page)
        product.add_to_cart()
        assert product.get_cart_count() == 1

    @pytest.mark.parametrize("first, last, postal, expected_error", invalid_checkout_info())
    def test_checkout_validation_errors(self, page, first, last, postal, expected_error):
        LoginPage(page).login(LOGIN_VALID["username"], LOGIN_VALID["password"])
        InventoryPage(page).add_item_to_cart("sauce-labs-backpack")
        page.locator("[data-test='shopping-cart-link']").click()
        CartPage(page).proceed_to_checkout()
        checkout = CheckoutPage(page)
        checkout.fill_info(first, last, postal)
        checkout.continue_to_overview()
        assert expected_error in checkout.get_error_message()

    @pytest.mark.parametrize("first, last, postal", valid_checkout_info())
    def test_checkout_completes_with_valid_data(self, page, first, last, postal):
        LoginPage(page).login(LOGIN_VALID["username"], LOGIN_VALID["password"])
        InventoryPage(page).add_item_to_cart("sauce-labs-backpack")
        page.locator("[data-test='shopping-cart-link']").click()
        CartPage(page).proceed_to_checkout()
        checkout = CheckoutPage(page)
        checkout.fill_info(first, last, postal)
        checkout.continue_to_overview()
        checkout.finish_order()
        assert checkout.is_order_complete()
