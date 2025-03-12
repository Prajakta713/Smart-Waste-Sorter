import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
    
    # Check if the title contains "Smart Waste Sorter"
    assert "Smart Waste Sorter" in driver.title
    
    # Check if the logo is visible (by finding the logo by its class name)
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

    # Wait for the file input to be visible (assuming it's visible once clicked)
    file_input = driver.find_element(By.ID, "image-upload")  # Update this ID to match your actual input element ID
    assert file_input.is_displayed(), "File input is not visible"

    # Define relative path to the image in the repo
    repo_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    image_path = os.path.join(repo_dir, "..", "static", "images", "image.png")  # Go one level up and join to the image path

    # Send the image path to the file input field
    file_input.send_keys(image_path)

    # Optionally, click on the "Submit" button if needed (e.g., if there's a submit button after uploading)
    # submit_button = driver.find_element(By.ID, "submit-button")  # Adjust the ID as needed
    # submit_button.click()

    # Assert that the upload was successful, based on your app's behavior after upload
    # For example, you can check if a success message or result is displayed after the image is uploaded
    # success_message = driver.find_element(By.ID, "upload-success")
    # assert success_message.is_displayed(), "Upload was not successful"
