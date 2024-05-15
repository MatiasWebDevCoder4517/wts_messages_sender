# Standard Library
import os
import time

# External
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Project
from app.config import CONTACT_CSV_TEST, LOGGER, MAIN_CELLPHONE, PDF_FILE, SPECIAL_MESSAGE_TEST


## selenium
def find_driver_path(driver_name: str = "chromedriver.exe"):
    search_path = "."

    filepath = next(
        os.path.join(root, driver_name)
        for root, _, files in os.walk(search_path)
        if driver_name in files
    )
    return filepath


def initialize_driver(filepath: str, phone_number: str) -> WebDriverWait:
    if filepath is None:
        return None

    chrome_service = Service(executable_path=filepath)
    driver = webdriver.Chrome(service=chrome_service)

    base_url = "https://web.whatsapp.com/send?phone="
    driver.get(f"{base_url}{phone_number}")
    driver.maximize_window()
    wait = WebDriverWait(driver, 180)  # Increased timeout for slow page loads

    return wait


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
    """Retrieve the absolute file path of a PDF file, attempting to locate it within the directory structure."""
    search_path = "."
    try:
        filepath = next(
            os.path.join(root, pdf_name)
            for root, _, files in os.walk(search_path)
            if pdf_name in files
        )
        abs_path = os.path.abspath(filepath)
        LOGGER.info(f"PDF file located at: {abs_path}")
        return abs_path
    except StopIteration:
        LOGGER.error("No PDF file found!")
        return None


def send_whatsapp_message(
    wait_driver: WebDriverWait, phone_number: str, message: str, file_path: str
):

    def find_and_click_element(locator):
        element = wait_driver.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def find_and_send_keys(locator, keys):
        element = wait_driver.until(EC.presence_of_element_located(locator))
        element.send_keys(keys)
        return element

    try:
        # Step 2: Open new chat button
        time.sleep(5)
        LOGGER.info("Clicking the new chat button")
        find_and_click_element(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span',
            )
        )

        # Step 3: Search or insert new number input box
        time.sleep(5)
        LOGGER.info("Inserting the phone number")
        find_and_send_keys(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]',
            ),
            phone_number,
        )

        # Step 4: Wait for the chat to load and click it
        time.sleep(5)
        LOGGER.info("Waiting for the chat to load and click it...")
        find_and_click_element(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div',
            )
        )

        # Step 5: At this point you are in the specific chat and watching the input box for texting
        time.sleep(2)
        LOGGER.info("Clicking the message input box")
        find_and_send_keys(
            (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'),
            message + Keys.ENTER,
        )

        # Step 6: Attach button to add the PDF
        time.sleep(2)
        LOGGER.info("Clicking the attach button")
        find_and_click_element(
            (
                By.XPATH,
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span',
            )
        )

        # Step 7: Input element for file upload
        time.sleep(5)
        LOGGER.info("Uploading the PDF file")
        find_and_send_keys(
            (
                By.XPATH,
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[1]/li/div/input',
            ),
            file_path,
        )

        # Step 8: Send button for the document
        time.sleep(2)
        LOGGER.info("Clicking the send button for the document")
        find_and_click_element(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span',
            )
        )
    except TimeoutException as e:
        LOGGER.error(f"Timed out waiting for an element: {e}")
    except WebDriverException as e:
        LOGGER.error(f"WebDriver exception occurred: {e}")
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {e}")


def main():
    driver_path = find_driver_path()
    wait_driver = initialize_driver(driver_path, MAIN_CELLPHONE)
    if not wait_driver:
        LOGGER.error("Web driver is not initialized")
        return

    data_csv = load_csv_to_df(CONTACT_CSV_TEST)
    LOGGER.info("Loading CSV file...")
    if data_csv is None or data_csv.empty:
        LOGGER.error("No data to process")
        return

    data_pdf = load_pdf(PDF_FILE)
    LOGGER.info("Loading PDF file...")
    if not data_pdf:
        LOGGER.error("PDF file not found")
        return

    count = 0
    for index, row in data_csv.iterrows():
        cellphone = f'+{int(row["cellphones"])}'
        LOGGER.info(f"CELLPHONE: {cellphone} | position: {index}")
        if index == 0:
            LOGGER.info(f"Starting point to send messages... main_cellphone: {MAIN_CELLPHONE}")
            time.sleep(30)
        send_whatsapp_message(wait_driver, cellphone, SPECIAL_MESSAGE_TEST, data_pdf)
        LOGGER.info(f"Message with pdf sended -> cellphone: {cellphone} | position: {index}")
        count += 1

    LOGGER.info(f"TOTAL MESSAGES & PDFs SENDED: {count}")
    wait_driver.quit()


if __name__ == "__main__":
    main()
