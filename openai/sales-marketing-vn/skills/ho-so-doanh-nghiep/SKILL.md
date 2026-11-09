---
name: ho-so-doanh-nghiep
description: Lập và cập nhật hồ sơ doanh nghiệp dùng chung cho cả bộ skill sales – marketing Việt Nam — sản phẩm, giá bán và giá vốn, mô hình B2C/B2B, kênh bán (sàn, inbox, Zalo, đại lý, sales trực tiếp), khách hàng mục tiêu, đối thủ, pháp nhân, ngành có điều kiện quảng cáo (mỹ phẩm, thực phẩm, thiết bị y tế…), giọng thương hiệu, chính sách đổi trả, mục tiêu doanh thu. Trích từ website, catalogue, bảng giá; trường thiếu ghi [?] và chỉ hỏi phần thiếu. Dùng khi người dùng nói "lập hồ sơ doanh nghiệp", "bắt đầu làm marketing cho shop tôi", "đây là thông tin công ty", "cập nhật giá mới", "đổi kênh bán", "nhớ thông tin sản phẩm của tôi".
---

# Hồ sơ doanh nghiệp

Đọc `references/nguyen-tac-chung.md`, mẫu ở `references/mau-ho-so.md`.
Khác mọi skill còn lại: skill này **chỉ thu thập và lưu bối cảnh**, không lập kế hoạch, không viết nội dung. 16 skill kia đọc hồ sơ này trước để khỏi hỏi lại.

## 1. Xác định trường hợp

| # | Trường hợp | Việc phải làm | Đầu ra |
|---|---|---|---|
| A | Chưa có hồ sơ, không có tài liệu | Hỏi bộ trường bắt buộc, **chia tối đa 2 lượt** (lượt 1: mục 1–6, lượt 2: mục 7–12) | Hồ sơ mới |
| B | Có tài liệu (link web, fanpage, catalogue, bảng giá, ảnh menu) | Trích tự động; trường không có trong tài liệu ghi `[?]`; chỉ hỏi phần `[?]` | Hồ sơ mới |
| C | Đã có hồ sơ | Đọc hồ sơ, hỏi 3 trường hay đổi: giá/giá vốn, kênh, mục tiêu doanh thu; giữ phần còn lại | Hồ sơ cập nhật + ngày cập nhật |

Tìm hồ sơ ở: `.agents/ho-so-doanh-nghiep.md` (khi chạy trong môi trường có thư mục làm việc, ví dụ Codex) → file "Hồ sơ doanh nghiệp" trong Project/Knowledge → cuộc trò chuyện.

## 2. Trường bắt buộc (12 mục)

1. Tên thương hiệu, ngành, sản phẩm/dịch vụ chủ lực (tối đa 5)
2. **Giá bán và giá vốn** từng sản phẩm chủ lực (giá vốn gồm nhập + đóng gói)
3. Mô hình: B2C / B2B / cả hai
4. Kênh bán đang dùng và tỷ trọng doanh thu ước tính
5. Khách hàng mục tiêu (ai mua, ai quyết định, mua vì vấn đề gì)
6. Đối thủ chính (2–3 tên) và điểm khác biệt
7. Pháp nhân: hộ kinh doanh / công ty; có xuất hóa đơn VAT không
8. **Ngành đặc biệt?** — sản phẩm có thuộc 11 nhóm của NĐ 342/2025 không (mỹ phẩm, thực phẩm, sữa trẻ nhỏ, hóa chất gia dụng, thiết bị y tế, khám chữa bệnh, thú y/BVTV/thức ăn chăn nuôi, phân bón, giống cây trồng, thuốc, đồ uống có cồn) — xem `references/phap-ly-marketing-vn.md` mục 2.5
9. Giọng thương hiệu: xưng hô (anh/chị, bạn, quý khách), 3 tính từ, từ cấm dùng
10. Chính sách đổi trả, bảo hành, giao hàng
11. Mục tiêu doanh thu (tháng/quý) và ngân sách marketing hiện có
12. Số liệu thật đang có: tỷ lệ chốt, chi phí/tin nhắn, AOV (giá trị đơn trung bình) — không có thì ghi "chưa có"

Quy tắc: giá vốn và số liệu thật **không được đoán**. Người dùng chưa biết → `[CẦN BỔ SUNG]`, giải thích vì sao cần (skill giá, KPI, đối soát dùng các số này).

## 3. Xử lý

- Đọc tài liệu người dùng gửi; mỗi thông tin trích ra ghi nguồn ngắn (vd. "web, trang Giới thiệu").
- Ngành thuộc nhóm đặc biệt → ghi rõ nhóm số mấy theo NĐ 342/2025, hỏi đã có văn bản xác nhận nội dung quảng cáo chưa.
- Không lưu: CCCD, số tài khoản, mật khẩu, danh sách khách hàng có SĐT.

## 4. Đầu ra

1. Một câu: hồ sơ đã đủ bao nhiêu/12 mục.
2. Hồ sơ theo đúng mẫu `references/mau-ho-so.md`, có dòng "Cập nhật: dd/mm/yyyy".
3. Bảng "Cần anh/chị kiểm tra": mọi `[?]` và `[CẦN BỔ SUNG]`.
4. Anh/chị tự làm:
   - Môi trường có thư mục làm việc (Codex, ChatGPT desktop): lưu thành `.agents/ho-so-doanh-nghiep.md` (skill sẽ ghi file nếu được phép).
   - ChatGPT (web): tải file hồ sơ lên Project / tệp đính kèm để các skill khác đọc được.
5. Gợi ý skill tiếp theo theo nhu cầu: định giá → `gia-san-pham-khuyen-mai`; kế hoạch → `ke-hoach-ngan-sach-kpi`.

## Không được làm

- Tự điền giá vốn, tỷ lệ chuyển đổi, doanh thu "ước chừng".
- Lưu dữ liệu cá nhân của khách hàng vào hồ sơ.
- Lập kế hoạch hay viết nội dung trong skill này.
