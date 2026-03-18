import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
CDP_URL = os.getenv("CDP_URL", "")
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function")
def page(request):
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    pg = context.new_page()
    pg.goto(BASE_URL)
    yield pg

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{request.node.name}.png")
        pg.screenshot(path=screenshot_path)

    context.close()
    browser.close()
    pw.stop()
