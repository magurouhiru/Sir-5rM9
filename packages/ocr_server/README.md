# ocr
[EasyOCR](https://github.com/JaidedAI/EasyOCR) を[FastAPI](https://github.com/fastapi/fastapi) でラップしたやつ。  
[EasyOCR](https://github.com/JaidedAI/EasyOCR) が軽くなかった(GCP のe2.micro では厳しい)ので、Cloud Run に切り出すために作成。

## 機能
- [x] ヘルスチェック(GET /)
- [x] OCR(POST /ocr)

## 開発

### フレームワーク・ライブラリ

#### [EasyOCR](https://github.com/JaidedAI/EasyOCR)
名前の通り、簡単にOCRが使えるライブラリ。前処理なしの方が精度が良いことも。裏でPyTorchを使っている。

#### [FastAPI](https://github.com/fastapi/fastapi)
モダンなWeb フレームワーク。

#### [ruff](https://github.com/astral-sh/ruff)
Rustで書かれた、非常に高速なPythonリンターおよびコードフォーマッター。
