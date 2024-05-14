# Standard Library
from os import getenv

# External
from dotenv import load_dotenv


load_dotenv()

CONTACT_CSV = getenv("CONTACT_CSV", "No csv has found")  ## ORIGINAL
SPECIAL_MESSAGE = getenv("SPECIAL_MESSAGE", "No message has found")
PDF_FILE = getenv("PDF_FILE", "No pdf has found")

CONTACT_CSV_TEST = getenv("CONTACT_CSV_TEST", "No csv_test has found")  ## for testing
