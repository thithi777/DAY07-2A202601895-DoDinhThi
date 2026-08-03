import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8501
WEBUI_DIR = Path(__file__).parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEBUI_DIR), **kwargs)


def main():
    print(f"🚀 Đang khởi chạy Lab 7 Demo Web UI tại: http://localhost:{PORT}")
    url = f"http://localhost:{PORT}"
    try:
        webbrowser.open(url)
    except Exception:
        pass

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("💡 Nhấn Ctrl+C để dừng Web UI server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Đã đóng Web UI server.")


if __name__ == "__main__":
    main()
