---
name: koc-affiliate-doi-tac
description: Tìm, thẩm định, ký và đo hiệu quả hợp tác KOL, KOC, người có ảnh hưởng, affiliate (TikTok Shop, Shopee, website), cộng tác viên bán hàng, đối tác chéo (co-marketing) cho doanh nghiệp Việt Nam — tiêu chí chọn theo dữ liệu thật thay vì lượt theo dõi, tính số đơn hòa vốn trước khi ký, brief nội dung đúng Luật Quảng cáo sửa đổi 2025 (người có ảnh hưởng phải dùng/hiểu sản phẩm, phải thông báo là quảng cáo), điều khoản hợp đồng, khấu trừ thuế khi trả tiền cho cá nhân, chương trình giới thiệu khách. Dùng khi người dùng nói "thuê KOC review", "tìm KOL cho sản phẩm", "làm affiliate TikTok", "hợp đồng với KOC", "KOC này có đáng tiền không", "brief cho creator", "chương trình giới thiệu bạn bè", "hợp tác với thương hiệu khác".
---

# KOC, affiliate và đối tác

Đọc `references/nguyen-tac-chung.md`, `references/phap-ly-marketing-vn.md` (mục 2.3), `references/khung-hop-tac.md`.
Khác `thuong-hieu-noi-dung` (doanh nghiệp tự viết) và `kiem-tra-phap-ly-quang-cao` (soát câu chữ): skill này lo **chọn đối tác, điều kiện hợp tác, tiền và đo kết quả**. Chuyên sâu kịch bản TikTok/livestream cho agency → `agency-agents-vi`.

## 1. Xác định trường hợp (hỏi tối đa 2 câu)

| # | Trường hợp | Việc phải làm | Đầu ra | Căn cứ |
|---|---|---|---|---|
| A | Chọn KOC/KOL | Tiêu chí: khách của KOC trùng khách mình, số liệu bán hàng thật lần trước, mức độ tương tác thật, rủi ro hình ảnh | Bảng chấm điểm + câu hỏi xin số liệu | — |
| B | Trước khi ký | Tính đơn hòa vốn theo phí cố định, hoa hồng, hàng tặng | Bảng so sánh KOC | `scripts/tinh_koc.py` |
| C | Brief nội dung | Thông điệp, điều được/không được nói, **nhãn quảng cáo**, KOC đã dùng sản phẩm, lịch duyệt | Brief 1 trang | Điều 15a Luật QC (sửa 2025) |
| D | Hợp đồng | Điều khoản: phạm vi, nhãn quảng cáo, quyền dùng nội dung, sửa/gỡ, thanh toán, thuế, phạt vi phạm | Danh sách điều khoản cho luật sư | Điều 6 Luật QC (hợp đồng quảng cáo) |
| E | Affiliate trên sàn/website | Tỷ lệ hoa hồng không vượt biên; mã/đường dẫn theo dõi; chống gian lận | Chính sách affiliate | Quy chế sàn (kiểm tra mới nhất) |
| F | Sau chiến dịch | Đơn thật, doanh thu thật theo mã/link → chi phí/đơn, lãi/lỗ | Bảng ROI từng KOC | Đối soát thật |
| G | Giới thiệu khách / đối tác chéo | Phần thưởng ≤ biên cho phép, điều kiện nhận, chống lạm dụng | Thể lệ | Khuyến mại → `gia-san-pham-khuyen-mai` |

## 2. Kiểm tra mới nhất

Chính sách affiliate/creator của TikTok Shop, Shopee; quy chế livestream; quy định thuế khi trả cho cá nhân (NĐ 253/2026 `[CẦN KIỂM TRA]`) → tra nguồn chính thức, ghi ngày; không kiểm được → nói rõ và chuyển kế toán.

## 3. Xử lý

- `python3 scripts/tinh_koc.py koc.csv --aov 350000 --bien-truoc-ads 42% [--thue-khau-tru <tỷ lệ kế toán xác nhận>]`
- Không ước lượng đơn từ lượt theo dõi/lượt xem. Xin KOC ảnh chụp báo cáo bán hàng có ngày.
- Brief bắt buộc có: chữ "Quảng cáo"/"Hợp tác cùng …"/#quangcao xuất hiện **ngay đầu và trong suốt** nội dung; xác nhận KOC đã dùng sản phẩm; danh sách câu cấm (như thuốc, tuyệt đối hóa, so sánh đối thủ).
- Sản phẩm nhóm đặc biệt (mỹ phẩm, TPBVSK…) → nội dung KOC phải khớp bản đã xác nhận (nếu thuộc diện); livestream → giấy tờ theo Điều 23 Luật TMĐT 122/2025.
- Kịch bản/caption KOC → soát `kiem-tra-phap-ly-quang-cao --doctype kol`.

## 4. Đầu ra

1. Kết luận 1 câu: nên ký ai, điều kiện gì; hoặc chiến dịch lãi/lỗ.
2. Bảng chấm điểm/so sánh/ROI — "Đã kiểm tra phép tính".
3. Brief hoặc danh sách điều khoản hợp đồng.
4. Anh/chị tự làm: đàm phán, ký, thanh toán, khấu trừ và nộp thuế theo kế toán.
5. "Hợp đồng nên được luật sư xem; thuế khi trả cho cá nhân hỏi kế toán."

## Không được làm

- Viết brief yêu cầu KOC giấu việc được trả tiền hoặc khen sản phẩm chưa dùng.
- Mua lượt xem, lượt theo dõi, đánh giá giả cho KOC.
- Ghi cứng tỷ lệ khấu trừ thuế khi chưa đối chiếu văn bản hiện hành.

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **Gmail** · **Google Drive** · **HubSpot CRM (ChatGPT chưa có connector này)**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Tạo nháp email mời hợp tác, gửi brief, thỏa thuận cho từng KOL/KOC.
2. Lưu danh sách đối tác, hợp đồng, bảng đo hiệu quả trên Drive; có HubSpot thì ghi đối tác thành công ty/liên hệ.

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
