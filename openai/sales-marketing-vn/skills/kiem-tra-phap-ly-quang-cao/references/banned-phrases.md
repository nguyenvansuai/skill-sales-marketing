<!-- vlc-disable: all -->

# Cụm từ bị soát — dữ liệu cho validate_copy.py

> Ngày tổng hợp: 02/11/2026. Bảng tuyệt đối hóa và bảng cụm từ thư hàng loạt lấy từ trussary/vietnamese-language-skill (MIT, `skills/vietnamese-business-comms/references/banned-phrases.md`), giữ nguyên định dạng để engine đọc được. Căn cứ pháp lý: `phap-ly-marketing-vn.md` mục 2.1.

## Tuyệt đối hóa — khoản 11 Điều 8 Luật Quảng cáo 2012 (không bị Luật 75/2025 sửa)

Cấm khi **không có tài liệu hợp pháp chứng minh**. Vì vậy `LAW001` chỉ cảnh báo, và chú thích `<!-- proof: ... -->` (ghi tên tài liệu chứng minh) trên cùng dòng hoặc dòng trên sẽ tắt cảnh báo.

<!-- machine-readable: superlatives -->

| Mẫu | Bắt được | Ghi chú |
|---|---|---|
| `(?:tốt\|hay\|đẹp\|rẻ\|lớn\|to\|nhanh\|mạnh\|cao\|sang\|xịn\|uy tín\|chất lượng\|hiện đại\|cao cấp\|sang trọng\|đẳng cấp\|hoàn hảo\|tuyệt vời\|an toàn\|bền\|bán chạy\|yêu thích\|nổi tiếng\|hiệu quả\|trắng\|mỏng\|nhẹ)\s+nhất` | "tốt nhất, rẻ nhất, bán chạy nhất…" | Cấu trúc chính bị cấm |
| `duy nhất` | "duy nhất" | Có trong luật |
| `số\s*(?:một\|1)\b` | "số một, số 1" | Có trong luật |
| `hàng đầu` | "hàng đầu" | Từ có nghĩa tương tự |
| `đứng đầu` | "đứng đầu" | Như trên |
| `vô địch` | "vô địch" | Như trên |
| `không ai sánh bằng` | "không ai sánh bằng" | Như trên |
| `top\s*1\b` | "top 1" | Cách nói thị trường VN |
| `\bno\.?\s*1\b` | "No.1" | Tiếng Anh |
| `(?<!#)#\s*1\b` | "#1" | Tiếng Anh; không bắt tiêu đề Markdown |
| `\bnumber\s+one\b` | "number one" | Tiếng Anh |
| `\bbest\s+seller\b` | "best seller" | Tuyên bố xếp hạng |

## Cụm từ khiến thư/tin nhắn giống gửi hàng loạt

<!-- machine-readable: calques -->

| ❌ Cụm từ | ✅ Thay bằng | Lý do |
|---|---|---|
| `kính gửi quý khách hàng thân mến` | `kính gửi anh/chị` | Chồng 2 cách xưng hô |
| `chúng tôi rất vui mừng thông báo` | `công ty xin thông báo` | Dịch từ thông cáo tiếng Anh |
| `hy vọng email này tìm thấy bạn` | `(bỏ hẳn câu này)` | Dịch word-by-word |
| `chúng tôi là công ty hàng đầu` | `công ty chúng tôi hoạt động trong lĩnh vực` | Tự xưng xếp hạng không bằng chứng |
| `cơ hội có một không hai` | `số lượng có hạn` | Quá đà, giống lừa đảo |
| `cam kết hoàn tiền 100% nếu không hiệu quả` | `chính sách đổi trả trong [số] ngày` | Cam kết kết quả; với sản phẩm sức khỏe là tuyên bố bị kiểm soát |
| `bạn phải thanh toán ngay` | `kính đề nghị quý khách thanh toán trước ngày` | Thô trong nhắc nợ |
