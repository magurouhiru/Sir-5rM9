import logging
from dataclasses import asdict

import easyocr
import numpy as np
from PIL import Image

from settings.settings import settings

from .ocr import ImageReader, Options

logger = logging.getLogger(__name__)


class EasyOcrImageReader(ImageReader):
    def __init__(self):
        super().__init__()
        self.reader = easyocr.Reader(["ja"], gpu=False)
        logger.info("init: EasyOcrImageReader")
        if settings.with_ocr_server:
            logger.error(
                f"settings.with_ocr_server{settings.with_ocr_server}だけど、OCRサーバーモードなのにEasyOcrImageReader が初期化されました。"
            )

    async def read(
        self,
        image: Image.Image,
        options: Options,
    ) -> list[str]:
        filtered_params = {k: v for k, v in asdict(options).items() if v is not None}
        result = self.reader.readtext(
            image=np.array(image), detail=0, **filtered_params
        )
        return result
