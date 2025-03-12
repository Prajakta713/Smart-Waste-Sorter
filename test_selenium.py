from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest

# Setup for headless Chrome
@pytest.fixture
def driver():
    options = Options()
    options.headless = True  # Running the browser in headless mode (without GUI)
    driver = webdriver.Chrome(executable_path=r"C:\path\to\chromedriver.exe", options=options)  # Adjust the path
    yield driver
    driver.quit()

def test_home_page(driver):
    driver.get('http://localhost:5000')  # Use the URL of your Flask app
    assert "Smart Waste Sorter" in driver.title
    element = driver.find_element_by_tag_name("h1")
    assert "Welcome to the Smart Waste Sorter" in element.text
