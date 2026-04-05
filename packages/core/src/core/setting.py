from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dev_mode: bool = False
    with_ocr_server: bool = True
    with_gcp_token: bool = False
    ocr_server_path: str = "http://localhost:8000"


settings = Settings()
