FROM python:3.12-alpine AS builder

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /build

# Копируем только файл зависимостей, чтобы кэш Docker не сбрасывался при изменении кода
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Копируем сам скрипт
COPY app.py /app/

EXPOSE 8080

CMD ["python", "app.py"]

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health', timeout=3)" || exit 1
