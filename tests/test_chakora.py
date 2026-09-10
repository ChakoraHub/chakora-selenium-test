import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def test_chakora_student_home_page():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    try:
        # Open ChakoraHub
        driver.get("https://chakorahub.com")

        # Get credentials from environment variables
        email = os.getenv("CHAKORA_STUDENT_EMAIL")
        password = os.getenv("CHAKORA_STUDENT_PASSWORD")

        assert email, "CHAKORA_STUDENT_EMAIL is not set"
        assert password, "CHAKORA_STUDENT_PASSWORD is not set"

        # Select Student login
        login_type = wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "select")
            )
        )

        Select(login_type).select_by_visible_text("Student")

        # Enter email
        email_field = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Enter your Email or Phone']")
            )
        )
        email_field.send_keys(email)

        # Enter password
        password_field = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Enter your password']")
            )
        )
        password_field.send_keys(password)

        # Click Login
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Login']")
            )
        )
        login_button.click()

        # Verify student Home/Resources page
        dashboard = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(normalize-space(), 'Learning Resources Dashboard')]"
                )
            )
        )

        assert dashboard.is_displayed()

        # Verify important Home page sections
        assert "Resources" in driver.page_source
        assert "Syllabus" in driver.page_source
        assert "Meeting hours" in driver.page_source
        assert "Enquiry" in driver.page_source
        assert "Calendar" in driver.page_source

    finally:
        driver.quit()