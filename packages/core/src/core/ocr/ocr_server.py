import io
import time
from logging import Logger

from aiohttp import ClientSession, FormData
from aiohttp.typedefs import LooseHeaders
from api import OCRResultList, SearchParams
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from PIL import Image

from core import settings

from .ocr import OCR


class OCRServer(OCR):
    def __init__(self, logger: Logger):
        super().__init__()
        self.base_url = settings.ocr_server_path
        self.logger = logger
        self.logger.info("init: OCRServer with base_url=%s", self.base_url)
        if self.base_url is None or self.base_url == "":
            raise ValueError(
                "OCR server の URL が設定されていません。環境変数 OCR_SERVER_PATH を確認してください。"
            )

    def get_headers(self) -> LooseHeaders:
        if settings.with_gcp_token:
            token = id_token.fetch_id_token(Request(), self.base_url)
            headers = {
                "Authorization": f"Bearer {token}",
            }
        else:
            headers = {}
        return headers

    async def try_connect(self, headers: LooseHeaders) -> bool:
        for _ in range(10):
            async with ClientSession(
                base_url=self.base_url, headers=headers
            ) as session:
                async with session.get("/") as response:
                    if response.status == 200:
                        return True
                    time.sleep(2)
        return False

    async def read(
        self,
        image: Image.Image,
        params: SearchParams,
    ) -> OCRResultList:
        headers = self.get_headers()
        is_connected = await self.try_connect(headers=headers)
        if not is_connected:
            raise Exception("OCR server に接続できないよ～")

        # 1. メモリ上にバイナリデータを保存するためのバッファを作成
        buffer = io.BytesIO()

        # 2. PIL画像をバッファに保存（形式を指定。例: JPEG, PNG）
        image.save(buffer, format="PNG")

        # 3. バッファの先頭から中身（bytes）を取り出す
        image_bytes = buffer.getvalue()
        # FormDataオブジェクトを作成
        data = FormData()
        # "file" はサーバー側が期待するフィールド名
        data.add_field(
            "file",
            image_bytes,
            filename="image.png",
            content_type="image/png",
        )
        async with ClientSession(base_url=self.base_url, headers=headers) as session:
            async with session.post(
                "/ocr", data=data, params=params.model_dump(exclude_none=True)
            ) as response:
                if response.status == 200:
                    text = await response.text()
                else:
                    raise Exception(response.json)
        results = OCRResultList.model_validate_json(text)
        return results
