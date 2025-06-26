FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY client.py /app/
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["uvicorn", "client:app", "--host", "0.0.0.0", "--port", "8080"]
