FROM python:3.11-slim
LABEL authors="pankyxa"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python", "main.py"]