import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.test_data import LOGIN_VALID


class TestUIValidations:

    def test_login_page_title(self, page):
        assert page.title() == "Swag Labs"

    def test_login_button_is_visible(self, page):
        assert page.locator("#login-button").is_visible()

    def test_password_field_is_masked(self, page):
        assert page.locator("#password").get_attribute("type") == "password"

    def test_login_error_has_close_button(self, page):
        LoginPage(page).login("bad_user", "bad_pass")
        close_btn = page.locator(".error-button")
        assert close_btn.is_visible()
        close_btn.click()
        assert not page.locator("[data-test='error']").is_visible()

    def test_add_to_cart_button_changes_to_remove(self, page):
        LoginPage(page).login(LOGIN_VALID["username"], LOGIN_VALID["password"])
        InventoryPage(page).add_item_to_cart("sauce-labs-backpack")
        assert page.locator("[data-test='remove-sauce-labs-backpack']").is_visible()

    def test_cart_shows_empty_when_no_items(self, page):
        LoginPage(page).login(LOGIN_VALID["username"], LOGIN_VALID["password"])
        page.locator("[data-test='shopping-cart-link']").click()
        assert CartPage(page).get_item_count() == 0

    def test_checkout_form_fields_are_present(self, page):
        LoginPage(page).login(LOGIN_VALID["username"], LOGIN_VALID["password"])
        InventoryPage(page).add_item_to_cart("sauce-labs-backpack")
        page.locator("[data-test='shopping-cart-link']").click()
        CartPage(page).proceed_to_checkout()
        assert page.locator("[data-test='firstName']").is_visible()
        assert page.locator("[data-test='lastName']").is_visible()
        assert page.locator("[data-test='postalCode']").is_visible()
