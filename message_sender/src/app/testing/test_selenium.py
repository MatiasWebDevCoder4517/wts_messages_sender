# Standard Library
import os
import time

# External
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def find_driver_path(driver_name: str = "chromedriver.exe"):
    search_path = "."

    filepath = next(
        os.path.join(root, driver_name)
        for root, _, files in os.walk(search_path)
        if driver_name in files
    )
    return filepath


def initialize_driver(filepath: str) -> webdriver:
    if filepath is None:
        return None

    chrome_service = Service(executable_path=filepath)
    driver = webdriver.Chrome(service=chrome_service)
    return driver


def test_selenium():
    filepath = find_driver_path()
    driver = initialize_driver(filepath)
    if driver is not None:
        try:
            driver.get("https://www.google.com")
            time.sleep(7)  # Hold the browser open for 5 seconds
        finally:
            driver.quit()
