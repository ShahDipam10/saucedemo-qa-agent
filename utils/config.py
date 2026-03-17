import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
VALID_USERNAME = os.getenv("VALID_USERNAME", "standard_user")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "secret_sauce")
LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
INVALID_USERNAME = os.getenv("INVALID_USERNAME", "wrong_user")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD", "wrong_pass")
