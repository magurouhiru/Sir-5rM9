from google.auth.transport.requests import Request
from google.oauth2 import id_token

# from ocr.easy_ocr import EasyOcrImageReader
from ocr.ocr_server import OcrServerImageReader
from settings.settings import settings


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
    if settings.with_gcp_token:
        token = id_token.fetch_id_token(Request(), base_url)
        headers = {
            "Authorization": f"Bearer {token}",
        }
    else:
        headers = {}
    return OcrServerImageReader(base_url=base_url, headers=headers)
