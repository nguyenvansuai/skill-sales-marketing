---
name: seo-website-landing
description: Kiểm tra và tối ưu website, trang bán hàng (landing page) cho doanh nghiệp Việt Nam — SEO trên Google cho từ khóa tiếng Việt (có dấu/không dấu, tìm theo khu vực "gần đây", "quận 7"), cấu trúc trang, tiêu đề, mô tả, tốc độ trên điện thoại, dữ liệu có cấu trúc, Google Business Profile cho cửa hàng; tối ưu để được AI (ChatGPT, Gemini, Google AI Overviews) trích dẫn; viết và soát landing page theo phễu chuyển đổi (tiêu đề, lợi ích, bằng chứng, form, nút Zalo/gọi), thông tin bắt buộc của website bán hàng. Dùng khi người dùng nói "kiểm tra SEO website", "web không lên Google", "viết landing page", "trang bán hàng ít đơn", "tối ưu Google Maps cửa hàng", "lên top tìm kiếm", "AI có nhắc tới thương hiệu tôi không".
---

# SEO, website và landing page

Đọc `references/nguyen-tac-chung.md`, `references/checklist-seo-landing.md`.
Khác `thuong-hieu-noi-dung` (viết bài, lịch đăng): skill này lo **cấu trúc, kỹ thuật, khả năng được tìm thấy và tỷ lệ chuyển đổi** của website/landing. Form thu thông tin → soát `kiem-tra-phap-ly-quang-cao` (`--doctype form`).

## 1. Xác định trường hợp (hỏi tối đa 2 câu: có link web không, mục tiêu trang)

| # | Trường hợp | Việc phải làm | Đầu ra |
|---|---|---|---|
| A | Có website, cần kiểm SEO | Đọc trang (công cụ đọc web nếu có), đi qua checklist kỹ thuật + nội dung; ưu tiên theo tác động | Bảng vấn đề → cách sửa → ưu tiên |
| B | Chưa có website / web mới | Cấu trúc trang theo nhóm từ khóa khách thật tìm; thông tin bắt buộc của web bán hàng | Sơ đồ trang + danh sách trang |
| C | Viết/soát landing page | Theo phễu: tiêu đề → lợi ích → bằng chứng → ưu đãi → form/CTA → câu hỏi thường gặp | Bản landing hoàn chỉnh + điểm cần A/B |
| D | Cửa hàng địa phương | Google Business Profile: danh mục, giờ, ảnh, đánh giá, bài đăng | Checklist + mẫu trả lời đánh giá |
| E | Được AI trích dẫn | Trả lời trực tiếp câu hỏi khách, dữ liệu có cấu trúc, nguồn đáng tin bên ngoài | Danh sách câu hỏi + trang cần có |

## 2. Kiểm tra mới nhất

Hướng dẫn của Google (Search Central), yêu cầu Google Business Profile, quy định thông báo/đăng ký website TMĐT với Bộ Công Thương (online.gov.vn) — `[CẦN KIỂM TRA]` sau Luật TMĐT 122/2025 có hiệu lực 01/07/2026 → tìm nguồn chính thức, ghi ngày.

## 3. Xử lý

- Từ khóa: lấy từ cách khách thật hỏi (inbox, bình luận, Google Search Console nếu người dùng xuất được) — không bịa lượng tìm kiếm; có công cụ thì ghi nguồn.
- Mỗi vấn đề ghi: trang, hiện trạng, cách sửa, mức ưu tiên (cao: chặn index, trang chậm trên điện thoại, thiếu tiêu đề; thấp: tinh chỉnh).
- Landing: một trang một mục tiêu; nút gọi/Zalo thấy ngay trên điện thoại; bằng chứng thật; giá rõ ràng.
- Nội dung trên trang qua soát pháp lý quảng cáo (tuyệt đối hóa, như thuốc, so sánh).

## 4. Đầu ra

1. Kết luận 1 câu: vấn đề lớn nhất đang làm mất khách/mất thứ hạng.
2. Bảng vấn đề/ưu tiên hoặc bản landing hoàn chỉnh.
3. Việc cần làm 30 ngày, người làm (marketing/dev) `[CẦN BỔ SUNG]`.
4. Anh/chị tự làm: sửa trên CMS, gửi sitemap trong Search Console, cập nhật Google Business Profile.
5. "Không cam kết thứ hạng; đối chiếu hướng dẫn hiện hành của Google."

## Không được làm

- Cam kết "lên top 1 trong X ngày".
- Đề xuất mua backlink, nhồi từ khóa, trang ẩn, đánh giá giả trên Google Maps.
- Sửa website trực tiếp khi chưa được yêu cầu.

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **Google Drive** · **Shopify**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Shopify: đọc tiêu đề, mô tả sản phẩm, trang để rà SEO; sửa nội dung trang chỉ sau khi xác nhận.
2. Lưu bảng từ khóa, đề xuất sửa từng trang vào Drive.

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
