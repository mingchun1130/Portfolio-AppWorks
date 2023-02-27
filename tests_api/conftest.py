import json
import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from database.stylish_backend import StylishBackend


@pytest.fixture(scope="session")
def database():
    return StylishBackend()


@pytest.fixture(scope="session")
def valid_user_account(worker_id):
    load_dotenv()
    user_data = json.loads(os.getenv("ACCOUNT"))
    match worker_id:
        case "master" | "gw0":
            return user_data["user0"]
        case "gw1":
            return user_data["user1"]
        case "gw2":
            return user_data["user2"]


@pytest.fixture(scope="session")
def db_user_data(database: StylishBackend, valid_user_account: dict) -> dict:
    return database.get_user_data_by_email(valid_user_account["email"])


@pytest.fixture(scope="session")
def db_products():
    df = StylishBackend().get_all_product_detail()
    df["main_image"] = df.agg("http://54.201.140.239/assets/{0[id]}/{0[main_image]}".format, axis=1)
    df["image"] = df.agg("http://54.201.140.239/assets/{0[id]}/{0[image]}".format, axis=1)
    return df


@pytest.fixture
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    yield driver
    driver.quit()
