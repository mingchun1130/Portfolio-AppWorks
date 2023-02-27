import json
import logging
import os

import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from database.stylish_backend import StylishBackend
from page_objects.home_page import HomePage

BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture
def browser(request):
    browser = request.config.getoption("browser").lower()
    if browser not in ["chrome", "brave", "safari"]:
        raise ValueError("--browser value must be one of chrome/brave/safari")
    return browser


@pytest.fixture
def driver(browser):
    match browser:
        case "chrome":
            logging.info("Using Chrome browser to test")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            # driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=chrome_options)
        case "brave":
            logging.info("Using Brave browser to test")
            brave_options = webdriver.ChromeOptions()
            brave_options.binary_location = BRAVE_PATH
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
                options=brave_options,
            )
        case "safari":
            logging.info("Using Safari browser to test")
            driver = webdriver.Safari()
    driver._browser = browser
    yield driver
    logging.info("Taking final screenshot before ending test")
    allure.attach(driver.get_screenshot_as_png(), "final_screeshot", allure.attachment_type.PNG)
    driver.quit()


@pytest.fixture
def home(driver):
    _home_url = "http://54.201.140.239/index.html"
    return HomePage(driver, _home_url)


@pytest.fixture(scope="session")
def database():
    return StylishBackend()


@pytest.fixture(scope="session")
def product_detail(database):
    return database.get_all_product_detail()


@pytest.fixture(scope="session")
def product_names(product_detail):
    return product_detail[["id", "category", "title"]].drop_duplicates(subset="id").set_index("id")


@pytest.fixture(scope="session")
def all_color_code(product_detail):
    _color_code = product_detail[["color_name", "color_code"]].drop_duplicates(subset="color_name")
    return _color_code.set_index("color_name").to_dict()["color_code"]


@pytest.fixture(scope="session")
def user(worker_id):
    load_dotenv()
    user_data = json.loads(os.getenv("ACCOUNT"))
    match worker_id:
        case "master" | "gw0":
            return user_data["user0"]
        case "gw1":
            return user_data["user1"]
        case "gw2":
            return user_data["user2"]
