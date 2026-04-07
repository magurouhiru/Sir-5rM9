from abc import ABC, abstractmethod

from core import SearchParams
from PIL import Image


class ImageReader(ABC):
    @abstractmethod
    async def read(
        self,
        image: Image.Image,
        params: SearchParams,
    ) -> list[str]:
        pass
