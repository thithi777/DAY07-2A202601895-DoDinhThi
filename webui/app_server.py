"""
app_server.py — Python Backend Server hỗ trợ WebUI Đặt Câu Hỏi (Live RAG Search)

Cung cấp API tìm kiếm vector và trả lời câu hỏi trực tiếp dựa trên tập tài liệu trong data/demo hoặc data/chinh-sach-shopee.
"""
from __future__ import annotations

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys
import webbrowser

# Đảm bảo Windows console hỗ trợ UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Đảm bảo import được các module từ thư mục gốc dự án
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingest import build_knowledge_base
from src.agent import KnowledgeBaseAgent
from src.chunking import FixedSizeChunker, RecursiveChunker, SentenceChunker
from src.embeddings import LocalEmbedder, _mock_embed

PORT = 8080
WEBUI_DIR = Path(__file__).parent
DATA_DIR = "data/demo"

# Biến lưu trữ cache các store
_STORES_CACHE = {}
_LOCAL_EMBEDDER = None


def get_embedder(use_local: bool = True):
    global _LOCAL_EMBEDDER
    if use_local:
        if _LOCAL_EMBEDDER is None:
            try:
                print("[INFO] Đang khởi tạo LocalEmbedder (SentenceTransformers)...")
                _LOCAL_EMBEDDER = LocalEmbedder()
            except Exception as e:
                print(f"[WARN] Không thể khởi tạo LocalEmbedder ({e}). Chuyển sang MockEmbedder.")
                return _mock_embed
        return _LOCAL_EMBEDDER
    return _mock_embed


def get_chunker(strategy_name: str, chunk_size: int = 200):
    if strategy_name == "sentence":
        return SentenceChunker(max_sentences_per_chunk=3)
    elif strategy_name == "recursive":
        return RecursiveChunker(chunk_size=chunk_size)
    else:
        return FixedSizeChunker(chunk_size=chunk_size, overlap=20)


def get_store(strategy_name: str = "fixed_size", use_local: bool = True):
    cache_key = f"{strategy_name}_{'local' if use_local else 'mock'}"
    if cache_key in _STORES_CACHE:
        return _STORES_CACHE[cache_key]

    embedder_fn = get_embedder(use_local)
    chunker = get_chunker(strategy_name)

    print(f"[INFO] Nạp store cho strategy={strategy_name}, local={use_local}...")
    store = build_knowledge_base(
        data_dir=DATA_DIR,
        embedding_fn=embedder_fn,
        chunker=chunker,
        collection_name=f"webui_{cache_key}",
    )
    _STORES_CACHE[cache_key] = store
    return store


class RAGRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEBUI_DIR), **kwargs)

    def do_POST(self):
        if self.path == "/api/search":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                payload = json.loads(post_data.decode("utf-8"))
                question = payload.get("question", "").strip()
                strategy = payload.get("strategy", "fixed_size")
                top_k = int(payload.get("top_k", 3))
                use_local = bool(payload.get("use_local", True))

                if not question:
                    self._send_json({"error": "Vui lòng nhập câu hỏi!"}, status=400)
                    return

                store = get_store(strategy_name=strategy, use_local=use_local)
                raw_results = store.search(question, top_k=top_k)

                results = []
                for res in raw_results:
                    results.append({
                        "score": round(float(res["score"]), 4),
                        "doc_id": res["metadata"].get("doc_id", "N/A"),
                        "chunk_index": res["metadata"].get("chunk_index", 0),
                        "content": res["content"],
                        "source": res["metadata"].get("source", "N/A"),
                        "source_url": res["metadata"].get("source_url", ""),
                    })

                response_data = {
                    "question": question,
                    "strategy": strategy,
                    "top_k": top_k,
                    "total_chunks": store.get_collection_size(),
                    "answer": results[0]['content'] if results else 'Không tìm thấy ngữ cảnh.',
                    "results": results,
                }
                self._send_json(response_data)
            except Exception as e:
                self._send_json({"error": f"Lỗi hệ thống: {str(e)}"}, status=500)
        else:
            self.send_error(404, "Endpoint Not Found")

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def main():
    print(f"[INFO] Đang khởi chạy Live RAG WebUI Server tại: http://localhost:{PORT}")
    url = f"http://localhost:{PORT}"
    try:
        webbrowser.open(url)
    except Exception:
        pass

    with HTTPServer(("", PORT), RAGRequestHandler) as httpd:
        print("[INFO] Nhấn Ctrl+C để dừng server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Đã đóng server.")


if __name__ == "__main__":
    main()
