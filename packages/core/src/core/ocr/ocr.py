from abc import ABC, abstractmethod

from api import OCRResultList, SearchParams
from PIL import Image


class OCR(ABC):
    @abstractmethod
    async def read(
        self,
        image: Image.Image,
        params: SearchParams,
    ) -> OCRResultList:
        pass
