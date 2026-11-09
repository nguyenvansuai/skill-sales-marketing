---
name: quan-ly-doi-sales
description: Quản lý đội bán hàng cho doanh nghiệp Việt Nam — giao chỉ tiêu theo người từ kế hoạch doanh thu, KPI hoạt động (cuộc gọi, lead, cuộc hẹn, báo giá) và KPI kết quả, cơ chế hoa hồng theo mức đạt chỉ tiêu tính trên tiền đã thu, dự báo doanh số tháng từ pipeline (cam kết / có khả năng / kỳ vọng), họp đội hằng tuần, đánh giá và kèm cặp sales, tuyển và đào tạo sales mới. Dùng khi người dùng nói "giao KPI cho sales", "tính hoa hồng tháng này", "cơ chế lương thưởng sales", "dự báo doanh số tháng sau", "họp sales hằng tuần", "nhân viên sales không đạt chỉ tiêu", "đánh giá sales".
---

# Quản lý đội sales

Đọc `references/nguyen-tac-chung.md`, `references/khung-doi-sales.md`.
Khác `quy-trinh-ban-hang-crm` (thiết kế giai đoạn, công cụ) và `ke-hoach-ngan-sach-kpi` (phễu tổng của doanh nghiệp): skill này chia chỉ tiêu **theo người**, tính **tiền thưởng**, **dự báo** và **kèm cặp**.

## 1. Xác định trường hợp (hỏi tối đa 2 câu)

| # | Trường hợp | Việc phải làm | Đầu ra |
|---|---|---|---|
| A | Giao chỉ tiêu | Từ kế hoạch tổng (`ke-hoach-ngan-sach-kpi`) chia theo năng lực thật (doanh số 3 tháng), khu vực, thâm niên; KPI hoạt động suy ngược từ tỷ lệ chuyển đổi thật của từng người | Bảng chỉ tiêu tháng/tuần theo người |
| B | Cơ chế hoa hồng | Bậc theo % đạt chỉ tiêu, tính trên tiền đã thu; trần; điều kiện (trả hàng, công nợ quá hạn trừ lại) | Quy chế + bảng tính thử 3 mức đạt |
| C | Tính hoa hồng kỳ này | Chạy script trên file kết quả | Bảng hoa hồng từng người |
| D | Dự báo | Pipeline có ngày dự kiến chốt + xác suất → cam kết/có khả năng/kỳ vọng so chỉ tiêu | Bảng dự báo + rủi ro |
| E | Kèm cặp, đánh giá | Phễu từng người so trung vị đội → điểm nghẽn (ít lead, chốt thấp, giá trị nhỏ) → 1–2 hành vi cần sửa | Kế hoạch kèm cặp 30 ngày |
| F | Tuyển, đào tạo sales mới | Tiêu chí tuyển, lộ trình 30-60-90 ngày, kịch bản luyện tập | Kế hoạch onboarding |

## 2. Kiểm tra mới nhất

Hoa hồng có thể là một phần tiền lương (Bộ luật Lao động 2019) → ghi trong hợp đồng/quy chế lương; thuế TNCN, bảo hiểm trên khoản hoa hồng → hỏi kế toán `[CẦN KIỂM TRA]`. Bộ `skill-ho-kinh-doanh` có skill về lương, bảo hiểm nhân viên cho hộ kinh doanh.

## 3. Xử lý

- Hoa hồng: `python3 scripts/hoa_hong_du_bao.py hoa-hong ket_qua.csv --bac "80%=2%,100%=3%,120%=4%" --tran 5%`
- Dự báo: `python3 scripts/hoa_hong_du_bao.py du-bao co_hoi.csv --thang 12/2026 --chi-tieu "An=300tr,Bình=250tr"` (CSV xuất từ sheet "Cơ hội" của file pipeline).
- Kiểm tra cơ chế trước khi ban hành: chạy thử với kết quả 3 tháng gần nhất — tổng hoa hồng / doanh số có trong ngân sách không; có ai lợi dụng được không (dồn đơn cuối kỳ, đơn ảo rồi trả).
- So sánh người với **trung vị của chính đội**, không với "chuẩn ngành".

## 4. Đầu ra

1. Kết luận 1 câu: đội đang ở đâu so chỉ tiêu; điểm nghẽn chính.
2. Bảng chỉ tiêu/hoa hồng/dự báo — "Đã kiểm tra phép tính".
3. Việc cần làm tuần này: theo người, cụ thể.
4. Anh/chị tự làm: duyệt quy chế, công bố, chi trả, họp 1-1.
5. "Quy chế lương thưởng ghi vào hợp đồng/quy chế nội bộ; thuế, bảo hiểm hỏi kế toán."

## Không được làm

- Đánh giá con người bằng nhận xét cá nhân không dựa trên số liệu/hành vi quan sát được.
- Đề xuất cơ chế phạt trừ lương trái luật `[CẦN KIỂM TRA]`; hoa hồng tính trên đơn chưa thu tiền.
- Chia sẻ bảng hoa hồng có thông tin cá nhân ra ngoài người có thẩm quyền.

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **HubSpot CRM (ChatGPT chưa có connector này)** · **Google Drive** · **Google Calendar**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Lấy số liệu hoạt động và kết quả theo từng người từ HubSpot (cuộc gọi, cuộc hẹn, deal thắng) để tính KPI, hoa hồng.
2. Lưu bảng chỉ tiêu, bảng hoa hồng vào Drive; tạo lịch họp sales tuần, 1-1 (sau khi xác nhận).

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
