import io
import time
from dataclasses import asdict

from aiohttp import ClientSession, FormData
from PIL import Image
from pydantic import BaseModel

from .ocr import ImageReader, Options


class OCRResult(BaseModel):
    result: list[str]


class OcrServerImageReader(ImageReader):
    def __init__(self):
        super().__init__()

    async def try_connect(self) -> bool:
        for _ in range(5):
            async with ClientSession() as session:
                async with session.get("http://localhost:8000/ready") as response:
                    if response.status == 200:
                        return True
                    time.sleep(2)
        return False

    async def read(
        self,
        image: Image.Image,
        options: Options,
    ) -> list[str]:
        self.try_connect()
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
        filtered_params = {k: v for k, v in asdict(options).items() if v is not None}
        async with ClientSession() as session:
            async with session.post(
                "http://localhost:8000/ocr", data=data, params=filtered_params
            ) as response:
                text = await response.text()
        result = OCRResult.model_validate_json(text)
        return result.result
