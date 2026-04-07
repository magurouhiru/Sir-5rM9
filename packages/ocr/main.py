import easyocr
from core import SearchParams
from fastapi import FastAPI, File, Query, UploadFile

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
    result = reader.readtext(data, detail=0, **params.model_dump(exclude_none=True))

    return {"result": result}
