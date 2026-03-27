import io

from aiohttp import ClientSession, FormData
from PIL import Image

from .ocr import ImageReader, Options


class OcrServerImageReader(ImageReader):
    def __init__(self):
        super().__init__()

    async def read(
        self,
        image: Image.Image,
        options: Options,
        filename: str = None,
        content_type: str = None,
    ) -> list[str]:
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
        async with ClientSession() as session:
            async with session.post("http://localhost:8000/ocr", data=data) as response:
                print("Status:", response.status)
                print("Content-type:", response.headers["content-type"])

                html = await response.text()
                print("Body:", html)
        return html["result"]
