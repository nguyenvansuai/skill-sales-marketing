# Khung kế hoạch marketing – bán hàng

> Ngày tổng hợp: 02/11/2026. Tham khảo cấu trúc từ minhnv0807/ai-business-skills (00-ke-hoach-mkt, 10-tinh-kpi-nguoc, 61-budget-planning) và coreyhaines31/marketingskills (marketing-plan) — MIT; đã bỏ toàn bộ benchmark không nguồn.

## 1. Cấu trúc bản kế hoạch (1–2 trang)

1. **Mục tiêu:** doanh thu, số khách mới, lợi nhuận — theo tháng.
2. **Hiện trạng (số thật):** doanh thu 3 tháng gần nhất theo kênh, AOV, tỷ lệ chốt, chi phí/lead, biên trước ads.
3. **Phễu ngược:** bảng từ `kpi_nguoc.py` (3 kịch bản).
4. **Phân bổ kênh:**

| Kênh | Vai trò (thu hút / chuyển đổi / giữ khách) | Ngân sách | KPI chính | Căn cứ (số thật / thử nghiệm) |
|---|---|---:|---|---|

5. **Lịch:** tháng → chiến dịch, sự kiện (Tết, ngày đôi, ngày ra mắt), nội dung chủ đạo.
6. **Nguồn lực:** người phụ trách từng kênh, công cụ.
7. **Rủi ro và điểm dừng:** ví dụ "CPL vượt X trong 7 ngày → dừng nhóm quảng cáo, xem lại nội dung".
8. **Mốc đo:** tuần 2 và tuần 4 chạy `bao-cao-doi-soat-hieu-qua`.

## 2. Lấy số liệu thật ở đâu

| Chỉ số | Nguồn |
|---|---|
| AOV | Báo cáo đơn hàng sàn / phần mềm bán hàng (đơn thành công) |
| Tỷ lệ chốt inbox | Số đơn từ inbox / số hội thoại mới (Meta Business Suite, Pancake, Zalo OA…) |
| Chi phí/tin nhắn | Chi phí quảng cáo / số hội thoại mới **đếm trong hộp thư**, không chỉ số nền tảng tự báo |
| Tỷ lệ thắng B2B | Số HĐ ký / số cơ hội đã báo giá trong 6–12 tháng |
| DT/điểm bán | Sell-in theo từng điểm 3 tháng gần nhất |

## 3. Mùa vụ thường gặp ở Việt Nam (để hỏi hệ số, không phải số liệu)

Tết Nguyên đán (thường tháng 1–2 dương lịch, đổi theo năm), 8/3, 30/4–1/5, 1/6, mùa tựu trường (8–9), 20/10, ngày đôi trên sàn (9.9, 10.10, 11.11, 12.12), Black Friday, Giáng sinh, mùa cưới (cuối năm). Hệ số từng tháng lấy từ doanh thu cùng kỳ năm trước của chính doanh nghiệp.

## 4. Ngưỡng ra quyết định (do doanh nghiệp tự đặt)

| Câu hỏi | Cách đặt ngưỡng |
|---|---|
| CPL tối đa chấp nhận | CPA hòa vốn × tỷ lệ chốt |
| ROAS tối thiểu | ROAS hòa vốn (từ `gia-san-pham-khuyen-mai`) |
| Dừng kênh thử nghiệm khi | Sau đủ ngân sách thử nghiệm mà CPL > 1,5 × ngưỡng (hệ số do doanh nghiệp chọn) |
