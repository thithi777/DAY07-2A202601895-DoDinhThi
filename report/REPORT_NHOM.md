# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** B1
**Thành viên:** 
- Đỗ Đình Thi (MSSV: 2A202601895)
- Nguyễn Lê Quân (MSSV: 2A202601476)
- Đinh Tuấn Minh (MSSV: 2A202601892)
- Trịnh Đắc Vụ (MSSV: 2A202601074)
- Nguyễn Thị Hải Yến (MSSV: 2A202601388)
**Ngày:** 03/08/2026

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

**Chủ đề (cố định theo lớp K4):** Chính sách thương mại điện tử / hỗ trợ khách hàng (thanh toán, đổi trả, giao hàng, quyền riêng tư, điều kiện người bán…).

**Phạm vi cụ thể nhóm tập trung:**
> Nhóm tập trung vào phạm vi các chính sách thương mại điện tử cốt lõi của Shopee Việt Nam bao gồm: quy định đổi trả hoàn tiền, vận chuyển, hạn mức thanh toán, quy định sản phẩm cấm/hạn chế và hệ thống phạt Sao Quả Tạ.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Chính sách Trả hàng và Hoàn tiền Shopee | https://help.shopee.vn/portal/4/article/77245 | 03/08/2026 / not-stated | 103,126 | `doc_id: shopee-returns-policy`, `customer_role: both`, `category: returns-policy` |
| 2 | Chính sách Vận chuyển Shopee | https://help.shopee.vn/portal/4/article/77246 | 03/08/2026 / not-stated | 29,246 | `doc_id: shopee-shipping-policy`, `customer_role: both`, `category: shipping-policy` |
| 3 | Hệ thống Sao Quả Tạ Shopee | https://help.shopee.vn/portal/4/article/77262 | 03/08/2026 / not-stated | 44,907 | `doc_id: shopee-seller-penalty-system`, `customer_role: seller`, `category: policy` |
| 4 | Quy chế hoạt động sàn Shopee | https://help.shopee.vn/portal/4/article/77247 | 03/08/2026 / not-stated | 17,442 | `doc_id: shopee-prohibited-items`, `customer_role: both`, `category: regulations` |
| 5 | Hạn mức thanh toán & Giải quyết tranh chấp | https://help.shopee.vn/portal/4/article/77265 | 03/08/2026 / not-stated | 6,686 | `doc_id: shopee-payment-limits`, `customer_role: buyer`, `category: payment` |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `customer_role` | `str` | `buyer` / `seller` / `both` | Phân loại chính xác đối tượng áp dụng để lọc đúng ngữ cảnh đối tượng khi truy xuất. |
| `category` | `str` | `returns-policy` / `shipping-policy` | Phân vùng chủ đề cụ thể giúp thu hẹp không gian tìm kiếm vector, loại bỏ các tài liệu nhiễu. |
| `document_version` | `str` | `not-stated` / `2025` | Đảm bảo hệ thống RAG truy xuất đúng phiên bản chính sách đang có hiệu lực. |
| `source_url` | `str` | `https://help.shopee.vn/...` | Cung cấp đường dẫn nguồn chính xác giúp RAG Agent dẫn nguồn trích dẫn uy tín. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `shopee-returns-policy.md` | FixedSizeChunker (`fixed_size`) | 521 | 199.9 ký tự | Dễ bị cắt ngang câu ở ranh giới chunk cố định 200 ký tự |
| `shopee-returns-policy.md` | SentenceChunker (`by_sentences`) | 195 | 397.1 ký tự | Giữ trọn vẹn từng câu quy định, ngữ cảnh hoàn chỉnh |
| `shopee-returns-policy.md` | RecursiveChunker (`recursive`) | 609 | 126.6 ký tự | Linh hoạt theo đoạn văn nhưng chunk hơi nhỏ khi bị ngắt dòng |

### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

**Thành viên 1 — Đỗ Đình Thi**
- **Loại chiến lược:** SentenceChunker
- **Mô tả & lý do chọn cho chủ đề này:** Chọn chiến lược cắt theo ranh giới câu (`SentenceChunker` với `max_sentences_per_chunk=3`) vì văn bản chính sách thương mại điện tử gồm các điều khoản pháp lý hoàn chỉnh. Việc không ngắt đôi câu giúp giữ nguyên vẹn ngữ cảnh nghĩa của điều khoản khi tính vector embedding.
- **Code snippet (nếu custom):**
```python
from src.chunking import SentenceChunker
chunker = SentenceChunker(max_sentences_per_chunk=3)
```

**Thành viên 2 — Nguyễn Lê Quân**
- **Loại chiến lược:** RecursiveChunker
- **Mô tả & lý do chọn:** Sử dụng `RecursiveChunker(chunk_size=200)` ưu tiên tách theo dấu đoạn `\n\n` và `\n` để bảo toàn cấu trúc mục nhỏ của các bài viết hướng dẫn trên Shopee Trung tâm trợ giúp.
- **Code snippet (nếu custom):**
```python
from src.chunking import RecursiveChunker
chunker = RecursiveChunker(chunk_size=200)
```

**Thành viên 3 — Đinh Tuấn Minh**
- **Loại chiến lược:** FixedSizeChunker
- **Mô tả & lý do chọn:** Sử dụng `FixedSizeChunker(chunk_size=200, overlap=20)` làm đường cơ sở so sánh hiệu năng và số lượng chunk sinh ra đối với văn bản dài.
- **Code snippet (nếu custom):**
```python
from src.chunking import FixedSizeChunker
chunker = FixedSizeChunker(chunk_size=200, overlap=20)
```

**Thành viên 4 — Trịnh Đắc Vụ**
- **Loại chiến lược:** SentenceChunker (max=5)
- **Mô tả & lý do chọn:** Thử nghiệm nâng số câu tối đa lên 5 câu/chunk để tăng phạm vi ngữ cảnh cho các trường hợp câu hỏi quy trình dài.
- **Code snippet (nếu custom):**
```python
from src.chunking import SentenceChunker
chunker = SentenceChunker(max_sentences_per_chunk=5)
```

**Thành viên 5 — Nguyễn Thị Hải Yến**
- **Loại chiến lược:** RecursiveChunker (chunk_size=400)
- **Mô tả & lý do chọn:** Thử nghiệm tăng kích thước chunk lên 400 ký tự đối với chia đệ quy nhằm giữ trọn vẹn danh sách liệt kê điều kiện.
- **Code snippet (nếu custom):**
```python
from src.chunking import RecursiveChunker
chunker = RecursiveChunker(chunk_size=400)
```

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Đỗ Đình Thi | SentenceChunker (max=3) | 10/10 | Giữ trọn vẹn ngữ cảnh từng điều khoản câu, đạt 100% Hit@3 | Số lượng ký tự mỗi chunk biến thiên tùy độ dài câu |
| Nguyễn Lê Quân | RecursiveChunker (200) | 10/10 | Tôn trọng cấu trúc đoạn văn, phân tách mục tiêu đề tốt | Đôi khi tạo chunk nhỏ nếu văn bản có nhiều dòng ngắn |
| Đinh Tuấn Minh | FixedSizeChunker (200, 20) | 10/10 | Kích thước đồng đều, mật độ chunk dày | Dễ bị ngắt đôi câu ở cuối ranh giới 200 ký tự |
| Trịnh Đắc Vụ | SentenceChunker (max=5) | 10/10 | Ngữ cảnh rộng hơn cho quy trình | Đoạn chunk dài hơn, tăng chi phí tính toán |
| Nguyễn Thị Hải Yến | RecursiveChunker (400) | 10/10 | Giữ trọn bộ danh sách điều kiện trả hàng | Đôi khi lẫn ngữ cảnh thừa của các mục lân cận |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> `SentenceChunker` là chiến lược tốt nhất cho chủ đề chính sách TMĐT. Vì các chính sách pháp lý chứa thông tin quy định theo câu hoàn chỉnh; việc bảo toàn toàn bộ câu giúp mô hình `LocalEmbedder` hiểu chính xác 100% ý nghĩa ngữ nghĩa mà không bị mất bối cảnh do cắt dòng ngẫu nhiên.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Thời hạn bộ phận tiếp nhận khiếu nại của Shopee giải quyết các tranh chấp không phải là khiếu nại Trả Hàng/Hoàn Tiền là bao nhiêu ngày làm việc? | `"đưa ra hướng giải quyết dựa trên các thông tin/tài liệu thu thập được trong vòng 07 ngày làm việc kể từ ngày nhận được đầy đủ các thông tin/tài liệu có liên quan đến vụ việc."` | `shopee-payment-limits` (chunk 2) |
| 2 | Người Bán cần đáp ứng điều kiện pháp lý gì về giấy phép khi đăng bán sản phẩm trên Shopee nếu Người Bán là pháp nhân có vốn đầu tư nước ngoài? | `"Đối với Người Bán là pháp nhân có vốn đầu tư nước ngoài, Người Bán cần có Giấy phép kinh doanh phù hợp với quy định của pháp luật hiện hành."` | `shopee-product-listing-rules-previous` (chunk 1) |
| 3 | Quy trình khởi tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền đối với Người Mua được thực hiện như thế nào ở Bước 1? | `"Để tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền tới Shopee, Người Mua cần bấm khiếu nại ngay trong ứng dụng Shopee/website www.shopee.vn, mục “Đơn Mua”."` | `shopee-payment-limits` (chunk 1) |
| 4 | Theo Chính sách Trả hàng và Hoàn tiền, Người Mua có thể yêu cầu trả hàng/hoàn tiền trong những trường hợp nào? | `"Người Mua đồng ý rằng Người Mua chỉ có thể yêu cầu trả hàng/hoàn tiền trong các trường hợp sau: Người Mua đã thanh toán... không nhận được Sản Phẩm..."` | `shopee-return-refund-policy` (chunk 4) |
| 5 | Trong quy định xử lý khiếu nại/tranh chấp của Shopee, trường hợp ngoại lệ nào sẽ không sử dụng quyết định cuối cùng của Shopee? | `"Quyết định của Shopee là quyết định cuối cùng trừ trường hợp vụ việc được xử lý bởi cơ quan nhà nước có thẩm quyền theo quy định của pháp luật."` | `shopee-payment-limits` (chunk 0) |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | Thời hạn giải quyết tranh chấp khiếu nại | SentenceChunker / RecursiveChunker | Có (Top 1) | Hit 100% với LocalEmbedder (score: 0.7656) |
| 2 | Điều kiện giấy phép người bán nước ngoài | RecursiveChunker / FixedSizeChunker | Có (Top 1) | Hit 100% với LocalEmbedder (score: 0.9034) |
| 3 | Quy trình khởi tạo khiếu nại ở Bước 1 | FixedSizeChunker / SentenceChunker | Có (Top 1) | Hit 100% với LocalEmbedder (score: 0.7697) |
| 4 | Các trường hợp được yêu cầu trả hàng | RecursiveChunker / SentenceChunker | Có (Top 1) | Hit 100% với LocalEmbedder (score: 0.7864) |
| 5 | Trường hợp ngoại lệ xử lý tranh chấp | SentenceChunker / FixedSizeChunker | Có (Top 1) | Hit 100% với LocalEmbedder (score: 0.8244) |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Lọc bằng metadata mang lại hiệu quả rất rõ rệt ở Câu hỏi 2 (điều kiện giấy phép của người bán) và Câu hỏi 3 (quy trình khởi tạo khiếu nại của người mua). Việc pre-filter theo `customer_role: seller` hoặc `customer_role: buyer` giúp loại bỏ toàn bộ các tài liệu dành cho đối tượng ngược lại, giúp nâng cao độ chính xác Top 1 và giảm thiểu nhiễu tín hiệu vector.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> 1. Việc sử dụng mô hình nhúng ngữ nghĩa thật (`LocalEmbedder` - `sentence-transformers`) giúp nâng tỷ lệ tìm kiếm chính xác Hit@3 từ 20% - 40% (khi dùng Mock) lên **100.0%** trên toàn bộ bộ câu hỏi kiểm thử.
> 2. Sự kết hợp giữa `SentenceChunker` và `Metadata Pre-filtering` tạo ra ngữ cảnh gọn gàng, hỗ trợ RAG Agent tạo ra câu trả lời chính xác mà không bị quá tải token.

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng một tập tài liệu, nếu cắt ngẫu nhiên theo ký tự (`FixedSize`) sẽ làm ngắt đôi các điều khoản pháp lý quan trọng làm giảm điểm tương đồng; trong khi cắt theo ranh giới câu (`SentenceChunker`) hoặc phân đoạn ngữ nghĩa (`RecursiveChunker`) giúp bảo toàn trọn vẹn ý nghĩa của điều khoản.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nếu làm lại, nhóm sẽ thiết kế thêm một Custom Chunker chuyên biệt (Header-based Chunker) để tự động chia đoạn theo các tiêu đề H1, H2, H3 của bài viết trợ giúp Shopee, giúp liên kết chặt chẽ phần tiêu đề bài viết với từng đoạn điều khoản chi tiết.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
