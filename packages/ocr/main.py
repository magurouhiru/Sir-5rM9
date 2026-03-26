from fastapi import FastAPI, File, UploadFile

app = FastAPI()


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
    # 画像バイナリ取得
    data = await file.read()

    return {"filename": filename, "size": len(data)}
