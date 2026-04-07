# --- Build Stage ---
FROM astral/uv:0.10.12-python3.13-trixie AS builder

# uvのインストール先などを設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN mkdir -p packages/ocr

# 依存関係のみを先にコピー（キャッシュ効率化）
COPY pyproject.toml uv.lock ./
COPY ./packages/ocr_server/pyproject.toml ./packages/ocr_server/

# 仮想環境 (.venv) を作成し、ライブラリをインストール
RUN uv sync --no-dev --package ocr_server

# --- Run Stage ---
FROM python:3.13-slim AS runner

WORKDIR /app

# ビルドステージで作った仮想環境だけをコピー
COPY --from=builder /app/.venv /app/.venv
COPY ./packages/ocr_server ./packages/ocr_server

# 仮想環境のパスを優先的に使う設定
ENV PATH="/app/.venv/bin:$PATH"

# easyocrのモジュールを含める
RUN python -c "import easyocr; easyocr.Reader([\"ja\"], gpu=False, verbose=False)"

# 実行コマンド（例：main.py を実行）
ENTRYPOINT ["fastapi", "run", "/app/packages/ocr_server/src/ocr_server/main.py"]