from pydantic import BaseModel, Field, RootModel, model_validator


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


class OCRResult(BaseModel):
    # 名前をつけて管理しやすくする
    bbox: list[list[int]] = Field(
        ..., description="4点の座標 [[x,y], [x,y], [x,y], [x,y]]"
    )
    text: str = Field(..., description="認識されたテキスト")
    confidence: float = Field(..., description="確信度 (0.0~1.0)")

    @model_validator(mode="before")
    @classmethod
    def from_list(cls, data):
        # EasyOCRの [座標, テキスト, 確信度] というリスト構造を分解
        if isinstance(data, (list, tuple)) and len(data) == 3:
            return {"bbox": data[0], "text": data[1], "confidence": data[2]}
        return data


class OCRResultList(RootModel):
    root: list[OCRResult]
