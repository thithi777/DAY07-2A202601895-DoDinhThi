"""
bench.py — Benchmark RAG Retrieval Strategies (Data Foundations Day 7)

Chạy đánh giá và so sánh các chiến lược Chunking (FixedSize, Sentence, Recursive)
trên tập tài liệu corpus và bộ 5 câu hỏi Benchmark Queries.

Cú pháp sử dụng:
    .venv\Scripts\python.exe bench.py
    .venv\Scripts\python.exe bench.py --provider local --data-dir data/demo --top-k 3
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

# Đảm bảo Windows console hỗ trợ UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ingest import build_knowledge_base
from src.chunking import FixedSizeChunker, RecursiveChunker, SentenceChunker
from src.embeddings import LocalEmbedder, _mock_embed


# Bộ 5 câu hỏi đánh giá chuẩn (Benchmark Queries)
BENCHMARK_QUERIES = [
    {
        "id": "Q1",
        "type": "Số liệu",
        "query": "Thời hạn bộ phận tiếp nhận khiếu nại của Shopee giải quyết các tranh chấp không phải là khiếu nại Trả Hàng/Hoàn Tiền là bao nhiêu ngày làm việc?",
        "expected_doc_id": "shopee-payment-limits",
        "gold_keyword": "07 ngày làm việc",
    },
    {
        "id": "Q2",
        "type": "Điều kiện",
        "query": "Người Bán cần đáp ứng điều kiện pháp lý gì về giấy phép khi đăng bán sản phẩm trên Shopee nếu Người Bán là pháp nhân có vốn đầu tư nước ngoài?",
        "expected_doc_id": "shopee-product-listing-rules-previous",
        "gold_keyword": "Giấy phép kinh doanh",
    },
    {
        "id": "Q3",
        "type": "Quy trình",
        "query": "Quy trình khởi tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền đối với Người Mua được thực hiện như thế nào ở Bước 1?",
        "expected_doc_id": "shopee-payment-limits",
        "gold_keyword": "mục “Đơn Mua”",
    },
    {
        "id": "Q4",
        "type": "Liệt kê",
        "query": "Theo Chính sách Trả hàng và Hoàn tiền, Người Mua có thể yêu cầu trả hàng/hoàn tiền trong những trường hợp nào?",
        "expected_doc_id": "shopee-return-refund-policy",
        "gold_keyword": "không nhận được Sản Phẩm",
    },
    {
        "id": "Q5",
        "type": "Ngoại lệ",
        "query": "Trong quy định xử lý khiếu nại/tranh chấp của Shopee, trường hợp ngoại lệ nào sẽ không sử dụng quyết định cuối cùng của Shopee?",
        "expected_doc_id": "shopee-payment-limits",
        "gold_keyword": "cơ quan nhà nước có thẩm quyền",
    },
]


def select_embedder(provider: str) -> Callable[[str], list[float]]:
    if provider == "local":
        try:
            print("🚀 Sử dụng LocalEmbedder (SentenceTransformers)...")
            return LocalEmbedder()
        except Exception as e:
            print(f"⚠️ Không thể tải LocalEmbedder ({e}). Tạm thời dùng MockEmbedder.")
            return _mock_embed
    print("⚡ Sử dụng MockEmbedder...")
    return _mock_embed


def evaluate_strategy(
    strategy_name: str,
    chunker,
    data_dir: str,
    embedder_fn: Callable[[str], list[float]],
    top_k: int = 3,
):
    print(f"\n==================================================")
    print(f"📊 CHẠY BENCHMARK: {strategy_name}")
    print(f"==================================================")

    store = build_knowledge_base(
        data_dir=data_dir,
        embedding_fn=embedder_fn,
        chunker=chunker,
        collection_name=f"bench_{strategy_name}",
    )

    total_chunks = store.get_collection_size()
    print(f"Tổng số chunks đã tạo: {total_chunks}")

    hits = 0
    total_queries = len(BENCHMARK_QUERIES)

    for item in BENCHMARK_QUERIES:
        q_id = item["id"]
        q_type = item["type"]
        q_text = item["query"]
        expected_doc = item["expected_doc_id"]
        keyword = item["gold_keyword"]

        results = store.search(q_text, top_k=top_k)

        is_hit = False
        for r in results:
            content = r["content"]
            doc_id = r["metadata"].get("doc_id", "")
            if expected_doc in doc_id or keyword.lower() in content.lower():
                is_hit = True
                break

        if is_hit:
            hits += 1
            status = "✅ HIT"
        else:
            status = "❌ MISS"

        print(f"\n[{q_id} - {q_type}] {status}")
        print(f"  Query: {q_text[:70]}...")
        if results:
            top1 = results[0]
            print(f"  Top 1 Score: {top1['score']:.4f} | Doc: {top1['metadata'].get('doc_id')}")
            print(f"  Snippet: \"{top1['content'][:100].replace(chr(10), ' ')}...\"")

    hit_rate = (hits / total_queries) * 100
    print(f"\nKết quả {strategy_name}: Hit@{top_k} = {hits}/{total_queries} ({hit_rate:.1f}%)")
    return {"strategy": strategy_name, "chunks": total_chunks, "hits": hits, "hit_rate": hit_rate}


def main():
    parser = argparse.ArgumentParser(description="Benchmark RAG Retrieval Strategies")
    parser.add_argument("--data-dir", default="data/demo", help="Thư mục dữ liệu (mặc định: data/demo)")
    parser.add_argument("--provider", default="mock", choices=["mock", "local"], help="Backend nhúng (mock | local)")
    parser.add_argument("--top-k", type=int, default=3, help="Số lượng Top-k kết quả cần lấy (mặc định: 3)")

    args = parser.parse_args()

    data_path = Path(args.data_dir)
    if not data_path.exists():
        print(f"❌ Thư mục {args.data_dir} không tồn tại!")
        sys.exit(1)

    embedder_fn = select_embedder(args.provider)

    strategies = [
        ("FixedSizeChunker(200, 20)", FixedSizeChunker(chunk_size=200, overlap=20)),
        ("SentenceChunker(max=3)", SentenceChunker(max_sentences_per_chunk=3)),
        ("RecursiveChunker(200)", RecursiveChunker(chunk_size=200)),
    ]

    summary_results = []
    for name, chunker in strategies:
        res = evaluate_strategy(name, chunker, args.data_dir, embedder_fn, top_k=args.top_k)
        summary_results.append(res)

    print("\n" + "=" * 60)
    print("🏆 BẢNG TỔNG HỢP KẾT QUẢ BENCHMARK RETRIEVAL")
    print("=" * 60)
    print(f"{'Chiến lược Chunking':<25} | {'Số Chunks':<10} | {'Hit@' + str(args.top_k):<8} | {'Tỷ lệ Hit (%)':<12}")
    print("-" * 60)
    for s in summary_results:
        print(f"{s['strategy']:<25} | {s['chunks']:<10} | {s['hits']}/5     | {s['hit_rate']:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
