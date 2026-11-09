---
name: trade-marketing-diem-ban
description: Thiết kế và đo hiệu quả trade marketing cho kênh truyền thống ở Việt Nam — nhà phân phối, đại lý cấp 1–2, tạp hóa, cửa hàng, siêu thị/chuỗi — chương trình trưng bày, POSM, thưởng doanh số theo bậc, chiết khấu thanh toán sớm, chính sách đại lý, tuyển và kích hoạt điểm bán mới, kiểm tra độ phủ và sell-out; tính lãi/lỗ của chương trình theo mức tăng doanh số đo từ thử nghiệm thật, tính thưởng từng đại lý từ file doanh số. Dùng khi người dùng nói "làm chương trình cho đại lý", "chính sách đại lý", "thưởng doanh số bậc thang", "trưng bày tại tạp hóa", "mở rộng điểm bán", "chương trình trade có lời không", "tính thưởng đại lý quý này".
---

# Trade marketing và điểm bán

Đọc `references/nguyen-tac-chung.md`, `references/khung-trade.md`.
Khác `ke-hoach-ngan-sach-kpi` (tính cần bao nhiêu điểm bán, bao nhiêu ngân sách trade cho cả kỳ) và `gia-san-pham-khuyen-mai` (giá đại lý theo bậc chiết khấu): skill này **thiết kế, chạy thử và đo từng chương trình** tại điểm bán.

## 1. Xác định trường hợp (hỏi tối đa 2 câu)

| # | Trường hợp | Việc phải làm | Đầu ra |
|---|---|---|---|
| A | Chính sách đại lý mới | Điều kiện làm đại lý, bậc chiết khấu (giá từ `gia-san-pham-khuyen-mai`), thưởng doanh số, công nợ, vùng bán, hỗ trợ | Bảng chính sách + mẫu thỏa thuận cần luật sư xem |
| B | Chương trình trưng bày/POSM | Tiêu chuẩn trưng bày (vị trí, số mặt hàng), cách chụp ảnh kiểm tra, thưởng | Thể lệ + checklist kiểm tra |
| C | Thưởng doanh số theo bậc | Chọn kiểu bậc (đạt bậc / lũy tiến), tính trên file doanh số | Bảng thưởng từng đại lý |
| D | Đánh giá chương trình | Thử nghiệm ở 5–10 điểm so với nhóm đối chứng → mức tăng thật → ROI | Kết luận mở rộng/dừng |
| E | Mở rộng điểm bán | Danh sách khu vực, tiêu chí chọn điểm, kịch bản chào, gói kích hoạt | Kế hoạch tuyến + KPI sales thị trường |

## 2. Kiểm tra mới nhất

Quy định khuyến mại giữa thương nhân, hóa đơn cho chiết khấu thương mại/thưởng doanh số → `[CẦN KIỂM TRA]` với kế toán (xem bộ `skill-ho-kinh-doanh` cho phần thuế hộ kinh doanh). Chương trình có bốc thăm, quà cho người tiêu dùng → `gia-san-pham-khuyen-mai`.

## 3. Xử lý

- Hiệu quả: `python3 scripts/tinh_trade.py roi --so-diem 40 --chi-phi-moi-diem 600000 --chi-phi-co-dinh 5tr --dt-moi-diem-truoc 8tr --tang-thu-nghiem 12% --bien-gop 35% --so-thang 3`
- Thưởng bậc: `python3 scripts/tinh_trade.py thuong-bac dai_ly.csv --bac "50tr=1%,100tr=2%,200tr=3%"` (thêm `--luy-tien` nếu thưởng từng phần).
- Mức tăng doanh số **chỉ lấy từ thử nghiệm có nhóm đối chứng**; chưa có → script chỉ ra mức tăng cần để hòa vốn.
- Doanh số tính thưởng = doanh số thuần (trừ hàng trả lại); kiểm trùng mã đại lý.
- Bậc thưởng gần nhau dễ làm đại lý dồn hàng cuối kỳ → ghi cảnh báo, đề xuất đo sell-out (bán ra) chứ không chỉ sell-in.

## 4. Đầu ra

1. Kết luận 1 câu: chương trình nên mở rộng/sửa/dừng; tổng chi thưởng.
2. Bảng chính sách/thể lệ/thưởng — "Đã kiểm tra phép tính".
3. Việc cần làm: thông báo đại lý, kiểm tra trưng bày (ảnh có ngày giờ), mốc đo.
4. Anh/chị tự làm: ký thỏa thuận đại lý, chi thưởng, xuất hóa đơn theo hướng dẫn kế toán.
5. "Hợp đồng đại lý và chính sách độc quyền vùng nên được luật sư xem."

## Không được làm

- Giả định mức tăng doanh số khi chưa thử nghiệm.
- Đề xuất ép đại lý không bán hàng đối thủ, ấn định giá bán lại bắt buộc — có thể vi phạm pháp luật cạnh tranh `[CẦN KIỂM TRA]`; chuyển luật sư.
- Chi thưởng, ký hợp đồng thay doanh nghiệp.
