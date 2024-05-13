# Standard Library
from os import getenv

# External
from dotenv import load_dotenv


load_dotenv()

CONTACT_CSV = "cellphones.csv"  ## ORIGINAL

CONTACT_CSV_TEST = "cellphones_test.csv"  ## for testing
SPECIAL_MESSAGE = getenv("SPECIAL_MESSAGE", "No message has found")

PDF_FILE_TEST = "Michelle_y_Nicolas.pdf"
