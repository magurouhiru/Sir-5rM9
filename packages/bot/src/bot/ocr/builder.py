# from ocr.easy_ocr import EasyOcrImageReader
from core import settings

from ocr.ocr_server import OcrServerImageReader


def builder():
    # if settings.with_ocr_server:
    #     return create_ocr_server_reader()
    # else:
    #     return create_easy_ocr_reader()
    return create_ocr_server_reader()


# def create_easy_ocr_reader():
#     return EasyOcrImageReader()


def create_ocr_server_reader():
    base_url = settings.ocr_server_path
    return OcrServerImageReader(base_url=base_url)
