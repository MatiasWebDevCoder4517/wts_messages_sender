# Local
from .config import (
    CONTACT_CSV,
    CONTACT_CSV_TEST,
    MAIN_CELLPHONE,
    PDF_FILE,
    SPECIAL_MESSAGE,
    SPECIAL_MESSAGE_TEST,
)
from .logger import create_logger


LOGGER = create_logger()

__all__ = [
    "CONTACT_CSV",
    "SPECIAL_MESSAGE",
    "CONTACT_CSV_TEST",
    "PDF_FILE",
    "MAIN_CELLPHONE",
    "SPECIAL_MESSAGE_TEST",
]
