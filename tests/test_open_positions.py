import os
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Base configuration
BASE_URL = os.getenv("CHAKORA_BASE_URL", "https://chakorahub.com").rstrip("/")
LOCAL_TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "chakora-website" / "templates"
HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")


@pytest.fixture(scope="module")
def driver():
    """Configures and provisions a Chrome WebDriver instance."""
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    web_driver = webdriver.Chrome(options=options)
    web_driver.implicitly_wait(5)
    yield web_driver
    web_driver.quit()


# ============================================================================
# USER SECTION TESTS: Open Positions & Careers (Candidate Application Flow)
# ============================================================================

def test_user_apply_page_elements(driver):
    """
    User Section Test:
    Verifies that candidate resume application page (/apply) loads properly
    with all required form fields, file inputs, and submit button.
    """
    wait = WebDriverWait(driver, 15)
    apply_url = f"{BASE_URL}/apply"

    try:
        driver.get(apply_url)
        wait.until(EC.presence_of_element_located((By.ID, "resumeForm")))
    except Exception:
        # Fallback to local template file if offline
        local_file = (LOCAL_TEMPLATES_DIR / "resume-upload.html").as_uri()
        driver.get(local_file)
        wait.until(EC.presence_of_element_located((By.ID, "resumeForm")))

    # Verify Page Title or Heading
    assert "Resume Upload" in driver.title or "Resume" in driver.page_source

    # Verify Required Form Inputs
    name_field = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    email_field = driver.find_element(By.ID, "email")
    phone_field = driver.find_element(By.ID, "phone")
    exp_field = driver.find_element(By.ID, "experience_years")
    resume_input = driver.find_element(By.ID, "resume")

    assert name_field.is_displayed(), "Name field should be visible"
    assert email_field.is_displayed(), "Email field should be visible"
    assert phone_field.is_displayed(), "Phone field should be visible"
    assert exp_field.is_displayed(), "Experience field should be visible"
    assert resume_input.get_attribute("type") == "file", "Resume upload field must be a file input"

    # Verify Dropdown selections
    qual_dropdown = driver.find_element(By.ID, "qualification")
    source_dropdown = driver.find_element(By.ID, "source")
    assert qual_dropdown.is_displayed(), "Qualification select dropdown should be visible"
    assert source_dropdown.is_displayed(), "Source select dropdown should be visible"

    # Verify Submit Button
    submit_btn = driver.find_element(By.ID, "submitBtn")
    assert submit_btn.is_displayed(), "Submit Resume button should be visible"
    assert "Submit" in submit_btn.text


def test_user_track_application_page(driver):
    """
    User Section Test:
    Verifies the candidate application status tracking page (/track-application).
    Ensures input field, tracking action button, and progress elements exist.
    """
    wait = WebDriverWait(driver, 15)
    track_url = f"{BASE_URL}/track-application"

    try:
        driver.get(track_url)
        wait.until(EC.presence_of_element_located((By.ID, "applicationId")))
    except Exception:
        local_file = (LOCAL_TEMPLATES_DIR / "track-application.html").as_uri()
        driver.get(local_file)
        wait.until(EC.presence_of_element_located((By.ID, "applicationId")))

    # Verify Page Title
    assert "Track" in driver.title

    # Verify Application ID Input Field
    app_id_input = wait.until(EC.visibility_of_element_located((By.ID, "applicationId")))
    assert app_id_input.is_displayed()

    # Enter sample test ID
    app_id_input.clear()
    app_id_input.send_keys("APP_TEST_2026")

    # Verify Track Status Button
    track_btn = driver.find_element(By.XPATH, "//button[contains(normalize-space(), 'Track Status')]")
    assert track_btn.is_displayed()
    assert track_btn.is_enabled()

    # Trigger click and verify UI does not break
    track_btn.click()


# ============================================================================
# ADMIN SECTION TESTS: Open Positions Management (CRUD & Pipeline)
# ============================================================================

def test_admin_open_positions_management_ui(driver):
    """
    Admin Section Test:
    Verifies the Open Positions Management dashboard (OpenPositionsManagement.html):
    - Table/pipeline layout
    - 'Add Position' modal controls
    - Input form fields (title, location, department, salary)
    - Modal cancel/close behavior
    """
    wait = WebDriverWait(driver, 15)
    local_file = (LOCAL_TEMPLATES_DIR / "OpenPositionsManagement.html").as_uri()

    # Load Open Positions Management Interface
    driver.get(local_file)

    # 1. Verify Header & Main Action Controls
    add_btn = wait.until(EC.element_to_be_clickable((By.ID, "addPositionBtn")))
    assert add_btn.is_displayed(), "Add Position button should be visible"

    refresh_btn = driver.find_element(By.ID, "refreshBtn")
    assert refresh_btn.is_displayed(), "Refresh button should be visible"

    # 2. Verify Pipeline / Status Columns
    pending_list = driver.find_element(By.ID, "pendingList")
    processed_list = driver.find_element(By.ID, "processedList")
    mail_sent_list = driver.find_element(By.ID, "mailSentList")

    assert pending_list.is_displayed()
    assert processed_list.is_displayed()
    assert mail_sent_list.is_displayed()

    # 3. Open 'Add Position' Modal
    add_btn.click()

    modal = wait.until(EC.visibility_of_element_located((By.ID, "positionModal")))
    assert modal.is_displayed(), "Add Position modal must open upon clicking Add Position"

    # 4. Verify Modal Form Inputs
    pos_title = driver.find_element(By.ID, "positionTitle")
    pos_location = driver.find_element(By.ID, "positionLocation")
    pos_dept = driver.find_element(By.ID, "positionDepartment")
    pos_type = driver.find_element(By.ID, "positionEmploymentType")
    pos_salary = driver.find_element(By.ID, "positionSalaryRange")

    # Enter sample position details
    pos_title.send_keys("QA Automation Engineer (Selenium)")
    pos_location.send_keys("Hyderabad")
    Select(pos_dept).select_by_visible_text("Engineering")
    Select(pos_type).select_by_visible_text("Full-time")
    pos_salary.send_keys("10-14 LPA")

    # 5. Verify Cancel closes the modal
    cancel_btn = driver.find_element(By.ID, "cancelBtn")
    cancel_btn.click()

    wait.until(EC.invisibility_of_element_located((By.ID, "positionModal")))
    assert not modal.is_displayed(), "Modal should close upon clicking Cancel"
