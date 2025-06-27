# mcp-tool-server/Dockerfile

# slimイメージを使用し、ビルドステージと実行ステージを分けることで、最終的なイメージサイズを小さくできます。
# --- Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /app

# uvをインストール
RUN pip install uv

# pyproject.tomlをコピーして、依存関係のみを先にインストールします。
# これにより、コードの変更時に毎回依存関係を再インストールする必要がなくなり、ビルドが高速化されます。
COPY pyproject.toml .
RUN uv pip install --system --no-cache .

# --- Run Stage ---
FROM python:3.11-slim

WORKDIR /app

# ビルドステージからインストール済みのライブラリとアプリケーションコードをコピーします。
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app/

# セキュリティ向上のため、非rootユーザーで実行します。
RUN useradd --create-home appuser
USER appuser

ENV PYTHONUNBUFFERED=1

# Cloud RunはEXPOSE命令を無視しますが、ドキュメントとして正しいポートを記載します。
EXPOSE 8080

CMD ["python", "server.py"]
