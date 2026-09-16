FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y docker.io

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src

CMD ["python", "main.py"]