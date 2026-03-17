class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def is_loaded(self) -> bool:
        return self.title.is_visible()

    def get_title(self) -> str:
        return self.title.inner_text()

    def add_item_to_cart(self, item_name: str):
        self.page.locator(f"[data-test='add-to-cart-{item_name}']").click()

    def remove_item_from_cart(self, item_name: str):
        self.page.locator(f"[data-test='remove-{item_name}']").click()

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def go_to_cart(self):
        self.cart_icon.click()
