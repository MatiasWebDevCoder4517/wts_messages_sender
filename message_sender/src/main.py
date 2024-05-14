# Standard Library
import os

# External
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Project
from app.config import CONTACT_CSV_TEST, LOGGER, PDF_FILE, SPECIAL_MESSAGE


## selenium
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


## main logic
def load_csv_to_df(filename: str):
    """Load CSV data into a DataFrame, attempting different encodings if necessary"""

    search_path = "."
    try:
        filepath = next(
            os.path.join(root, filename)
            for root, _, files in os.walk(search_path)
            if filename in files
        )
        return pd.read_csv(filepath, encoding="utf-8")
    except StopIteration:
        LOGGER.error("No CSV file found!")
        return None
    except UnicodeDecodeError:
        try:
            LOGGER.info("Retrying read CSV with latin1...")
            return pd.read_csv(filepath, encoding="latin1")
        except UnicodeDecodeError:
            LOGGER.info("Retrying read CSV with cp1252...")
            return pd.read_csv(filepath, encoding="cp1252")


def load_pdf(pdf_name: str):
    """Retrieve the file path of a PDF file, attempting to locate it within the directory structure."""
    search_path = "."
    try:
        filepath = next(
            os.path.join(root, pdf_name)
            for root, _, files in os.walk(search_path)
            if pdf_name in files
        )
        LOGGER.info(f"PDF file located at: {filepath}")
        return filepath
    except StopIteration:
        LOGGER.error("No PDF file found!")
        return None


def send_whatsapp_message(driver, phone_number, message: str, file_path: str):
    base_url = "https://web.whatsapp.com/send?phone="
    driver.get(f"{base_url}{phone_number}")

    # Wait for the page to load

    wait = WebDriverWait(driver, 60)
    try:
        # Wait for the message box to be clickable
        try:
            input_box = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[@title="Type a message"]'))
            )
            ##input_box = wait.until(
            ##    EC.element_to_be_clickable((By.XPATH, '//div[@title="Type a message"]'))
            ##)
        except TimeoutException:
            driver.save_screenshot("debug_screenshot.png")
            LOGGER.error(f"Timed out waiting for an element: {e}")
            return

        input_box.click()
        input_box.send_keys(message)
        input_box.send_keys(Keys.ENTER)

        # Attach file - click the attach button
        attach_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-testid="clip"]'))
        )
        attach_btn.click()

        # Click on the 'document' icon
        document_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        document_btn.send_keys(file_path)  # Directly send the file path to the input

        # Wait for send button to be clickable after file is loaded and then click send
        send_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-testid="send"]'))
        )
        send_button.click()

    except Exception as e:
        LOGGER.error(f"Failed to send message to {phone_number}: {e}")


def main():
    driver_path = find_driver_path()
    driver = initialize_driver(driver_path)
    if not driver:
        LOGGER.error("Web driver is not initialized")
        return

    data_csv = load_csv_to_df(CONTACT_CSV_TEST)  # change later to the original
    if data_csv is None or data_csv.empty:
        LOGGER.error("No data to process")
        return

    data_pdf = load_pdf(PDF_FILE)
    if not data_pdf:
        LOGGER.error("PDF file not found")
        return

    for _, row in data_csv.iterrows():
        cellphone = f'+{int(row["cellphones"])}'
        LOGGER.info(f"CELLPHONE: {cellphone}")
        send_whatsapp_message(driver, cellphone, SPECIAL_MESSAGE, data_pdf)

    LOGGER.info("All messages have been scheduled.")
    driver.quit()


if __name__ == "__main__":
    main()
