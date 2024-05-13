# Standard Library
import os
from datetime import datetime, time

# External
import pandas as pd
import pywhatkit

# Project
from app.config import CONTACT_CSV_TEST, LOGGER, SPECIAL_MESSAGE  # #PDF_FILE_TEST


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


# Todo: Build a function that retrieve a pdf file same as function 'load_csv_to_df'
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


def main():
    data_csv = load_csv_to_df(CONTACT_CSV_TEST)  ## change later to the original
    if data_csv is None or data_csv.empty:
        LOGGER.error("No data to process")
        return

    ##data_pdf = load_pdf(PDF_FILE_TEST)

    now = datetime.now()
    hour = now.hour
    minute = now.minute + 1

    for index, row in data_csv.iterrows():
        try:
            cellphone = int(row["cellphones"])
            LOGGER.info(f"Sending message to {cellphone}: {SPECIAL_MESSAGE} | position: {index}")
            print("Step..")

            # Todo: Send the whatsapp message + pdf file retrieved

            pywhatkit.sendwhatmsg(cellphone, SPECIAL_MESSAGE, hour, minute)
            time.sleep(6)
        except Exception as e:
            LOGGER.error(f"Failed to send message to {cellphone}: {e}")

    LOGGER.info("All messages have been scheduled.")


if __name__ == "__main__":
    main()
