class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")

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

    def add_items_to_cart(self, item_names: list):
        for item_name in item_names:
            self.add_item_to_cart(item_name)

    def go_to_cart(self):
        self.cart_icon.click()

    def get_product_names(self) -> list:
        return self.page.locator("[data-test='inventory-item-name']").all_inner_texts()

    def get_product_prices(self) -> list:
        raw = self.page.locator("[data-test='inventory-item-price']").all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def sort_by(self, option: str):
        self.sort_dropdown.select_option(option)

    def click_product(self, product_name: str):
        self.page.locator(f"[data-test='inventory-item-name']:has-text('{product_name}')").click()
