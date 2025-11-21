import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@pytest.fixture
def login(driver, config, logger):
    def _login(username, password):
        try:
            driver.get(config["openbmc_url"])
            user_field = driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
            user_field.clear()
            user_field.send_keys(username)

            pass_field = driver.find_element(By.ID, "password")
            pass_field.clear()
            pass_field.send_keys(password)

            driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-button-submit']").click()
            logger.info(f"Login attempt with user '{username}'")
            return True
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    return _login

@pytest.fixture
def logout(driver, logger, config):
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
            logger.info("User logged out successfully.")
        except Exception as e:
            logger.warning(f"Logout issue: {e}, reloading main page.")
            driver.get(config["openbmc_url"])
    return _logout

@pytest.mark.usefixtures("driver")
def test_successful_login(driver, login, logout, config, logger):
    assert login(config["valid_username"], config["valid_password"]), "Login failed"
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
        driver.find_elements(By.XPATH, indicator)
        for indicator in success_indicators
    )

    logout()
    assert found, "No success indicator found after login"

def test_invalid_credentials(driver, login, config, logger):
    driver.get(config["openbmc_url"])
    assert login(config["valid_username"], config["invalid_password"]), "Login submission failed"
    time.sleep(2)

    error_indicators = [
        "//*[contains(text(), 'Invalid username or password')]",
        "//*[contains(@class, 'alert') or contains(@class, 'error') or contains(@class, 'danger')]",
        "//*[@id='login-error-alert']"
    ]

    error_found = any(
        driver.find_elements(By.XPATH, selector)
        for selector in error_indicators
    )

    try:
        login_button_visible = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-button-submit']").is_displayed()
    except:
        login_button_visible = False

    assert error_found or login_button_visible, (
        "Invalid credentials test failed: no error message and login button not visible"
    )

    logger.info("Invalid credentials test passed — system stayed on login page or showed an error message.")


def test_account_lockout(driver, login, config, logger):
    url = config["openbmc_url"]
    username = config["testuser_username"]
    wrong_password = config["invalid_password"]
    correct_password = config["testuser_password"]
    max_attempts = 3

    logger.info("Starting account lockout test...")

    for i in range(max_attempts):
        driver.get(url)
        driver.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(wrong_password)
        driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-button-submit']").click()
        time.sleep(2)

        assert "login" in driver.current_url.lower(), f"Unexpectedly left login page on attempt {i + 1}"
        logger.info(f"Attempt {i + 1}/3 with wrong password complete — still on login page.")

    driver.get(url)
    driver.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(correct_password)
    driver.find_element(By.CSS_SELECTOR, "button[data-test-id='login-button-submit']").click()
    time.sleep(2)

    assert "login" in driver.current_url.lower(), "Account not locked after 3 invalid login attempts"
    logger.info("Account lockout test passed — user still on login page after valid credentials.")

def test_power_management(driver, login, logout, config, logger):
    if "login" in driver.current_url.lower():
        assert login(config["valid_username"], config["valid_password"]), "Login failed"

    time.sleep(2)
    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='nav-button-operations']"))).click()
    time.sleep(1)

    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='nav-item-server-power-operations']"))).click()
    time.sleep(2)

    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Power') or contains(text(), 'Reboot')]")
    logout()
    assert elements, "Power management page not loaded"

def test_inventory_display(driver, login, logout, config, logger):
    if "login" in driver.current_url.lower():
        assert login(config["valid_username"], config["valid_password"]), "Login failed"

    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='nav-button-hardware-status']"))).click()
    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='nav-item-inventory']"))).click()
    time.sleep(2)

    inventory_indicators = [
        "//*[contains(text(), 'System')]",
        "//*[contains(text(), 'CPU')]",
        "//*[contains(text(), 'Memory')]",
        "//*[contains(text(), 'Storage')]"
    ]

    found = any(driver.find_elements(By.XPATH, i) for i in inventory_indicators)
    logout()
    assert found, "Inventory page did not display expected elements"

def test_event_logs_display(driver, login, logout, config, logger):
    if "login" in driver.current_url.lower():
        assert login(config["valid_username"], config["valid_password"]), "Login failed"

    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='nav-button-logs']"))).click()
    driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='nav-item-event-logs']"))).click()
    time.sleep(2)

    logs_found = driver.find_elements(By.XPATH, "//*[contains(text(), 'Event logs')]")
    logout()
    assert logs_found, "Event logs page not displayed"
