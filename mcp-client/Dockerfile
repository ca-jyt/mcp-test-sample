# --- Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /app

# uvをインストール
RUN pip install uv

# requirements.txtをコピーして依存関係をインストール
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# --- Run Stage ---
FROM python:3.11-slim

WORKDIR /app

# ビルドステージからインストール済みのライブラリと実行ファイルをコピー
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY client.py /app/

# セキュリティ向上のため、非rootユーザーで実行します。
RUN useradd --create-home appuser
USER appuser

ENV PYTHONUNBUFFERED=1

# Cloud Runから渡されるPORT環境変数を尊重するようにCMDを修正
CMD ["sh", "-c", "uvicorn client:app --host 0.0.0.0 --port $PORT"]
