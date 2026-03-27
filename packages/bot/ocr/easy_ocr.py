from dataclasses import asdict

import easyocr
import numpy as np
from PIL import Image

from .ocr import ImageReader, Options


class EasyOcrImageReader(ImageReader):
    def __init__(self):
        super().__init__()
        self.reader = easyocr.Reader(["ja"], gpu=False)

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
