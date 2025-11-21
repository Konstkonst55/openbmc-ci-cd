import json
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def config():
    with open("tests/webui/config.json", "r", encoding="utf-8") as file:
        return json.load(file)

@pytest.fixture(scope="session")
def logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("test_log.log"), logging.StreamHandler()]
    )
    return logging.getLogger("openbmc-tests")

@pytest.fixture(scope="session")
def driver(config, logger):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(config["implicit_wait"])
    driver.wait = WebDriverWait(driver, config["explicit_wait"])

    yield driver

    driver.quit()
    logger.info("Driver closed after test session.")