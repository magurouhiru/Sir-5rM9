from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dev_mode: bool = False
    with_gcp_token: bool = True
    ocr_server_path: str = ""


settings = Settings()
