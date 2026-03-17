import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
CDP_URL = os.getenv("CDP_URL", "")


@pytest.fixture(scope="function")
def page():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    pg = context.new_page()
    pg.goto(BASE_URL)
    yield pg
    context.close()
    browser.close()
    pw.stop()
