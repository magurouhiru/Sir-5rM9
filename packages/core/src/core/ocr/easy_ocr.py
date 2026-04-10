from logging import Logger

import easyocr
import numpy as np
from api import OCRResultList, SearchParams
from PIL import Image

from .ocr import OCR


class EasyOCR(OCR):
    def __init__(self, logger: Logger):
        super().__init__()
        self.reader = easyocr.Reader(["ja"], gpu=False, verbose=False)
        self.logger = logger
        self.logger.info("init: EasyOCR")

    async def read(
        self,
        image: Image.Image,
        params: SearchParams,
    ) -> OCRResultList:
        raw_results = self.reader.readtext(
            image=np.array(image), detail=1, **params.model_dump(exclude_none=True)
        )
        results = OCRResultList.model_validate(raw_results)
        return results
