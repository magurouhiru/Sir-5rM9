from abc import ABC, abstractmethod

from core import OCRResultList, SearchParams
from PIL import Image


class ImageReader(ABC):
    @abstractmethod
    async def read(
        self,
        image: Image.Image,
        params: SearchParams,
    ) -> OCRResultList:
        pass
