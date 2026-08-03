# Benchmark Queries - Demo Corpus Evaluation (Data Foundations Day 7)

Bộ 5 câu hỏi đánh giá (Benchmark Queries) đa dạng được biên soạn trực tiếp từ tập tài liệu trong thư mục `data/demo/`.

---

## Bảng Tổng Hợp 5 Câu Hỏi Đánh Giá (Benchmark Queries)

| # | Loại Query | Câu hỏi (Benchmark Query) | Gold Answer (Trích dẫn trực tiếp từ Corpus) | File & `doc_id` | Chunk kỳ vọng (Nội dung / Ngữ cảnh chứa đáp án) |
|---|---|---|---|---|---|
| **1** | **Số liệu** | Thời hạn bộ phận tiếp nhận khiếu nại của Shopee giải quyết các tranh chấp không phải là khiếu nại Trả Hàng/Hoàn Tiền là bao nhiêu ngày làm việc? | `"đưa ra hướng giải quyết dựa trên các thông tin/tài liệu thu thập được trong vòng 07 ngày làm việc kể từ ngày nhận được đầy đủ các thông tin/tài liệu có liên quan đến vụ việc."` | `shopee-payment-limits copy.md`<br>(`shopee-payment-limits`) | **Mục 1 - Bước 3:** *"Đối với các tranh chấp không phải là khiếu nại Trả Hàng/Hoàn Tiền, Shopee yêu cầu các bên tranh chấp cung cấp đầy đủ thông tin/tài liệu liên quan đến vụ việc, và đưa ra hướng giải quyết dựa trên các thông tin/tài liệu thu thập được trong vòng 07 ngày làm việc kể từ ngày nhận được đầy đủ các thông tin/tài liệu có liên quan đến vụ việc."* |
| **2** | **Điều kiện** | Người Bán cần đáp ứng điều kiện pháp lý gì về giấy phép khi đăng bán sản phẩm trên Shopee nếu Người Bán là pháp nhân có vốn đầu tư nước ngoài? | `"Đối với Người Bán là pháp nhân có vốn đầu tư nước ngoài, Người Bán cần có Giấy phép kinh doanh phù hợp với quy định của pháp luật hiện hành."` | `shopee-product-listing-rules-previous copy.md`<br>(`shopee-product-listing-rules-previous`) | **Mục B.1.b:** *"Khi đăng bán sản phẩm trên Shopee, Người Bán có trách nhiệm tuân thủ các quy định... Đối với Người Bán là pháp nhân có vốn đầu tư nước ngoài, Người Bán cần có Giấy phép kinh doanh phù hợp với quy định của pháp luật hiện hành."* |
| **3** | **Quy trình** | Quy trình khởi tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền đối với Người Mua được thực hiện như thế nào ở Bước 1? | `"Để tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền tới Shopee, Người Mua cần bấm khiếu nại ngay trong ứng dụng Shopee/website www.shopee.vn, mục “Đơn Mua”."` | `shopee-payment-limits copy.md`<br>(`shopee-payment-limits`) | **Mục 1 - Bước 1:** *"Để tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền tới Shopee, Người Mua cần bấm khiếu nại ngay trong ứng dụng Shopee/website www.shopee.vn, mục “Đơn Mua”. Hệ thống sẽ ghi nhận khiếu nại này của Người Mua..."* |
| **4** | **Liệt kê** | Theo Chính sách Trả hàng và Hoàn tiền, Người Mua có thể yêu cầu trả hàng/hoàn tiền trong những trường hợp nào? | `"Người Mua đồng ý rằng Người Mua chỉ có thể yêu cầu trả hàng/hoàn tiền trong các trường hợp sau: Người Mua đã thanh toán bằng các phương thức thanh toán hợp lệ và trực tiếp trên Trang Shopee nhưng (i) không nhận được Sản Phẩm, hoặc (ii) không nhận được toàn bộ các Sản Phẩm đã đặt, hoặc (iii) nhận được Sản Phẩm là hàng giả, hàng nhái; Sản Phẩm bị lỗi hoặc bị hư hại trong quá trình vận chuyển; Người Bán giao sai Sản Phẩm cho Người Mua... Sản Phẩm hết hạn sử dụng..."` | `shopee-return-refund-policy copy.md`<br>(`shopee-return-refund-policy`) | **Mục 3.1:** *"Người Mua đồng ý rằng Người Mua chỉ có thể yêu cầu trả hàng/hoàn tiền trong các trường hợp sau: Người Mua đã thanh toán bằng các phương thức thanh toán hợp lệ và trực tiếp trên Trang Shopee nhưng (i) không nhận được Sản Phẩm... (iii) nhận được Sản Phẩm là hàng giả, hàng nhái; Sản Phẩm bị lỗi hoặc bị hư hại trong quá trình vận chuyển..."* |
| **5** | **Ngoại lệ** | Trong quy định xử lý khiếu nại/tranh chấp của Shopee, trường hợp ngoại lệ nào sẽ không sử dụng quyết định cuối cùng của Shopee? | `"Quyết định của Shopee là quyết định cuối cùng trừ trường hợp vụ việc được xử lý bởi cơ quan nhà nước có thẩm quyền theo quy định của pháp luật."` | `shopee-payment-limits copy.md`<br>(`shopee-payment-limits`) | **Mục 1. Quy Định Chung Về Giải Quyết Tranh Chấp:** *"Khi phát sinh tranh chấp hoặc khiếu nại, Shopee khuyến khích giải pháp thương lượng... Quyết định của Shopee là quyết định cuối cùng trừ trường hợp vụ việc được xử lý bởi cơ quan nhà nước có thẩm quyền theo quy định của pháp luật."* |

---

## Chi Tiết Nội Dung 5 Queries (Trích từ Corpus `data/demo/`)

### Query 1 — Số liệu (Numerical)
- **Câu hỏi**: Thời hạn bộ phận tiếp nhận khiếu nại của Shopee giải quyết các tranh chấp không phải là khiếu nại Trả Hàng/Hoàn Tiền là bao nhiêu ngày làm việc?
- **File**: `data/demo/shopee-payment-limits copy.md` (`doc_id`: `shopee-payment-limits`)
- **Gold Answer**: `"đưa ra hướng giải quyết dựa trên các thông tin/tài liệu thu thập được trong vòng 07 ngày làm việc kể từ ngày nhận được đầy đủ các thông tin/tài liệu có liên quan đến vụ việc."`
- **Chunk kỳ vọng**:
  > Bước 3: Khiếu nại Trả Hàng/Hoàn Tiền được xử lý theo Chính Sách Trả Hàng Và Hoàn Tiền của Shopee. Đối với các tranh chấp không phải là khiếu nại Trả Hàng/Hoàn Tiền, Shopee yêu cầu các bên tranh chấp cung cấp đầy đủ thông tin/tài liệu liên quan đến vụ việc, và đưa ra hướng giải quyết dựa trên các thông tin/tài liệu thu thập được trong vòng 07 ngày làm việc kể từ ngày nhận được đầy đủ các thông tin/tài liệu có liên quan đến vụ việc.

### Query 2 — Điều kiện (Condition)
- **Câu hỏi**: Người Bán cần đáp ứng điều kiện pháp lý gì về giấy phép khi đăng bán sản phẩm trên Shopee nếu Người Bán là pháp nhân có vốn đầu tư nước ngoài?
- **File**: `data/demo/shopee-product-listing-rules-previous copy.md` (`doc_id`: `shopee-product-listing-rules-previous`)
- **Gold Answer**: `"Đối với Người Bán là pháp nhân có vốn đầu tư nước ngoài, Người Bán cần có Giấy phép kinh doanh phù hợp với quy định của pháp luật hiện hành."`
- **Chunk kỳ vọng**:
  > B. QUY ĐỊNH CHUNG: 1. Nguyên tắc chung... b. Khi đăng bán sản phẩm trên Shopee, Người Bán có trách nhiệm tuân thủ các quy định tại Điều 117, Điều 120.4, Điều 121 của Luật Thương Mại và các văn bản quy phạm pháp luật có liên quan đến hoạt động trưng bày, giới thiệu hàng hóa, dịch vụ. Đối với Người Bán là pháp nhân có vốn đầu tư nước ngoài, Người Bán cần có Giấy phép kinh doanh phù hợp với quy định của pháp luật hiện hành.

### Query 3 — Quy trình (Process)
- **Câu hỏi**: Quy trình khởi tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền đối với Người Mua được thực hiện như thế nào ở Bước 1?
- **File**: `data/demo/shopee-payment-limits copy.md` (`doc_id`: `shopee-payment-limits`)
- **Gold Answer**: `"Để tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền tới Shopee, Người Mua cần bấm khiếu nại ngay trong ứng dụng Shopee/website www.shopee.vn, mục “Đơn Mua”."`
- **Chunk kỳ vọng**:
  > Bước 1: Để tạo khiếu nại yêu cầu Trả Hàng/Hoàn Tiền tới Shopee, Người Mua cần bấm khiếu nại ngay trong ứng dụng Shopee/website www.shopee.vn, mục “Đơn Mua”. Hệ thống sẽ ghi nhận khiếu nại này của Người Mua.. Các tranh chấp không phải là khiếu nại Trả Hàng/Hoàn Tiền có thể được gửi đến cho Shopee thông qua các phương thức liên hệ TẠI ĐÂY.

### Query 4 — Liệt kê (List)
- **Câu hỏi**: Theo Chính sách Trả hàng và Hoàn tiền, Người Mua có thể yêu cầu trả hàng/hoàn tiền trong những trường hợp nào?
- **File**: `data/demo/shopee-return-refund-policy copy.md` (`doc_id`: `shopee-return-refund-policy`)
- **Gold Answer**: `"Người Mua đồng ý rằng Người Mua chỉ có thể yêu cầu trả hàng/hoàn tiền trong các trường hợp sau: Người Mua đã thanh toán bằng các phương thức thanh toán hợp lệ và trực tiếp trên Trang Shopee nhưng (i) không nhận được Sản Phẩm, hoặc (ii) không nhận được toàn bộ các Sản Phẩm đã đặt, hoặc (iii) nhận được Sản Phẩm là hàng giả, hàng nhái; Sản Phẩm bị lỗi hoặc bị hư hại trong quá trình vận chuyển; Người Bán giao sai Sản Phẩm cho Người Mua... Sản Phẩm hết hạn sử dụng..."`
- **Chunk kỳ vọng**:
  > 3.1. Người Mua đồng ý rằng Người Mua chỉ có thể yêu cầu trả hàng/hoàn tiền trong các trường hợp sau: Người Mua đã thanh toán bằng các phương thức thanh toán hợp lệ và trực tiếp trên Trang Shopee nhưng (i) không nhận được Sản Phẩm, hoặc (ii) không nhận được toàn bộ các Sản Phẩm đã đặt, hoặc (iii) nhận được Sản Phẩm là hàng giả, hàng nhái; Sản Phẩm bị lỗi hoặc bị hư hại trong quá trình vận chuyển...

### Query 5 — Ngoại lệ (Exception)
- **Câu hỏi**: Trong quy định xử lý khiếu nại/tranh chấp của Shopee, trường hợp ngoại lệ nào sẽ không sử dụng quyết định cuối cùng của Shopee?
- **File**: `data/demo/shopee-payment-limits copy.md` (`doc_id`: `shopee-payment-limits`)
- **Gold Answer**: `"Quyết định của Shopee là quyết định cuối cùng trừ trường hợp vụ việc được xử lý bởi cơ quan nhà nước có thẩm quyền theo quy định của pháp luật."`
- **Chunk kỳ vọng**:
  > Khi phát sinh tranh chấp hoặc khiếu nại, Shopee khuyến khích giải pháp thương lượng... Quyết định của Shopee là quyết định cuối cùng trừ trường hợp vụ việc được xử lý bởi cơ quan nhà nước có thẩm quyền theo quy định của pháp luật.
