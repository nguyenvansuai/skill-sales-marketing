---
name: gia-san-pham-khuyen-mai
description: Tính giá và thiết kế khuyến mại cho doanh nghiệp, hộ kinh doanh Việt Nam — P&L từng đơn sau phí sàn (Shopee, TikTok Shop, Lazada), phí ship, COD, hoàn đơn, chi phí quảng cáo; giá hòa vốn, ROAS và CPA hòa vốn, mức giảm tối đa còn lãi; giá đại lý theo bậc chiết khấu; kiểm khuyến mại theo NĐ 81/2018 sửa bởi NĐ 239/2026 và Thông tư 39/2025/TT-BCT (trần giảm 50%, khuyến mại tập trung, hàng cấm khuyến mại, khi nào phải thông báo/đăng ký). Dùng khi người dùng nói "bán giá này có lời không", "tính giá bán", "giảm 30% còn lãi không", "ROAS bao nhiêu thì hòa vốn", "phí sàn ăn hết lời", "làm chương trình khuyến mại", "giảm 70% được không", "chiết khấu đại lý bao nhiêu".
---

# Giá sản phẩm và khuyến mại

Đọc `references/nguyen-tac-chung.md`, `references/phap-ly-marketing-vn.md` (mục 3), `references/phi-kenh-ban.md`.
Khác `ke-hoach-ngan-sach-kpi`: skill này tính trên **một đơn / một sản phẩm**; skill kia tính trên **tổng doanh thu kỳ**. ROAS, CPA hòa vốn ở đây là đầu vào của skill kia và của `quang-cao-truc-tuyen`.

## 1. Xác định trường hợp (hỏi tối đa 2 câu nếu thiếu)

| # | Trường hợp | Việc phải làm | Căn cứ / nguồn số |
|---|---|---|---|
| A | Bán trên sàn | Giá vốn + từng loại phí sàn (hoa hồng, thanh toán, dịch vụ, voucher shop chịu, affiliate, trợ giá ship) + hoàn đơn → P&L/đơn, ROAS/CPA hòa vốn | Seller Center / file đối soát của shop, **ghi ngày kiểm** |
| B | Online tự vận hành (inbox, web, Zalo) | + phí ship shop chịu, phí COD, chi phí ads/đơn | Số liệu của doanh nghiệp |
| C | B2B / đại lý | Giá đại lý theo bậc chiết khấu trên giá bán lẻ khuyến nghị; cảnh báo bậc bán dưới giá vốn | `--bac-chiet-khau` |
| D | Dịch vụ | Giá gói = (chi phí nhân sự theo giờ × số giờ + chi phí khác) / (1 − biên mục tiêu) | Số liệu doanh nghiệp |
| E | Có khuyến mại | Kiểm hình thức, mức giảm/giá trị quà, mặt hàng cấm, thủ tục | NĐ 81/2018 (sửa 2024, 2026) — mục 3 |

## 2. Kiểm tra mới nhất (bắt buộc với phí sàn)

Có công cụ tìm kiếm → tìm "biểu phí người bán [sàn] [tháng/năm hiện tại]" trên trang chính thức của sàn → nếu khác số người dùng đưa thì hỏi lại; ghi nguồn + ngày. Ưu tiên **file đối soát thật** của shop hơn mọi bài viết. Không kiểm tra được → ghi "phí lấy theo số anh/chị cung cấp ngày …".

## 3. Xử lý

- P&L, hòa vốn, giảm giá, bậc chiết khấu:
  `python3 scripts/tinh_gia.py --gia-ban 250000 --gia-von 110000 --phi "hoa hồng=8%" --phi "thanh toán=3%" --phi "trợ giá ship=5000" --ty-le-hoan 4% --chi-phi-moi-don-hoan 35000 --ads-moi-don 20000 --loi-nhuan-muc-tieu 10% --giam 30% --ngay-kiem-phi 02/11/2026`
  Nhiều SKU: `python3 scripts/tinh_gia.py --csv san_pham.csv`
- Khuyến mại: `python3 scripts/kiem_khuyen_mai.py --hinh-thuc giam-gia --gia-truoc 300000 --gia-sau 120000 --mat-hang "kem chống nắng"`
- Quy tắc:
  - Mỗi loại phí là một biến có tên; **không gộp "phí sàn ~ X%"**, không dùng tỷ lệ phí trên mạng khi shop có file đối soát.
  - Voucher chồng nhau (shop + sàn + xu): cộng phần shop chịu vào phí rồi tính lại; biên âm → không đăng ký SKU đó.
  - Giá trước khuyến mại phải là giá thật đã bán; không nâng giá rồi gạch.
  - Thiếu giá vốn → dừng, hỏi; không ước tính.

## 4. Đầu ra

1. Kết luận 1 câu: lãi/lỗ mỗi đơn, ROAS hòa vốn, chương trình khuyến mại hợp lệ hay không.
2. Bảng P&L một đơn (và khi giảm giá); bảng giá đại lý nếu B2B — "Đã kiểm tra phép tính".
3. Việc cần làm: mức giảm đề xuất (≤ mức hòa vốn và ≤ trần pháp lý), thủ tục khuyến mại + căn cứ.
4. Anh/chị tự làm: cài giá/voucher trên sàn, thông báo/đăng ký khuyến mại nếu thuộc diện.
5. "Đối chiếu biểu phí hiện hành của sàn và văn bản khuyến mại hiện hành; hỏi Sở Công Thương với chương trình may rủi."

## Không được làm

- Ghi cứng tỷ lệ phí của bất kỳ sàn nào như sự thật.
- Đề xuất giảm giá > 50% ngoài khuyến mại tập trung/ngoại lệ; đề xuất giá gốc ảo.
- Cài giá, bật voucher, đăng ký chương trình thay người dùng.
