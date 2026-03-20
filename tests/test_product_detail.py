import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage


class TestProductDetail:

    @pytest.fixture(autouse=True)
    def login(self, page):
        LoginPage(page).login("standard_user", "secret_sauce")

    def test_clicking_product_opens_detail_page(self, page):
        inventory = InventoryPage(page)
        inventory.click_product("Sauce Labs Backpack")
        product = ProductPage(page)
        assert product.is_loaded()
        assert product.get_name() == "Sauce Labs Backpack"

    def test_product_detail_shows_description(self, page):
        InventoryPage(page).click_product("Sauce Labs Backpack")
        product = ProductPage(page)
        desc = product.get_description()
        assert desc is not None and len(desc) > 0

    def test_product_detail_shows_price(self, page):
        InventoryPage(page).click_product("Sauce Labs Backpack")
        product = ProductPage(page)
        assert product.get_price() == "$29.99"
        assert product.get_price_as_float() == 29.99

    def test_add_to_cart_from_detail_page(self, page):
        InventoryPage(page).click_product("Sauce Labs Backpack")
        product = ProductPage(page)
        product.add_to_cart()
        assert product.get_cart_count() == 1

    def test_back_button_returns_to_inventory(self, page):
        inventory = InventoryPage(page)
        inventory.click_product("Sauce Labs Backpack")
        ProductPage(page).go_back()
        assert inventory.is_loaded()
        assert inventory.get_title() == "Products"
