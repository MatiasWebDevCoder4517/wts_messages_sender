# Local
from .config import CONTACT_CSV, CONTACT_CSV_TEST, PDF_FILE, SPECIAL_MESSAGE
from .logger import create_logger


LOGGER = create_logger()

__all__ = ["CONTACT_CSV", "SPECIAL_MESSAGE", "CONTACT_CSV_TEST", "PDF_FILE"]
