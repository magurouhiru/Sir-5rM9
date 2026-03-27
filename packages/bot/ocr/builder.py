import os

from config.config import WITH_OCR, WithOcr
from ocr.easy_ocr import EasyOcrImageReader
from ocr.ocr import ImageReader
from ocr.ocr_server import OcrServerImageReader

withOcr = os.getenv(WITH_OCR)


def builder() -> ImageReader:
    if withOcr == WithOcr.ON.value:
        return create_easy_ocr_reader()
    else:
        return create_ocr_server_reader()


def create_easy_ocr_reader():
    return EasyOcrImageReader()


def create_ocr_server_reader():
    return OcrServerImageReader()
