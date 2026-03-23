# --- Build Stage ---
FROM astral/uv:0.10.12-python3.13-trixie AS builder

# Poetryのインストール先などを設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# 依存関係のみを先にコピー（キャッシュ効率化）
COPY pyproject.toml uv.lock ./

# 仮想環境 (.venv) を作成し、ライブラリをインストール
RUN uv sync --no-dev

# --- Run Stage ---
FROM python:3.13-slim AS runner

WORKDIR /app

# ビルドステージで作った仮想環境だけをコピー
COPY --from=builder /app/.venv /app/.venv
COPY . .

# 仮想環境のパスを優先的に使う設定
ENV PATH="/app/.venv/bin:$PATH" \
    APP_ENV=production

# 実行コマンド（例：main.py を実行）
ENTRYPOINT ["python", "main.py"]