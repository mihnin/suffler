"""Запуск Суфлёра на компьютере.

Просто запустите этот файл (двойной щелчок по «Запустить суфлёр.bat» на Windows
или «Запустить суфлёр.command» на Mac). Откроется браузер с приложением.
Адрес для iPad в той же Wi-Fi сети будет показан в этом окне.
Чтобы остановить — закройте окно.
"""
import http.server
import os
import socket
import socketserver
import webbrowser

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # пакеты не отправляются, только выбор сетевого интерфейса
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".webmanifest": "application/manifest+json",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), Handler) as httpd:
    ip = lan_ip()
    print("=" * 60)
    print(" Суфлёр запущен.")
    print(f" На этом компьютере:   http://localhost:{PORT}")
    if ip:
        print(f" С iPad (та же Wi-Fi): http://{ip}:{PORT}")
        print("   (по такому адресу работает чтение и прокрутка, но без")
        print("    офлайн-режима и микрофона — см. README, раздел про HTTPS)")
    print(" Чтобы остановить — закройте это окно.")
    print("=" * 60)
    webbrowser.open(f"http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
