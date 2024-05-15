# Standard Library
from os import getenv

# External
from dotenv import load_dotenv


load_dotenv()

CONTACT_CSV = getenv("CONTACT_CSV", "No csv has found")  ## ORIGINAL
SPECIAL_MESSAGE = getenv("SPECIAL_MESSAGE", "No message has found")
SPECIAL_MESSAGE_TEST = (
    "TESTING: TESTEANDO FUNCIONALIDAD ENVIO AUTOMATICO DE MENSAJES!!, POR FAVOR NO RESPONDER"
)
PDF_FILE = getenv("PDF_FILE", "No pdf has found")
MAIN_CELLPHONE = getenv("MAIN_CELLPHONE", "No main cellphone has found")

CONTACT_CSV_TEST = getenv("CONTACT_CSV_TEST", "No csv_test has found")  ## for testing
