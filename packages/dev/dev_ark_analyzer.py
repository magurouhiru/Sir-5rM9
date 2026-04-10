import asyncio
import io
import logging

from core.ark import analyze_main
from core.ocr import builder
from PIL import Image

image_path = "sample2.png"


async def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    ocr = builder(logger)
    img = Image.open(image_path)

    # 1. メモリ上にバイナリを置くためのバッファを作成
    img_bytes_io = io.BytesIO()

    # 2. バッファに対して画像を保存（フォーマットの指定が必要）
    img.save(img_bytes_io, format="PNG")

    # 3. バッファの中身を bytes として取り出す
    img_bytes = img_bytes_io.getvalue()

    result = await analyze_main(img_bytes, ocr, logger)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
