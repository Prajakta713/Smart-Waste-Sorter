import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytest

# Setup for headless Chrome
@pytest.fixture
def driver():
    options = Options()
    options.headless = True  # Running the browser in headless mode (without GUI)
    driver = webdriver.Chrome(executable_path=r"C:\Users\Prajakta\Downloads\chromedriver\chromedriver-win64\chromedriver.exe", options=options)  # Adjust the path
    yield driver
    driver.quit()

def test_home_page(driver):
    driver.get('http://localhost:5000')  # Use the URL of your Flask app
    assert "Smart Waste Sorter" in driver.title
    element = driver.find_element(By.TAG_NAME, "h1")
    assert "Welcome to the Smart Waste Sorter" in element.text

def test_upload_image(driver):
    # Local path to the image in your repository (adjust according to your project structure)
    image_path = os.path.join(os.getcwd(), 'static', 'images', 'image.png')  # Adjust the path to your image file

    # Open the homepage of your Flask app
    driver.get('http://localhost:5000')
    
    # Locate the file input element for the image upload
    upload_input = driver.find_element(By.NAME, "file")  # Ensure the input name matches your form field

    # Upload the image
    upload_input.send_keys(image_path)
    
    # Submit the form (if there's a submit button)
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    
    # Allow time for the Flask app to process the image and show the result
    time.sleep(5)  # Increased sleep time to ensure image processing completes
    
    # Check if the results page has the expected content (check for a detected category or image result)
    assert "Smart Waste Sorter" in driver.title  # Check the title to verify it reached the result page
    assert "Plastic" in driver.page_source  # Check if the detected category is in the page (you can change based on actual result)
