from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обрабатывает GET-запросы."""
        if self.path == "/":
            self.path = "/contacts.html"

        try:
            # Читаем HTML-файл
            with open("templates" + self.path, "r", encoding="utf-8") as file:
                content = file.read()

            # Отправляем ответ
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        except FileNotFoundError:
            # Если файл не найден — 404
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("<h1>404 - Страница не найдена</h1>".encode("utf-8"))

    def do_POST(self):
        """Обрабатывает POST-запросы (дополнительное задание)."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        print("Получены данные:", post_data)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<h1>Данные получены!</h1>".encode("utf-8"))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()