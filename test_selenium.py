import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time
import requests

# Ensure Flask is running before tests
def wait_for_flask_app():
    url = 'http://localhost:5000'
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Flask app is running!")
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    raise Exception("Flask app did not start in time.")

# Wait for Flask app before running tests
wait_for_flask_app()

# Setup for headless Chrome
@pytest.fixture
def driver():
    options = Options()
    options.headless = True  # Running the browser in headless mode (without GUI)
    
    # Path to chromedriver
    chromedriver_path = r"C:\Users\Prajakta\Downloads\chromedriver\chromedriver-win64\chromedriver.exe"  # Adjust the path
    service = Service(executable_path=chromedriver_path)  # Using Service

    driver = webdriver.Chrome(service=service, options=options)  # Initialize the driver with service
    yield driver
    driver.quit()

def test_home_page(driver):
    driver.get('http://localhost:5000')  # Use the URL of your Flask app
    
    # Check if the title contains "Smart Waste Sorter"
    assert "Smart Waste Sorter" in driver.title
    
    # Check if the logo is visible
    logo = driver.find_element(By.CLASS_NAME, "logo")
    assert logo.is_displayed(), "Logo is not displayed"
    
    # Check if the header contains the correct text
    header = driver.find_element(By.TAG_NAME, "h1")
    assert "Smart Waste Sorter - Waste Detection" in header.text
    
    # Check if the "About Us" section is visible
    about_us_section = driver.find_element(By.ID, "about-us")
    assert about_us_section.is_displayed(), "About Us section is not visible"
    
    # Check if the "Our Goals" section is visible
    our_goals_section = driver.find_element(By.ID, "our-goals")
    assert our_goals_section.is_displayed(), "Our Goals section is not visible"
    
    # Check if the "Detect Image" button exists
    detect_image_button = driver.find_element(By.XPATH, "//a[@href='#detect-image']")
    assert detect_image_button.is_displayed(), "Detect Image button is not visible"
    
    # Click on the "Detect Image" button
    detect_image_button.click()

    # Wait for the file input to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "image-upload"))
    )

    # Define relative path to the image
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(repo_dir, "..", "static", "images", "image.png")

    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image file at {image_path} does not exist.")
    
    # Send the image path to the file input field
    file_input = driver.find_element(By.ID, "image-upload")
    file_input.send_keys(image_path)

    # Optionally, click on the "Submit" button if needed
    # submit_button = driver.find_element(By.ID, "submit-button")
    # submit_button.click()

    # You can also assert upload success based on your app's behavior
    # success_message = driver.find_element(By.ID, "upload-success")
    # assert success_message.is_displayed(), "Upload was not successful"
