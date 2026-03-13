# --- Build Stage ---
FROM python:3.13-slim AS builder

# Poetryのインストール先などを設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/root/.local" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# PATHを通す
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# 依存関係のみを先にコピー（キャッシュ効率化）
COPY pyproject.toml poetry.lock ./

# Poetryのインストール
# 仮想環境 (.venv) を作成し、ライブラリをインストール
RUN apt update && \
    apt upgrade -y && \
    apt install -y pipx && \
    pip3 install --upgrade pip && \
    pipx install poetry==2.3.2 && \
    poetry install --no-root

# --- Run Stage ---
FROM python:3.13-slim AS runner

WORKDIR /app

# ビルドステージで作った仮想環境だけをコピー
COPY --from=builder /app/.venv /app/.venv
COPY . .

# 仮想環境のパスを優先的に使う設定
ENV PATH="/app/.venv/bin:$PATH"

# 実行コマンド（例：main.py を実行）
ENTRYPOINT ["python", "main.py"]