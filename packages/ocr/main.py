import easyocr
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


reader = easyocr.Reader(["ja"], gpu=False)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/ocr")
async def upload_image(file: UploadFile = File(...)):
    # メタデータ取得
    filename = file.filename
    content_type = file.content_type
    # 画像バイナリ取得
    data = await file.read()
    print(filename)
    print(content_type)
    print(len(data))
    result = reader.readtext(data, detail=0)

    # return {"filename": filename, "content_type": content_type}
    return {"result": result}
