from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://opencart.abstracta.us/index.php?route=account/forgotten"

tests = [
    "test.student098@gmail.com",
    f"unregistered.{uuid4().hex}@example.com",
    ""
]

expected = ["success", "email_error","empty_error"]

for i, email in enumerate(tests):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(URL)

        email_field = driver.find_element(By.ID, "input-email")
        assert email_field.is_displayed(), "Expected the email field to be visible"
        email_field.send_keys(email)

        reset_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        assert reset_button.is_displayed() and reset_button.is_enabled(), (
            "Expected the reset button to be visible and enabled"
        )
        reset_button.click()

        def email_error(d):
            return  any(
                "e-mail address was not found in our records" in element.text.lower()
                for element in d.find_elements(By.CSS_SELECTOR, ".alert-danger")
                if element.is_displayed()
            )
        
        if expected[i] == "success":
            wait.until(lambda d: "route=account/login" in d.current_url)
            wait.until(lambda d: any(
                "email" in element.text.lower().replace("e-mail", "email")
                and "sent" in element.text.lower()
                for element in d.find_elements(By.CSS_SELECTOR, ".alert-success")
                if element.is_displayed()
            ))
        elif expected[i] == "email_error":
            wait.until(email_error)
            assert "route=account/forgotten" in driver.current_url
        elif expected[i] == "empty_error":
            wait.until(email_error)
            assert "route=account/forgotten" in driver.current_url
            assert driver.find_element(By.ID, "input-email").get_attribute("value") == "", (
                "Expected the email field to remain empty"
            )

        print(f"Scenario {i+1}: PASS")
        
    except Exception as error:
        print(f"Scenario {i+1}: FAILED/ERROR - {error}")
        
    finally:
        driver.quit()