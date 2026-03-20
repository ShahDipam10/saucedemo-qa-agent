import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestSorting:

    @pytest.fixture(autouse=True)
    def login(self, page):
        LoginPage(page).login("standard_user", "secret_sauce")

    def test_default_sort_is_name_a_to_z(self, page):
        inventory = InventoryPage(page)
        names = inventory.get_product_names()
        assert names == sorted(names)

    def test_sort_name_z_to_a(self, page):
        inventory = InventoryPage(page)
        inventory.sort_by("za")
        names = inventory.get_product_names()
        assert names == sorted(names, reverse=True)

    def test_sort_price_low_to_high(self, page):
        inventory = InventoryPage(page)
        inventory.sort_by("lohi")
        prices = inventory.get_product_prices()
        assert prices == sorted(prices)

    def test_sort_price_high_to_low(self, page):
        inventory = InventoryPage(page)
        inventory.sort_by("hilo")
        prices = inventory.get_product_prices()
        assert prices == sorted(prices, reverse=True)

    def test_sort_name_a_to_z_explicit(self, page):
        inventory = InventoryPage(page)
        inventory.sort_by("hilo")
        inventory.sort_by("az")
        names = inventory.get_product_names()
        assert names == sorted(names)
