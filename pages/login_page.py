class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        # wait for either inventory page or error — whichever comes first
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self) -> str:
        return self.error_message.inner_text()

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()
