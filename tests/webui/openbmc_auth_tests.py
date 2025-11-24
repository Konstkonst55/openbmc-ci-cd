import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@pytest.fixture
def login(driver):
    def _login(username, password):
        try:
            driver.get("https://localhost:2443")
            user_field = driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
            user_field.clear()
            user_field.send_keys(username)

            pass_field = driver.find_element(By.ID, "password")
            pass_field.clear()
            pass_field.send_keys(password)

            driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-button-submit']").click()
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    return _login

@pytest.fixture
def logout(driver):
    def _logout():
        try:
            user_menu = driver.wait.until(EC.element_to_be_clickable((By.ID, "app-header-user__BV_toggle_")))
            user_menu.click()
            logout_button = driver.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='appHeader-link-logout']"))
            )
            logout_button.click()
            driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
            time.sleep(1)
        except Exception as e:
            print(f"Logout issue: {e}, reloading main page.")
            driver.get("https://localhost:2443")
    return _logout

def test_successful_login(driver, login, logout):
    assert login("root", "0penBmc"), "Login failed"
    time.sleep(3)

    success_indicators = [
        "//*[contains(text(), 'Overview')]",
        "//*[contains(text(), 'System')]",
        "//*[contains(text(), 'Dashboard')]",
        "//*[contains(text(), 'Welcome')]",
        "//*[contains(@class, 'dashboard')]",
        "//*[contains(@class, 'overview')]",
        "//button[contains(@id, 'app-header-user')]",
        "//*[contains(@data-test-id, 'nav-button')]"
    ]

    found = any(
        len(driver.find_elements(By.XPATH, indicator)) > 0
        for indicator in success_indicators
    )

    logout()
    assert found, "No success indicator found after login"

def test_invalid_credentials(driver, login):
    driver.get("https://localhost:2443")
    assert login("root", "wrongpassword"), "Login submission failed"
    time.sleep(2)

    error_indicators = [
        "//*[contains(text(), 'Invalid username or password')]",
        "//*[contains(@class, 'alert') or contains(@class, 'error') or contains(@class, 'danger')]",
        "//*[@id='login-error-alert']"
    ]

    error_found = any(
        len(driver.find_elements(By.XPATH, selector)) > 0
        for selector in error_indicators
    )

    try:
        login_button_visible = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-button-submit']").is_displayed()
    except:
        login_button_visible = False

    assert error_found or login_button_visible, (
        "Invalid credentials test failed: no error message and login button not visible"
    )

def test_power_management(driver, login, logout):
    if "login" in driver.current_url.lower():
        assert login("root", "0penBmc"), "Login failed"

    time.sleep(2)
    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='nav-button-operations']"))).click()
    time.sleep(1)

    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='nav-item-server-power-operations']"))).click()
    time.sleep(2)

    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Power') or contains(text(), 'Reboot')]")
    logout()
    assert len(elements) > 0, "Power management page not loaded"

def test_inventory_display(driver, login, logout):
    if "login" in driver.current_url.lower():
        assert login("root", "0penBmc"), "Login failed"

    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='nav-button-hardware-status']"))).click()
    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='nav-item-inventory']"))).click()
    time.sleep(2)

    inventory_indicators = [
        "//*[contains(text(), 'System')]",
        "//*[contains(text(), 'CPU')]",
        "//*[contains(text(), 'Memory')]",
        "//*[contains(text(), 'Storage')]"
    ]

    found = any(len(driver.find_elements(By.XPATH, i)) > 0 for i in inventory_indicators)
    logout()
    assert found, "Inventory page did not display expected elements"

def test_event_logs_display(driver, login, logout):
    if "login" in driver.current_url.lower():
        assert login("root", "0penBmc"), "Login failed"

    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='nav-button-logs']"))).click()
    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='nav-item-event-logs']"))).click()
    time.sleep(2)

    logs_found = driver.find_elements(By.XPATH, "//*[contains(text(), 'Event logs')]")
    logout()
    assert len(logs_found) > 0, "Event logs page not displayed"