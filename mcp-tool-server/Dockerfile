FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install uv vertexai fastmcp
COPY . /app/
ENV PYTHONUNBUFFERED=1
EXPOSE $PORT
CMD ["python", "server.py"]
