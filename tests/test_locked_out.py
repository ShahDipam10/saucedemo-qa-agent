import pytest
from playwright.sync_api import Page, expect

@pytest.mark.login
def test_locked_out_user_login(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page.locator('[data-test="error"]')).to_be_visible()
    expect(page.locator("h3")).to_contain_text("Sorry, this user has been locked out.")
