class CartPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def is_loaded(self) -> bool:
        return self.title.is_visible()

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def proceed_to_checkout(self):
        self.checkout_button.click()

    def get_item_names(self) -> list:
        return self.page.locator(".inventory_item_name").all_inner_texts()
