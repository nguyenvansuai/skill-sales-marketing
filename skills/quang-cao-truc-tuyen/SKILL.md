---
name: quang-cao-truc-tuyen
description: Lên kế hoạch, viết mẫu và đọc số quảng cáo trả phí cho doanh nghiệp Việt Nam trên Facebook/Instagram (Meta), TikTok, Google, YouTube, Zalo Ads, quảng cáo trên sàn — chọn mục tiêu (tin nhắn, lead, đơn hàng, cuộc gọi), cấu trúc chiến dịch, tệp đối tượng, ngân sách thử nghiệm, mẫu quảng cáo và biến thể A/B; đọc file xuất số liệu để chẩn đoán CPM, CTR, CPC, chi phí/kết quả, so ROAS nền tảng báo với ROAS thật, phân loại dừng/giữ/tăng theo ngưỡng hòa vốn của chính doanh nghiệp. Dùng khi người dùng nói "chạy quảng cáo Facebook", "ads đắt quá", "giá tin nhắn cao", "đọc giúp số liệu quảng cáo", "nên tắt chiến dịch nào", "viết mẫu quảng cáo", "có nên tăng ngân sách không", "ROAS báo 5 mà không có lời".
---

# Quảng cáo trực tuyến

Đọc `references/nguyen-tac-chung.md`, `references/khung-quang-cao.md`, `references/phap-ly-marketing-vn.md` (mục 2).
Khác `ke-hoach-ngan-sach-kpi` (chia tổng ngân sách giữa các kênh) và `bao-cao-doi-soat-hieu-qua` (đối chiếu doanh thu thật đa kênh): skill này làm **bên trong nền tảng quảng cáo**. Chuyên sâu TikTok Ads/ads sàn cho agency → `agency-agents-vi`.

## 1. Xác định trường hợp (hỏi tối đa 2 câu)

| # | Trường hợp | Việc phải làm | Đầu ra |
|---|---|---|---|
| A | Bắt đầu chạy | Mục tiêu tối ưu khớp cách bán (inbox → tin nhắn; web có theo dõi chuyển đổi → mua hàng; B2B → lead form); ngân sách thử nghiệm; 2–3 tệp × 3 mẫu | Cấu trúc chiến dịch + đặt tên |
| B | Viết mẫu quảng cáo | Theo insight, mỗi mẫu 1 ý: hook – lợi ích – bằng chứng – CTA; 3–5 biến thể | Bảng mẫu + gợi ý hình/video |
| C | Đọc số, chẩn đoán | Chạy script, so trung vị tài khoản, phân loại theo ngưỡng hòa vốn | Bảng chẩn đoán + việc làm 7 ngày |
| D | Tăng/giảm ngân sách | Chỉ tăng nhóm trên mục tiêu, tăng từng bước; nhóm dưới hòa vốn sửa hoặc dừng | Kế hoạch điều chỉnh (người dùng tự bấm) |
| E | Sản phẩm thuộc nhóm đặc biệt | Kiểm xác nhận nội dung; chính sách nền tảng với ngành (mỹ phẩm, TPCN, y tế, tài chính) | Danh sách điều kiện trước khi chạy |

## 2. Kiểm tra mới nhất (bắt buộc)

Tên mục tiêu chiến dịch, tùy chọn tối ưu, chính sách quảng cáo theo ngành của Meta/TikTok/Google đổi thường xuyên → có công cụ tìm kiếm thì tra trang trợ giúp chính thức tháng hiện tại; ghi nguồn + ngày. Không kiểm tra được → "giao diện/chính sách kiểm tra lần cuối ngày …, anh/chị đối chiếu trong Trình quản lý quảng cáo".

## 3. Xử lý

- Ngưỡng: ROAS/CPA hòa vốn từ `gia-san-pham-khuyen-mai`; CPL tối đa = CPA hòa vốn × tỷ lệ chốt thật.
- Đọc số: `python3 scripts/doc_so_ads.py ads.csv --roas-hoa-von 2,36 --roas-muc-tieu 3,1 --cpl-toi-da 30000 --toi-thieu-chi-phi 1tr`
- Số nền tảng tự báo ≠ đơn thật: ưu tiên cột `doanh_thu_that` từ đối soát; thiếu → ghi rõ "ROAS theo nền tảng báo".
- Chiến dịch chi chưa đủ → "chưa đủ dữ liệu", không kết luận.
- Mẫu quảng cáo: qua soát `kiem-tra-phap-ly-quang-cao` trước khi giao (tuyệt đối hóa, như thuốc, giảm > 50%, so sánh).

## 4. Đầu ra

1. Kết luận 1 câu: tài khoản đang lãi/lỗ theo số thật; 1 việc quan trọng nhất.
2. Bảng chẩn đoán/cấu trúc/mẫu quảng cáo — "Đã kiểm tra phép tính".
3. Việc cần làm 7 ngày: dừng/sửa/giữ/tăng từng chiến dịch, lý do, chỉ số theo dõi.
4. Anh/chị tự làm: thao tác trong Trình quản lý quảng cáo, thanh toán, duyệt mẫu.
5. "Chính sách quảng cáo nền tảng và luật quảng cáo kiểm tra lần cuối ngày …"

## Không được làm

- Đăng nhập tài khoản quảng cáo, bật/tắt, đổi ngân sách thay người dùng.
- Dùng CPM/CPL/ROAS "trung bình ngành" không nguồn làm ngưỡng.
- Đề xuất lách kiểm duyệt (đọc lái, ảnh trước-sau cơ thể khi nền tảng cấm, landing "che").
