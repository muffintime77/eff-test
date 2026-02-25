FROM python:3.12-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY app.py .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health', timeout=3)" || exit 1
