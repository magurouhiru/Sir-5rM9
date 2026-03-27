import os

from config.config import WITH_OCR
from ocr.ocr import ImageReader
from ocr.ocr_server import OcrServerImageReader

withOcr = os.getenv(WITH_OCR)


def builder() -> ImageReader:
    # if withOcr == WithOcr.ON:
    #     return EasyOcrImageReader()
    # else:
    #     return OcrServerImageReader()
    # return EasyOcrImageReader()
    return OcrServerImageReader()
