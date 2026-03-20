class ProductPage:
    def __init__(self, page):
        self.page = page
        self.name = page.locator("[data-test='inventory-item-name']")
        self.description = page.locator("[data-test='inventory-item-desc']")
        self.price = page.locator("[data-test='inventory-item-price']")
        self.add_to_cart_btn = page.locator("[data-test^='add-to-cart']")
        self.back_btn = page.locator("[data-test='back-to-products']")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def get_name(self) -> str:
        return self.name.inner_text()

    def get_description(self) -> str:
        return self.description.inner_text()

    def get_price(self) -> str:
        return self.price.inner_text()

    def get_price_as_float(self) -> float:
        return float(self.price.inner_text().replace("$", ""))

    def add_to_cart(self):
        self.add_to_cart_btn.click()

    def go_back(self):
        self.back_btn.click()

    def is_loaded(self) -> bool:
        return self.name.is_visible()

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0
