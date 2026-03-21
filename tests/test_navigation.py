import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.navigation_page import NavigationPage
from pages.cart_page import CartPage


class TestNavigation:

    @pytest.fixture(autouse=True)
    def login(self, page):
        LoginPage(page).login("standard_user", "secret_sauce")

    def test_inventory_page_has_correct_title(self, page):
        assert InventoryPage(page).get_title() == "Products"

    def test_cart_icon_navigates_to_cart(self, page):
        NavigationPage(page).go_to_cart()
        assert CartPage(page).is_loaded()
        assert page.url == "https://www.saucedemo.com/cart.html"

    def test_all_6_products_are_displayed(self, page):
        assert len(InventoryPage(page).get_product_names()) == 6

    def test_all_products_have_prices(self, page):
        prices = InventoryPage(page).get_product_prices()
        assert len(prices) == 6
        assert all(p > 0 for p in prices)

    def test_all_products_have_images(self, page):
        images = page.locator(".inventory_item img").all()
        assert len(images) == 6
        for img in images:
            assert img.get_attribute("src") not in (None, "")

    def test_cart_empty_by_default(self, page):
        assert InventoryPage(page).get_cart_count() == 0
