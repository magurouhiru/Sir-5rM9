import importlib.util
from logging import Logger

from .ocr_server import OCRServer


def builder(logger: Logger):
    easy_ocr_spec = importlib.util.find_spec("easyocr")
    if easy_ocr_spec is not None:
        from .easy_ocr import EasyOCR

        return EasyOCR(logger)

    return OCRServer(logger)
