class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.success_message = page.locator(".complete-header")
        self.error_message = page.locator("[data-test='error']")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_overview(self):
        self.continue_button.click()

    def finish_order(self):
        self.finish_button.click()

    def get_success_message(self) -> str:
        return self.success_message.inner_text()

    def is_order_complete(self) -> bool:
        return self.success_message.is_visible()

    def get_error_message(self) -> str:
        return self.error_message.inner_text()

    def get_overview_item_names(self) -> list:
        return self.page.locator(".cart_item .inventory_item_name").all_inner_texts()

    def get_item_total(self) -> float:
        raw_text = self.page.locator(".summary_subtotal_label").inner_text()
        return float(raw_text.split("$")[-1])

    def get_tax_amount(self) -> float:
        raw_text = self.page.locator(".summary_tax_label").inner_text()
        return float(raw_text.split("$")[-1])

    def get_total(self) -> float:
        raw_text = self.page.locator(".summary_total_label").inner_text()
        return float(raw_text.split("$")[-1])
