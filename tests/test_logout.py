import pytest
from pages.login_page import LoginPage
from pages.navigation_page import NavigationPage
from pages.inventory_page import InventoryPage


class TestLogout:

    @pytest.fixture(autouse=True)
    def login(self, page):
        LoginPage(page).login("standard_user", "secret_sauce")

    def test_logout_redirects_to_login(self, page):
        NavigationPage(page).logout()
        assert page.url == "https://www.saucedemo.com/"
        assert page.locator("#login-button").is_visible()

    def test_cannot_access_inventory_after_logout(self, page):
        NavigationPage(page).logout()
        page.goto("https://www.saucedemo.com/inventory.html")
        assert page.locator("#login-button").is_visible()

    def test_menu_opens_and_closes(self, page):
        nav = NavigationPage(page)
        nav.open_menu()
        assert page.locator("[data-test='logout-sidebar-link']").is_visible()
        nav.close_menu()
        assert not page.locator("[data-test='logout-sidebar-link']").is_visible()

    def test_all_items_link_goes_to_inventory(self, page):
        nav = NavigationPage(page)
        nav.go_to_cart()
        nav.go_to_all_items()
        assert InventoryPage(page).get_title() == "Products"

    def test_reset_clears_cart(self, page):
        inventory = InventoryPage(page)
        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1
        NavigationPage(page).reset_app_state()
        assert inventory.get_cart_count() == 0
