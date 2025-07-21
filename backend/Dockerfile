FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Wir kopieren den Inhalt von ./app direkt nach /app
COPY ./app .

# Wir starten wieder direkt main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]