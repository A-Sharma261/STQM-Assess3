import json
from pathlib import Path 
from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://opencart.abstracta.us/index.php?route=account/register"

fields = [
    "input-firstname",
    "input-lastname",
    "input-email",
    "input-telephone",
    "input-password",
    "input-confirm"
]

emails = [f"test.student.{uuid4().hex}@gmail.com" for _ in range(2)]

storage_path = Path(__file__).with_name("registered_emails.json")
testcases = json.loads(storage_path.read_text())
testcases.append({"testcase": len(testcases) + 1, "emails": emails})
storage_path.write_text(json.dumps(testcases,indent=4) + "\n")

tests = [
    [
        "test", "student", emails[0], "0410395874",
        "Password123", "Password123"
    ],
    [
        "test", "student", emails[1], "0410395874",
        "Password123", "WrongPassword123"
    ],
    [
        "","","","","",""
    ],
]

expected = ["success", "password_error", "required_error"]

for i, inputs in enumerate(tests):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver,15)

    try:
        driver.get(URL)

        for field, value in zip(fields,inputs):
            driver.find_element(By.ID, field).send_keys(value)

        if i < 2:
            check = driver.find_element(By.NAME, "agree")
            driver.execute_script("arguments[0].click();", check)

        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        def validation_messages(d):
            return [
                element.text.lower()
                for element in d.find_elements(By.CSS_SELECTOR, ".text-danger")
                if element.is_displayed()
            ]

        if expected[i] == "success":
            wait.until(lambda d: "route=account/success" in d.current_url)
        elif expected[i] == "password_error":
            wait.until(lambda d: any("password confirmation does not match password" in message
                for message in validation_messages(d)))
        elif expected[i] == "required_error":
            wait.until(lambda d: all(
                any(field_name in message for message in validation_messages(d))
                for field_name in ("first name", "last name", "e-mail", "telephone", "password")
            ))

        print(f"Scenario {i+1}: PASS")

    except Exception as error:
        print(f"Scenario {i+1}: FAILED/ERROR - {error}")

    finally:
        driver.quit()
