# Kết quả mẫu – Sale 11.11 serum Lumi Glow trên Shopee

Con số chạy thật bằng công cụ `tinh_gia.py`, `kiem_khuyen_mai.py` (skill `gia-san-pham-khuyen-mai`) và `validate_copy.py` (skill `kiem-tra-phap-ly-quang-cao`) trên dữ liệu trong `dau-vao/`. Câu chữ AI trả lời mỗi lần có thể khác, **con số phải giống**.

## 1. Giảm 40% có lãi không? → **Lỗ 14.400đ mỗi đơn**

| Khoản (1 đơn) | Giá thường | Giảm 40% |
|---|---:|---:|
| Giá bán thực nhận | 450.000 | 270.000 |
| − Giá vốn | 135.000 | 135.000 |
| − Phí sàn % (cố định 10%, thanh toán 5%, Freeship Xtra 6%, Voucher Xtra 3%) | 108.000 | 64.800 |
| − Phí hạ tầng + đóng gói | 11.000 | 11.000 |
| − Chi phí hoàn kỳ vọng (8% × 45.000) | 3.600 | 3.600 |
| **= Lãi trước quảng cáo** | **192.400** | **55.600** |
| − Shopee Ads mỗi đơn mùa sale | 70.000 | 70.000 |
| **= Lợi nhuận sau quảng cáo** | **122.400** | **−14.400** |

Cách tính nhẩm hay gặp: "270.000 − 135.000 giá vốn = lãi 135.000" → bỏ sót **149.400đ** phí sàn, đóng gói, hoàn đơn và quảng cáo.

## 2. Giới hạn để còn lãi

| Chỉ số | Giá trị |
|---|---:|
| Mức giảm tối đa còn hòa vốn (đã tính 70.000đ quảng cáo) | **35,8%** |
| ROAS Shopee Ads hòa vốn ở giá sale 270.000 | **4,86** |
| Chi phí quảng cáo tối đa mỗi đơn ở giá sale (CPA hòa vốn) | 55.600 |
| ROAS hòa vốn ở giá thường 450.000 | 2,34 |

Đề xuất: **giảm 25%** (giá 337.500đ) → lãi 36.900đ/đơn (10,9%) sau quảng cáo; hoặc giữ 40% nhưng chỉ khi ROAS thực tế đạt từ 4,86 trở lên.

## 3. Chương trình có vi phạm quy định khuyến mại không?

- Giảm 40% ≤ trần 50% (khoản 1 Điều 4 TT 39/2025/TT-BCT) → **được**; không phải thông báo Sở Công Thương với hình thức giảm giá (NĐ 81/2018 sửa bởi NĐ 239/2026).
- **Banner ghi "Giá gốc 750.000đ" là sai**: giá thật đã bán ngay trước đó là 450.000đ. Nâng giá rồi gạch là thông tin gian dối về khuyến mại.
- **"GIẢM 40% DUY NHẤT HÔM NAY"** trong khi chạy 3 ngày 10–12/11 → thông tin sai về thời gian khuyến mại.

## 4. Soát tiêu đề, mô tả, banner

| Câu trong nội dung | Vấn đề | Nguồn phát hiện |
|---|---|---|
| "trị thâm nám tận gốc", "trị dứt điểm thâm nám, mụn" | Mỹ phẩm nói như thuốc điều trị (NĐ 342/2025) | Công cụ (SK001) |
| "an toàn tuyệt đối" (2 lần) | Cam kết tuyệt đối không chứng minh được | Công cụ (CK001) |
| "Serum số 1 Việt Nam" | Từ ngữ "số 1" phải có tài liệu chứng minh (Luật Quảng cáo) | Công cụ (LAW001) |
| "DUY NHẤT HÔM NAY" | Từ ngữ tuyệt đối, sai thời gian thật | Công cụ (LAW001) |
| "Trắng da sau 7 ngày", "không hiệu quả hoàn tiền 100%" | Cam kết công dụng, thời gian vượt công dụng đã công bố | Skill rà theo checklist |
| "được bác sĩ da liễu khuyên dùng" | Dùng danh nghĩa bác sĩ để quảng cáo mỹ phẩm (NĐ 342/2025) | Skill rà theo checklist |
| "Tốt hơn hẳn serum Hàn Quốc giá gấp đôi" | Quảng cáo so sánh không có tài liệu chứng minh | Skill rà theo checklist |
| "Giá gốc 750.000đ" | Giá gốc ảo | Skill rà theo checklist |
| (thiếu) | Chưa ghi tổ chức chịu trách nhiệm, số phiếu công bố | Skill rà theo checklist |

## 5. Nội dung viết lại (3 phương án, đúng luật)

**Tiêu đề Shopee:** Serum Vitamin C Lumi Glow 30ml – Dưỡng ẩm, hỗ trợ làm sáng da, giúp da đều màu

**Phương án A – nhấn công dụng:**
> Serum Vitamin C Lumi Glow giúp da ẩm mịn, hỗ trợ làm sáng và đều màu da khi dùng đều đặn sáng – tối. Kết cấu mỏng nhẹ, thấm nhanh, hợp da văn phòng. Đổi trả trong 7 ngày nếu sản phẩm lỗi hoặc không đúng mô tả.

**Phương án B – nhấn ưu đãi (dùng cho banner):**
> SALE 11.11 – Serum Lumi Glow giảm 25% từ 10/11 đến hết 12/11/2026: 450.000đ → 337.500đ. Số lượng có hạn.

**Phương án C – nhấn trải nghiệm:**
> Hơn 2.000 đánh giá trên Shopee [CẦN BỔ SUNG số thật]. Bạn thoa 2–3 giọt sau bước làm sạch, ban ngày dùng thêm kem chống nắng để bảo vệ da.

Chân mô tả bắt buộc thêm: *Sản phẩm là mỹ phẩm, không phải thuốc. Đơn vị chịu trách nhiệm: Công ty TNHH Mỹ phẩm Lumi, số phiếu công bố: [CẦN BỔ SUNG].*

## 6. Người vẫn phải tự làm

- Thay mức phí minh họa bằng biểu phí thật trong Kênh Người Bán tại thời điểm bán.
- Quyết định mức giảm, duyệt nội dung cuối, tự đăng lên Shopee.
- Kiểm tra số liệu đánh giá, số phiếu công bố trước khi đăng.
