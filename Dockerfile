FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]

#docker build -t fastapi-app . ---собираем наш образ
#docker run -p 8000:8000 fastapi-app ---запускаем наш образ