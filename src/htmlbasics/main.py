# Импорт встроенной библиотеки для работы веб-сервера
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети
serverHomeDir = Path("../../html")
page = serverHomeDir / "contacts.html"

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """Обрабатывает GET-запросы"""
        file_path = serverHomeDir / self.path.lstrip("/")  # Путь к запрашиваемому файлу

        if file_path.exists() and file_path.is_file():  # Если файл есть
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(file_path)  # Определяем тип файла
            self.send_header("Content-Type", mime_type or "application/octet-stream")
            self.send_header("Content-Length", str(file_path.stat().st_size))
            self.end_headers()

            with open(file_path, "rb") as f:
                self.wfile.write(f.read())  # Отдаём файл
        else:
            self.send_response(200)  # Всегда отдаём contacts.html, если файл не найден
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(page.stat().st_size))
            self.end_headers()

            with open(page, "rb") as f:
                self.wfile.write(f.read())


if __name__ == "__main__":
    # Инициализация веб-сервера, который по заданным параметрам будет
    # принимать запросы в сети и отправлять их на обработку специальному
    # классу, описанному выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
