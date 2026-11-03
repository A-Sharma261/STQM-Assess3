# README - Website Functionality Testing

## Project Overview
This project uses Python and Selenium WebDriver to automate testing of the registration, login, and forgot password functions on the OpenCart website.

## Files

**test_registration.py**
- Tests successful user registration.
- Tests registration with mismatched passwords.
- Tests validation errors when required fields are empty.
- Generates unique email addresses for testing.

**test_login.py**
- Tests successful login with valid credentials.
- Tests login with an incorrect password.
- Tests login with empty fields.

**test_forgot_password.py**
- Tests password reset using a registered email.
- Tests password reset using an unregistered email.
- Tests password reset with an empty email field.

**registered_emails.json**
- Stores generated email addresses used during registration testing.
- Must exist before running the registration script, initially containing `[]`.

## Requirements
- Python 3
- Selenium
- Google Chrome

Install Selenium using:

`pip install selenium`

## Running the Tests

Run each test file separately using:

`python test_registration.py`

`python test_login.py`

`python test_forgot_password.py`

## Test Results

Each script automatically opens Chrome, performs the test scenarios, and checks the expected results.

Results are displayed in the terminal as `PASS` or `FAILED/ERROR`.

The browser closes automatically after each test scenario.