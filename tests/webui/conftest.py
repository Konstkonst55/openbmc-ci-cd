import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def config():
    return {
        "openbmc_url": "https://localhost:2443",
        "valid_username": "root", 
        "valid_password": "0penBmc",
        "invalid_password": "wrongpassword",
        "testuser_username": "testuser",
        "testuser_password": "TestPass123",
        "implicit_wait": 5,
        "explicit_wait": 5
    }

@pytest.fixture(scope="session")
def driver(config):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(config["implicit_wait"])
    driver.wait = WebDriverWait(driver, config["explicit_wait"])

    yield driver
    driver.quit()