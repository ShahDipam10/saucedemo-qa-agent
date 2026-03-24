"""
Data-driven tests using external JSON (data/test_data.json).
Demonstrates parametrize with multiple data sets loaded at runtime.
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from utils.data_loader import valid_users, products


class TestDataDriven:

    @pytest.mark.parametrize("username, password", valid_users())
    def test_all_valid_users_see_6_products(self, page, username, password):
        """Every valid user type should see all 6 products after login."""
        LoginPage(page).login(username, password)
        names = InventoryPage(page).get_product_names()
        assert len(names) == 6

    @pytest.mark.parametrize("username, password", valid_users())
    def test_all_valid_users_can_add_to_cart(self, page, username, password):
        """Every valid user type should be able to add an item to cart."""
        LoginPage(page).login(username, password)
        inventory = InventoryPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1

    @pytest.mark.parametrize("product_id, product_name, expected_price", products())
    def test_each_product_detail_page(self, page, product_id, product_name, expected_price):
        """Each product's detail page should show correct name and price."""
        LoginPage(page).login("standard_user", "secret_sauce")
        InventoryPage(page).click_product(product_name)
        product = ProductPage(page)
        assert product.get_name() == product_name
        assert product.get_price_as_float() == expected_price

    @pytest.mark.parametrize("product_id, product_name, expected_price", products())
    def test_each_product_can_be_added_from_detail_page(self, page, product_id, product_name, expected_price):
        """Adding to cart from every product detail page should update badge."""
        LoginPage(page).login("standard_user", "secret_sauce")
        InventoryPage(page).click_product(product_name)
        product = ProductPage(page)
        product.add_to_cart()
        assert product.get_cart_count() == 1
