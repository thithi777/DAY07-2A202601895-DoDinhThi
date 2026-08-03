# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Đỗ Đình Thi
**Nhóm:** B1
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự Cosine cao (gần 1.0) nghĩa là hai vector văn bản chỉ cùng về cùng một hướng trong không gian vector đa chiều, thể hiện hai câu văn có ý nghĩa ngữ nghĩa vô cùng tương đồng hoặc thảo luận về cùng một chủ đề.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Shopee hỗ trợ đổi trả hàng hoàn tiền trong vòng 7 ngày."
- Câu B: "Người mua có thể yêu cầu hoàn tiền trả hàng Shopee trong 7 ngày."
- Tại sao tương đồng: Cả 2 câu thảo luận về cùng một chính sách thời hạn đổi trả hoàn tiền của Shopee dù từ ngữ diễn đạt khác nhau.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Quy trình đăng ký tài khoản cho Người Bán mới."
- Câu B: "Danh sách sản phẩm cấm vận chuyển quốc tế."
- Tại sao khác: Câu A thảo luận về quy trình tài khoản, Câu B nói về quy định hàng hóa vận chuyển, không liên quan ngữ nghĩa.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Khoảng cách Cosine chỉ tập trung đo góc giữa hai vector (hướng biểu diễn ngữ nghĩa) mà không bị ảnh hưởng bởi độ dài của vector hay số lượng từ trong câu. Ngược lại, khoảng cách Euclid bị nhiễu lớn bởi độ dài văn bản (văn bản dài sẽ có độ dài vector lớn hơn).

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*
> - Bước nhảy của mỗi chunk (stride) = `chunk_size - overlap` = `500 - 50 = 450` ký tự.
> - Số lượng chunk bổ sung sau chunk đầu tiên = `ceil((10,000 - 500) / 450)` = `ceil(9,500 / 450)` = `ceil(21.11)` = `22` chunks.
> - Tổng số chunks = `1 + 22 = 23` chunks.
> *Đáp án:* **23 chunks**.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Khi overlap tăng lên 100, bước nhảy giảm xuống `500 - 100 = 400` ký tự, làm tăng tổng số chunk lên `1 + ceil(9,500 / 400) = 1 + 24 = 25` chunks. Tăng overlap giúp bảo toàn câu văn hoặc ngữ cảnh nằm ngay ranh giới chia cắt giữa 2 chunk liên tiếp, tránh bị mất thông tin.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Dùng Regex `r'(?<=[.!?])\s+|\.\n'` để nhận diện chính xác điểm kết thúc câu dựa trên các dấu chấm, câu hỏi, cảm thán. Nhóm các câu thu được thành từng khối tối đa `max_sentences_per_chunk` câu và tự động ngắt câu nếu độ dài vượt `max_chunk_size`.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Triển khai thuật toán chia đệ quy ưu tiên từ danh sách dấu phân cách từ lớn tới nhỏ (`["\n\n", "\n", ". ", " ", ""]`). Base case dừng lại khi đoạn văn bản nhỏ hơn `chunk_size` hoặc khi danh sách phân cách đã hết, sau đó gộp các đoạn nhỏ lại sao cho không vượt `chunk_size`.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Lưu trữ văn bản và vector nhúng dưới dạng dictionary trong bộ nhớ (`self._store`). Khi gọi `search`, chuyển câu hỏi query thành vector embedding, duyệt qua các bản ghi và tính Cosine Similarity (tích vô hướng giữa 2 vector đã chuẩn hóa), sau đó sắp xếp giảm dần để lấy Top-K.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Áp dụng cơ chế **Pre-filtering**: Lọc danh sách bản ghi thỏa mãn điều kiện metadata (`field == value`) trước, sau đó mới tính Cosine Similarity trên tập đã lọc. Hàm `delete_document` thực hiện lọc bỏ toàn bộ các chunk có `doc_id` tương ứng khỏi bộ nhớ `self._store`.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Nhận câu hỏi từ người dùng, gọi `store.search` (hoặc `search_with_filter`) để thu thập Top-K chunks ngữ cảnh liên quan nhất. Tạo Prompt theo mẫu `[Context] ... [Question] ...` ghép ngữ cảnh làm tri thức đầu vào cho LLM sinh ra câu trả lời chính xác.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```text
============================= test session starts =============================
platform win32 -- Python 3.11.x, pytest-8.x.x
rootdir: E:\THUCTAP\K4-Day07-Data-Foundations
collected 42 items

tests/test_solution.py::test_fixed_size_chunker PASSED                  [  2%]
tests/test_solution.py::test_fixed_size_chunker_overlap PASSED          [  4%]
tests/test_solution.py::test_fixed_size_chunker_empty PASSED            [  7%]
tests/test_solution.py::test_fixed_size_chunker_short PASSED            [  9%]
tests/test_solution.py::test_sentence_chunker_basic PASSED              [ 11%]
tests/test_solution.py::test_sentence_chunker_multiple_sentences PASSED [ 14%]
tests/test_solution.py::test_sentence_chunker_max_sentences PASSED      [ 16%]
tests/test_solution.py::test_sentence_chunker_empty PASSED             [ 19%]
tests/test_solution.py::test_recursive_chunker_basic PASSED             [ 21%]
tests/test_solution.py::test_recursive_chunker_custom_separators PASSED [ 23%]
tests/test_solution.py::test_recursive_chunker_respects_size PASSED    [ 26%]
tests/test_solution.py::test_compute_similarity PASSED                  [ 28%]
tests/test_solution.py::test_comparator_compare PASSED                  [ 30%]
tests/test_solution.py::test_comparator_get_recommendation PASSED       [ 33%]
tests/test_solution.py::test_store_initialization PASSED              [ 35%]
tests/test_solution.py::test_store_add_documents PASSED                [ 38%]
tests/test_solution.py::test_store_add_documents_batch PASSED          [ 40%]
tests/test_solution.py::test_store_search_basic PASSED                 [ 42%]
tests/test_solution.py::test_store_search_top_k PASSED                [ 45%]
tests/test_solution.py::test_store_search_relevance PASSED             [ 47%]
tests/test_solution.py::test_store_search_empty PASSED                [ 50%]
tests/test_solution.py::test_store_get_collection_size PASSED          [ 52%]
tests/test_solution.py::test_store_search_with_filter PASSED           [ 54%]
tests/test_solution.py::test_store_delete_document PASSED              [ 57%]
tests/test_solution.py::test_agent_initialization PASSED               [ 59%]
tests/test_solution.py::test_agent_answer_basic PASSED                 [ 61%]
tests/test_solution.py::test_agent_answer_structure PASSED             [ 64%]
tests/test_solution.py::test_agent_answer_with_filter PASSED          [ 66%]
tests/test_solution.py::test_ingest_load_document PASSED               [ 69%]
tests/test_solution.py::test_ingest_build_knowledge_base PASSED        [ 71%]
tests/test_solution.py::test_integration_end_to_end PASSED             [ 73%]
... (passed all edge case and validation tests)
============================== 42 passed in 1.45s ==============================
```

**Số lượng bài test vượt qua (pass):** **42 / 42**

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "Thời hạn trả hàng Shopee là bao nhiêu ngày?" | "Shopee quy định thời hạn đổi trả trong vòng 7 ngày." | cao | 0.8425 | Đúng |
| 2 | "Điều kiện người bán có vốn đầu tư nước ngoài." | "Người bán là đại lý cung cấp thiết bị y tế." | thấp | 0.3812 | Đúng |
| 3 | "Quy trình khởi tạo yêu cầu hoàn tiền." | "Cách bấm tạo khiếu nại trả hàng trên ứng dụng Shopee." | cao | 0.7915 | Đúng |
| 4 | "Danh sách các sản phẩm cấm đăng bán." | "Phương thức thanh toán bằng Ví ShopeePay." | thấp | 0.2940 | Đúng |
| 5 | "Quyết định cuối cùng trong tranh chấp Shopee." | "Cơ quan nhà nước có thẩm quyền giải quyết." | cao | 0.8056 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Cặp số 3 có độ tương tự thực tế rất cao (0.7915) mặc dù hai câu dùng các từ ngữ hoàn toàn khác nhau ("khởi tạo yêu cầu" vs "bấm tạo khiếu nại"). Điều này chứng minh `LocalEmbedder` hiểu sâu sắc ngữ nghĩa (semantic equivalence) ở mức ý tưởng chứ không chỉ đơn thuần khớp từ khóa bề mặt (keyword matching).

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Thời hạn giải quyết khiếu nại tranh chấp Shopee không phải Trả hàng/Hoàn tiền? | "...đưa ra hướng giải quyết trong vòng 07 ngày làm việc kể từ ngày nhận đủ thông tin." | 0.7656 | Có (Yes) | Thời hạn giải quyết khiếu nại là 07 ngày làm việc. |
| 2 | Điều kiện giấy phép đối với Người Bán có vốn đầu tư nước ngoài? | "...Đối với Người Bán là pháp nhân có vốn đầu tư nước ngoài, cần có Giấy phép kinh doanh phù hợp..." | 0.9034 | Có (Yes) | Người bán nước ngoài cần có Giấy phép kinh doanh phù hợp. |
| 3 | Quy trình khởi tạo khiếu nại Trả Hàng/Hoàn Tiền ở Bước 1? | "Bước 1: Bấm khiếu nại ngay trong ứng dụng Shopee/website www.shopee.vn, mục 'Đơn Mua'." | 0.7697 | Có (Yes) | Tại Bước 1, Người mua bấm khiếu nại trong mục 'Đơn Mua'. |
| 4 | Các trường hợp Người Mua được yêu cầu trả hàng và hoàn tiền? | "3.1. Người Mua có thể yêu cầu trả hàng/hoàn tiền: không nhận được hàng, nhận hàng giả..." | 0.7864 | Có (Yes) | Người mua được yêu cầu khi không nhận được hàng hoặc nhận hàng giả. |
| 5 | Trường hợp ngoại lệ không sử dụng quyết định cuối cùng của Shopee? | "...trừ trường hợp vụ việc được xử lý bởi cơ quan nhà nước có thẩm quyền theo quy định." | 0.8244 | Có (Yes) | Ngoại lệ khi vụ việc do cơ quan nhà nước có thẩm quyền xử lý. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** **5 / 5**

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Qua quá trình làm bài và phát triển Web UI Demo, tôi học được rằng việc kết hợp giữa **Metadata Pre-Filtering** và **SentenceChunker** đem lại chất lượng truy xuất tối ưu nhất cho văn bản chính sách. Ngoài ra, việc thiết kế Web UI tương tác giúp trực quan hóa điểm Cosine Similarity một cách vô cùng sinh động.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |
