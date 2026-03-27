from abc import ABC, abstractmethod
from dataclasses import dataclass

from PIL import Image


@dataclass
class Options:
    allowlist: str = None
    decoder: str = None
    beamWidth: int = None
    mag_ratio: float = None
    contrast_ths: float = None
    adjust_contrast: float = None
    text_threshold: float = None
    low_text: float = None
    link_threshold: float = None


class ImageReader(ABC):
    @abstractmethod
    async def read(
        self,
        image: Image.Image,
        options: Options,
        filename: str = None,
        content_type: str = None,
    ) -> list[str]:
        pass
