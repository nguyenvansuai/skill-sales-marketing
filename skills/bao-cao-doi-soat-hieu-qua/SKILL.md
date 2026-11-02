---
name: bao-cao-doi-soat-hieu-qua
description: Đối soát và báo cáo hiệu quả marketing – bán hàng thật cho doanh nghiệp Việt Nam từ nhiều nguồn — báo cáo đơn sàn (Shopee, TikTok Shop, Lazada), CRM/inbox, POS cửa hàng, file chi phí quảng cáo (Meta, TikTok, Google), sao kê ngân hàng — loại đơn huỷ/hoàn, loại trùng đơn giữa các nguồn, không cộng tiền sàn chuyển về, so chuyển đổi nền tảng tự báo với đơn thật; ra doanh thu thật, ROAS thật, CAC, lợi nhuận sau marketing theo kênh và chiến dịch; B2B: giá trị pipeline, tỷ lệ thắng, chu kỳ bán; không ngoại suy dữ liệu thiếu. Dùng khi người dùng nói "báo cáo marketing tháng này", "đối soát doanh thu các kênh", "quảng cáo báo ROAS 5 mà không có lời", "kênh nào hiệu quả nhất", "chi phí mỗi khách mới bao nhiêu", "tổng kết chiến dịch", "báo cáo cho sếp".
---

# Báo cáo và đối soát hiệu quả

Đọc `references/nguyen-tac-chung.md`, `references/khung-doi-soat.md`.
Khác `ke-hoach-ngan-sach-kpi` (lập kế hoạch **trước** kỳ) và `quang-cao-truc-tuyen` (chẩn đoán bên trong nền tảng): skill này đo **kết quả thật sau kỳ**, đa kênh, theo tiền. Sổ doanh thu cho thuế hộ kinh doanh → bộ `skill-ho-kinh-doanh` (`doi-soat-doanh-thu`).

## 1. Xác định trường hợp (hỏi tối đa 2 câu: kỳ báo cáo, các kênh đang bán)

| # | Trường hợp | Chỉ số chính | Nguồn bắt buộc |
|---|---|---|---|
| A | Chỉ bán sàn | Doanh thu thật, lợi nhuận sau phí sàn và ads, ROAS thật | [Sàn] + [Ads] (ads trong sàn hoặc ngoài) |
| B | Online tự vận hành | Chi phí/lead, tỷ lệ chốt, CAC, lợi nhuận/đơn | [CRM] + [Ads] |
| C | Đa kênh | Đóng góp từng kênh sau loại trùng; doanh thu chưa gắn chiến dịch | Mọi nguồn đang có |
| D | B2B | Giá trị pipeline theo giai đoạn, tỷ lệ thắng, chu kỳ bán, CAC theo nguồn lead | File pipeline (`quy-trinh-ban-hang-crm`) + chi phí |
| E | Có cửa hàng/đại lý | Doanh thu POS/sell-in, chi phí trade | [POS] + chi phí trade |

## 2. Dữ liệu thật nằm ở đâu (hỏi đủ, thiếu một nguồn = sót)

| Mã | Nguồn | Trùng/loại cần xử lý |
|---|---|---|
| `[Sàn]` | File đơn hàng + đối soát sàn | Đơn huỷ/hoàn loại; phí sàn lấy từ đối soát |
| `[CRM]` | CRM, Pancake, file chốt đơn inbox | Đơn khách chốt inbox nhưng đặt trên sàn → không cộng lại; trùng SĐT |
| `[POS]` | Phần mềm bán hàng tại quầy | — |
| `[Ads]` | File xuất từ Trình quản lý quảng cáo | "Kết quả" nền tảng tự báo ≠ đơn thật |
| `[TK]` | Sao kê ngân hàng/ví | **Chỉ đối chiếu tiền về**, không cộng doanh thu (tiền sàn chuyển về đã nằm trong [Sàn]) |

## 3. Xử lý

- `python3 scripts/doi_soat.py --tu 01/10/2026 --den 31/10/2026 --san san.csv --crm crm.csv --ads ads.csv --tk saoke.csv --ty-le-gia-von 44% --chi-phi "KOC=15tr"`
- Tên cột từng file: xem docstring script; người dùng gửi file khác định dạng → đổi tên cột cho khớp, không đoán nghĩa cột.
- Gắn đơn về chiến dịch bằng tên chiến dịch trong đơn/CRM (quy ước đặt tên ở `quang-cao-truc-tuyen`); không gắn được → báo "doanh thu chưa gắn chiến dịch", không tự phân bổ.
- Thiếu nguồn, thiếu ngày → cảnh báo; **không ngoại suy** (1 tuần ≠ 1 tháng).
- Che SĐT còn 4 số cuối trước khi gửi file.

## 4. Đầu ra

1. Kết luận 1 câu: doanh thu thật, lợi nhuận sau marketing, chênh lệch so số nền tảng tự báo.
2. Bảng theo kênh, theo chiến dịch, lãi lỗ tổng — "Đã kiểm tra phép tính".
3. Danh sách đã xử lý trùng/loại và bảng "Cần anh/chị kiểm tra".
4. **3 việc cần làm** kỳ tới (dừng/giữ/tăng kênh, sửa cách ghi nguồn đơn) — mỗi việc dựa trên một con số trong báo cáo.
5. Anh/chị tự làm: xác nhận số, gửi báo cáo, cập nhật kế hoạch (`ke-hoach-ngan-sach-kpi`).

## Không được làm

- Cộng tiền sao kê vào doanh thu; cộng một đơn hai lần.
- Lấy số "chuyển đổi" của nền tảng làm doanh thu thật khi có dữ liệu đơn.
- Ngoại suy từ dữ liệu một phần; tự phân bổ doanh thu chưa gắn chiến dịch.
