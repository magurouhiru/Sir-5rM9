# --- Build Stage ---
FROM astral/uv:0.10.12-python3.13-trixie AS builder

# uvのインストール先などを設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN mkdir -p packages/bot

# 依存関係のみを先にコピー（キャッシュ効率化）
COPY pyproject.toml uv.lock ./
COPY ./packages/api ./packages/api
COPY ./packages/core ./packages/core
COPY ./packages/bot/pyproject.toml ./packages/bot/

# 仮想環境 (.venv) を作成し、ライブラリをインストール
RUN uv sync --no-dev --package bot --no-cache --no-editable

# --- Run Stage ---
FROM python:3.13-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get upgrade -y

# ビルドステージで作った仮想環境だけをコピー
COPY --from=builder /app/.venv /app/.venv
COPY ./packages/bot ./packages/bot


# 仮想環境のパスを優先的に使う設定
ENV PATH="/app/.venv/bin:$PATH"

# 実行コマンド（例：main.py を実行）
ENTRYPOINT ["python", "/app/packages/bot/src/bot/main.py"]
