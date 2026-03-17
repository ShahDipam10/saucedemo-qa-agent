import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
CDP_URL = os.getenv("CDP_URL", "")


def pytest_addoption(parser):
    parser.addoption("--cdp", action="store_true", default=False, help="Use existing Chrome session via CDP")


@pytest.fixture(scope="function")
def page(pytestconfig):
    use_cdp = pytestconfig.getoption("--cdp") or bool(CDP_URL)
    pw = sync_playwright().start()

    if use_cdp and CDP_URL:
        browser = pw.chromium.connect_over_cdp(CDP_URL)
        context = browser.new_context()
        pg = context.new_page()
        pg.goto(BASE_URL)
        yield pg
        context.close()
        pw.stop()
    else:
        browser = pw.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        pg = context.new_page()
        pg.goto(BASE_URL)
        yield pg
        context.close()
        browser.close()
        pw.stop()
