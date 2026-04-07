from pydantic import BaseModel


class SearchParams(BaseModel):
    allowlist: str = None
    decoder: str = None
    beamWidth: int = None
    mag_ratio: float = None
    contrast_ths: float = None
    adjust_contrast: float = None
    text_threshold: float = None
    low_text: float = None
    link_threshold: float = None
