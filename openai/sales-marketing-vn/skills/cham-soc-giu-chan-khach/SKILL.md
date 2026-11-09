---
name: cham-soc-giu-chan-khach
description: Chăm sóc khách hàng sau bán và giữ chân khách cho doanh nghiệp Việt Nam — hành trình chăm sóc theo thời điểm (sau giao hàng, hết hạn dùng, sinh nhật, ngày lễ, khách lâu không mua), chia nhóm khách theo lần mua gần nhất – số lần – giá trị (RFM), chương trình khách thân thiết, tích điểm, giới thiệu bạn bè, xử lý khiếu nại và đánh giá xấu, kéo khách quay lại; kênh Zalo OA/ZNS, email, SMS, gọi điện, nhóm Zalo/cộng đồng; chỉ gửi cho khách đã đồng ý, đúng khung giờ và tần suất theo NĐ 91/2020 và Luật 91/2025. Dùng khi người dùng nói "chăm sóc khách cũ", "khách mua 1 lần rồi thôi", "làm chương trình tích điểm", "kịch bản Zalo OA", "nhắc khách mua lại", "trả lời khiếu nại", "chia nhóm khách hàng", "tăng tỷ lệ quay lại".
---

# Chăm sóc và giữ chân khách hàng

Đọc `references/nguyen-tac-chung.md`, `references/khung-giu-chan.md`, `references/phap-ly-marketing-vn.md` (mục 3, 5, 6).
Khác `kich-ban-tu-van-chot-don` (khách đang cân nhắc mua) và `pr-su-kien-khung-hoang` (sự cố lan rộng): skill này lo **khách đã mua** — quay lại, mua thêm, giới thiệu. Chuyên sâu Zalo OA/nhóm Zalo cho agency → `agency-agents-vi`.

## 1. Xác định trường hợp (hỏi tối đa 2 câu)

| # | Trường hợp | Việc phải làm | Đầu ra | Căn cứ |
|---|---|---|---|---|
| A | Hành trình chăm sóc | Mốc thời gian theo vòng đời sản phẩm thật (thời gian dùng hết, bảo hành) → nội dung → kênh | Bảng hành trình + mẫu tin | NĐ 91/2020; quy định mẫu ZNS |
| B | Chia nhóm khách | RFM từ file đơn hàng; mỗi nhóm một mục tiêu | Bảng nhóm + hành động | Dữ liệu doanh nghiệp |
| C | Khách thân thiết / tích điểm | Quy đổi ≤ biên cho phép; thể lệ công khai | Thể lệ + chi phí ước tính | NĐ 239/2026 (không còn phải thông báo) |
| D | Giới thiệu bạn bè | Thưởng 1/2 chiều ≤ CPA hòa vốn | Thể lệ | `koc-affiliate-doi-tac` mục referral |
| E | Khiếu nại, đánh giá xấu | Lắng nghe → xin lỗi phần đúng → giải pháp cụ thể → hạn → đóng vòng | Mẫu trả lời công khai + riêng | Luật BVQLNTD `[CẦN KIỂM TRA]` |
| F | Khách lâu không mua | Hỏi lý do, ưu đãi quay lại (≤ 50% hoặc KM tập trung), dừng nếu khách từ chối | Chuỗi 2–3 tin | NĐ 91/2020 Đ13 |

## 2. Kiểm tra mới nhất (bắt buộc với Zalo)

Loại tin Zalo (ZNS chăm sóc/giao dịch, tin truyền thông OA), giới hạn ký tự, quy định duyệt mẫu và chi phí **đổi thường xuyên** → tra tài liệu chính thức của Zalo for Business, ghi ngày. Bộ trussary ghi nhận giới hạn 400 ký tự cho mẫu ZNS và cấm nội dung khuyến mại trong mẫu giao dịch `[THỨ CẤP]`.

## 3. Xử lý

- Chỉ gửi cho khách **đã đồng ý** nhận tin (có ngày, kênh trong CRM); không mua data.
- Tin quảng cáo: SMS 07:00–22:00, gọi 08:00–17:00; ≤ 3 tin, ≤ 3 email, ≤ 1 cuộc gọi/24 giờ; dừng ngay khi khách từ chối (NĐ 91/2020 Điều 13).
- Tin chăm sóc/giao dịch không chèn khuyến mại (quy định ZNS `[THỨ CẤP]`).
- RFM: `python3 scripts/rfm.py don_hang.csv --ngay-tinh 02/11/2026` (cột `ma_khach` dùng mã hoặc 4 số cuối SĐT; đơn huỷ/hoàn tự loại).
- Mỗi mẫu tin qua soát `kiem-tra-phap-ly-quang-cao --doctype bulk-message`.
- Đo: tỷ lệ mua lại, thời gian giữa 2 lần mua, doanh thu từ khách cũ (đo bằng `bao-cao-doi-soat-hieu-qua`).

## 4. Đầu ra

1. Kết luận 1 câu: nhóm khách đáng chăm nhất và hành động chính.
2. Bảng hành trình / nhóm RFM / thể lệ / mẫu trả lời khiếu nại.
3. Bộ mẫu tin theo kênh (đã soát).
4. Anh/chị tự làm: cài tự động hóa trên Zalo OA/CRM, duyệt mẫu ZNS, gửi tin.
5. "Chỉ gửi cho khách đã đồng ý; quy định Zalo kiểm tra lần cuối ngày …"

## Không được làm

- Gửi tin cho người chưa đồng ý, gửi ngoài khung giờ, gửi dồn.
- Đổi quà lấy đánh giá 5 sao, xóa/ẩn đánh giá xấu trái quy chế nền tảng.
- Gửi tin, cài chiến dịch thay người dùng.
