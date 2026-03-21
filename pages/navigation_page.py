class NavigationPage:
    def __init__(self, page):
        self.page = page
        self.burger_btn = page.locator("[data-test='open-menu']")
        self.close_btn = page.locator("[data-test='close-menu']")
        self.all_items_link = page.locator("[data-test='inventory-sidebar-link']")
        self.logout_link = page.locator("[data-test='logout-sidebar-link']")
        self.reset_link = page.locator("[data-test='reset-sidebar-link']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")

    def open_menu(self):
        self.burger_btn.click()
        self.logout_link.wait_for(state="visible")

    def close_menu(self):
        self.close_btn.click()
        self.logout_link.wait_for(state="hidden")

    def logout(self):
        self.open_menu()
        self.logout_link.click()

    def go_to_all_items(self):
        self.open_menu()
        self.all_items_link.click()

    def reset_app_state(self):
        self.open_menu()
        self.reset_link.click()

    def go_to_cart(self):
        self.cart_link.click()
