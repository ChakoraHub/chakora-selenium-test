from selenium import webdriver


def test_chakora_home_page():
    driver = webdriver.Chrome()

    try:
        driver.get("https://chakorahub.com")

        # Verify page title
        assert "ChakoraHub" in driver.title

        # Verify Home Page content
        assert "Login to ChakoraHub" in driver.page_source
        assert "Our Services" in driver.page_source
        assert "Quick Enquiry" in driver.page_source

    finally:
        driver.quit()