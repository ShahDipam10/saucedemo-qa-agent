import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
CDP_URL = os.getenv("CDP_URL", "")  # e.g. http://localhost:9222


def pytest_addoption(parser):
    parser.addoption("--cdp", action="store_true", default=False, help="Use existing Chrome session via CDP")


@pytest.fixture(scope="session")
def browser_context(pytestconfig):
    use_cdp = pytestconfig.getoption("--cdp") or bool(CDP_URL)
    pw = sync_playwright().start()

    if use_cdp and CDP_URL:
        browser = pw.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        yield context
        pw.stop()
    else:
        browser = pw.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        yield context
        context.close()
        browser.close()
        pw.stop()


@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    page.goto(BASE_URL)
    yield page
    page.close()
