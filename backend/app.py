import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import signal
import threading

port = 8080
root_endpoint_text = os.getenv("ROOT_ENDP_TEXT", 'root page default text')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

class Handler(BaseHTTPRequestHandler):
    def get_real_ip(self):
            # 1. Приоритет — X-Real-IP (ставит nginx)
            real_ip = self.headers.get("X-Real-IP")
            if real_ip:
                return real_ip
    
            # 2. Затем первый IP из X-Forwarded-For
            forwarded_for = self.headers.get("X-Forwarded-For")
            if forwarded_for:
                return forwarded_for.split(",")[0].strip()
    
            # 3. Фолбэк — IP сокета
            return self.client_address[0]
    
    def log_request(self, status_code):
        logging.info(
            "client_ip=%s method=%s path=%s status=%s",
            self.get_real_ip(),
            self.command,
            self.path,
            status_code,
        )
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(root_endpoint_text.encode('utf-8'))

        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = HTTPServer(("0.0.0.0", port), Handler)
    
    def signal_handler(signum, frame):
        logging.info(f"Received signal {signum}, shutting down gracefully...")
        # Запускаем shutdown в отдельном потоке, чтобы не блокировать обработчик
        threading.Thread(target=server.shutdown, daemon=True).start()
    
    # Регистрируем обработчик для SIGTERM (сигнал остановки контейнера)
    signal.signal(signal.SIGTERM, signal_handler)
    # Для SIGINT будет стандартное поведение – будет выброшено KeyboardInterrupt
    
    logging.info("Starting server on port %s", port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Received SIGINT, shutting down...")
        # При Ctrl+C serve_forever уже прерван, просто идём к finally
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        server.server_close()
        logging.info("Server stopped.")

if __name__ == "__main__":
    run_server()
