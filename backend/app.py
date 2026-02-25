import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn

port = 8080
root_text = os.getenv("ROOT_ENDP_TEXT", "root page default text")

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

app = FastAPI()

@app.middleware("http")
async def log_real_ip(request: Request, call_next):
    real_ip = request.headers.get("X-Real-IP", request.client.host)
    response = await call_next(request)
    logging.info(
        "client_ip=%s method=%s path=%s status=%s",
        real_ip,
        request.method,
        request.url.path,
        response.status_code,
    )
    return response

@app.get("/", response_class=PlainTextResponse)
async def root():
    return root_text

@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "OK"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
