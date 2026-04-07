import easyocr
from core import OCRResultList, SearchParams
from fastapi import FastAPI, File, Query, UploadFile

app = FastAPI()


reader = easyocr.Reader(["ja"], gpu=False, verbose=False)


@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/ocr")
async def upload_image(file: UploadFile = File(...), params: SearchParams = Query()):
    data = await file.read()
    raw_results = reader.readtext(
        data, detail=1, **params.model_dump(exclude_none=True)
    )
    results = OCRResultList.model_validate(raw_results)

    return results
