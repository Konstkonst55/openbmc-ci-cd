import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def login(driver):
    def _login(username, password):
        driver.get("https://localhost:2443")
        user_field = driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
        user_field.clear()
        user_field.send_keys(username)

        pass_field = driver.find_element(By.ID, "password")
        pass_field.clear()
        pass_field.send_keys(password)

        driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-button-submit']").click()
        return True
    return _login

@pytest.fixture
def logout(driver):
    def _logout():
        user_menu = driver.wait.until(EC.element_to_be_clickable((By.ID, "app-header-user__BV_toggle_")))
        user_menu.click()
        logout_button = driver.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='appHeader-link-logout']"))
        )
        logout_button.click()
        driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
        time.sleep(1)
    return _logout

@pytest.mark.usefixtures("driver")
def test_successful_login(driver, login, logout):
    assert login("root", "0penBmc")
    time.sleep(3)

    success_indicators = [
        "//*[contains(text(), 'Overview')]",
        "//*[contains(text(), 'System')]",
        "//button[contains(@id, 'app-header-user')]",
    ]

    found = any(
        driver.find_elements(By.XPATH, indicator)
        for indicator in success_indicators
    )

    logout()
    assert found

def test_invalid_credentials(driver, login):
    driver.get("https://localhost:2443")
    assert login("root", "wrongpassword")
    time.sleep(2)

    error_indicators = [
        "//*[contains(text(), 'Invalid username or password')]",
        "//*[contains(@class, 'alert')]",
    ]

    error_found = any(
        driver.find_elements(By.XPATH, selector)
        for selector in error_indicators
    )

    assert error_found