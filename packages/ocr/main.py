import easyocr
from fastapi import FastAPI, File, Query, UploadFile
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


app = FastAPI()


reader = easyocr.Reader(["ja"], gpu=False, verbose=False)


@app.get("/")
def root():
    return {"hello": "world"}


@app.get("/ready")
def ready():
    return {"ready": "ok"}


@app.post("/ocr")
async def upload_image(file: UploadFile = File(...), params: SearchParams = Query()):
    data = await file.read()
    filtered_params = {k: v for k, v in params.model_dump().items() if v is not None}
    result = reader.readtext(data, detail=0, **filtered_params)

    return {"result": result}
