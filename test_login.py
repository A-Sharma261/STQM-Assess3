from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://opencart.abstracta.us/index.php?route=account/login"

fields = ["input-email", "input-password"]

tests = [
    ["test.student098@gmail.com", "Password123"],
    ["test.student098@gmail.com", "WrongPassword123"],
    ["",""]
]

expected = ["success", "password_error","empty_error"]

for i, inputs in enumerate(tests):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(URL)

        for field, value in zip(fields,inputs):
            driver.find_element(By.ID, field).send_keys(value)

        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        def login_error(d):
            return any(
                "no match for e-mail address and/or password" in element.text.lower()
                for element in d.find_elements(By.CSS_SELECTOR, ".alert-danger")
                if element.is_displayed()
            )
        
        if expected[i] == "success":
            wait.until(lambda d: "route=account/account" in d.current_url)
            wait.until(lambda d: any(
                element.is_displayed()
                for element in d.find_elements(By.CSS_SELECTOR, 'a[href*="route=account/logout"]')
            ))
        elif expected[i] == "password_error":
            wait.until(login_error)
        elif expected[i] == "empty_error":
            wait.until(login_error)
            assert all(
                driver.find_element(By.ID,field).get_attribute("value") == ""
                for field in fields
                ), "Expected both login fields to remain empty"
        
        print(f"Scenario {i+1}: PASS")
        
    except Exception as error:
        print(f"Scenario {i+1}: FAILED/ERROR - {error}")
        
    finally:
        driver.quit()