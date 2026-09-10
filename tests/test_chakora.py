from selenium import webdriver


def test_chakora_website():
    driver = webdriver.Chrome()

    driver.get("https://chakorahub.com")

    assert "Chakora" in driver.title

    driver.quit()