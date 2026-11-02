---
name: kiem-tra-phap-ly-quang-cao
description: Soát nội dung quảng cáo, bài đăng, kịch bản KOL/KOC, livestream, tin nhắn hàng loạt, form thu thông tin khách theo luật Việt Nam hiện hành — từ ngữ tuyệt đối "nhất, số 1, duy nhất" thiếu bằng chứng (khoản 11 Điều 8 Luật Quảng cáo), so sánh với đối thủ (khoản 10, sửa 2025), người có ảnh hưởng phải ghi rõ là quảng cáo (Luật 75/2025), mỹ phẩm và thực phẩm nói như thuốc, thông tin bắt buộc cho thực phẩm bảo vệ sức khỏe (NĐ 342/2025), giảm giá quá 50% (NĐ 81/2018 sửa 2024, 2026), xin đồng ý dữ liệu cá nhân (Luật 91/2025), tin nhắn rác (NĐ 91/2020). Chạy công cụ soát tự động, ra bảng lỗi kèm căn cứ và cách sửa, kết luận được đăng / sửa rồi đăng / cần xin xác nhận nội dung. Dùng khi người dùng nói "kiểm tra bài quảng cáo này", "content này có vi phạm không", "soát kịch bản KOC", "được ghi tốt nhất không", "quảng cáo thực phẩm chức năng cần ghi gì", "form này có đúng luật dữ liệu cá nhân không".
---

# Kiểm tra pháp lý quảng cáo

Đọc `references/nguyen-tac-chung.md`, `references/phap-ly-marketing-vn.md`, `references/checklist-duyet.md`.
Khác `thuong-hieu-noi-dung`, `quang-cao-truc-tuyen`: skill này **không viết nội dung mới**, chỉ soát và đề xuất câu thay thế. Các skill viết nội dung gọi skill này trước khi giao.

## 1. Xác định trường hợp (hỏi tối đa 2 câu: loại sản phẩm, kênh)

| # | Trường hợp | `--doctype` | Kiểm thêm | Căn cứ |
|---|---|---|---|---|
| A | Nội dung thường (bài, banner, landing) | (không) | Tuyệt đối hóa, so sánh, cam kết 100%, giảm > 50%, từ như thuốc (mức cảnh báo) | Đ8 k10, k11 Luật QC; Đ7 NĐ 81/2018 |
| B | Mỹ phẩm | `my-pham` | Từ như thuốc (lỗi); hình ảnh bác sĩ/cơ sở y tế; thông tin tổ chức chịu trách nhiệm | NĐ 342/2025 Đ4 |
| C | Thực phẩm bảo vệ sức khỏe | `tpbvsk` | Cụm "Thực phẩm bảo vệ sức khỏe" + câu khuyến cáo bắt buộc | NĐ 342/2025 Đ5 |
| D | Thực phẩm bổ sung / thực phẩm | `thuc-pham-bo-sung` / `thuc-pham` | Cụm từ bắt buộc; tổ chức chịu trách nhiệm | NĐ 342/2025 Đ5 |
| E | Bài/kịch bản KOL, KOC, được tài trợ | `kol` | Có dấu hiệu "Quảng cáo/Hợp tác/#quangcao"; không tự nhận "không phải quảng cáo" | Đ15a, Đ23 k2 Luật QC (sửa 2025) |
| F | Form, landing thu SĐT/email | `form` | Ô đồng ý không tick sẵn; có câu đồng ý; mục đích; chính sách bảo mật | Luật 91/2025, NĐ 356/2025 |
| G | SMS, email, tin Zalo gửi hàng loạt | `bulk-message` | Cách từ chối nhận; nhắc khung giờ, tần suất | NĐ 91/2020 Đ11, Đ13 |
| H | Livestream bán hàng | `kol` + checklist mục livestream | Giấy tờ người bán, nội dung khớp bản đã xác nhận | Luật TMĐT 122/2025 Đ23, Đ24 |
| I | Sản phẩm thuộc nhóm đặc biệt khác (thiết bị y tế, thuốc, sữa trẻ nhỏ, đồ uống có cồn, phân bón…) | (không) + checklist | Hỏi văn bản xác nhận nội dung quảng cáo | NĐ 342/2025 Đ3; `[CẦN KIỂM TRA]` thủ tục |

## 2. Kiểm tra mới nhất

Văn bản quảng cáo vừa thay đổi lớn (Luật 75/2025 từ 01/01/2026, NĐ 342/2025 từ 15/02/2026). Có công cụ tìm kiếm → tìm "Luật Quảng cáo nghị định hướng dẫn [tháng/năm hiện tại]" trên vbpl.vn, thuvienphapluat.vn; có văn bản mới hơn ngày tổng hợp 02/11/2026 → báo người dùng, ghi nguồn + ngày. Không kiểm tra được → "căn cứ tổng hợp ngày 02/11/2026".

## 3. Xử lý

- Lưu nội dung người dùng gửi vào file `.md` rồi chạy:
  `python3 scripts/validate_copy.py noi-dung.md --doctype tpbvsk`
  (`--list-rules` xem mọi quy tắc; `--json` để lấy kết quả dạng máy đọc).
- Có tài liệu chứng minh cho "số 1"/so sánh → người dùng ghi `<!-- proof: tên tài liệu, số, ngày -->` cùng dòng; khuyến mại tập trung → `<!-- khuyen-mai-tap-trung: tên chương trình -->`.
- Phần máy không kiểm được (hình ảnh, lời nói trong video, KOC đã dùng sản phẩm chưa, giá trước khuyến mại có thật không) → đi qua `references/checklist-duyet.md` bằng tay, hỏi người dùng.
- Mỗi lỗi: đề xuất **câu thay thế cụ thể**, không chỉ nói "sai".

## 4. Đầu ra

1. Kết luận 1 trong 3: **Được đăng** / **Sửa rồi đăng** / **Cần xin xác nhận nội dung trước** (+ lý do 1 câu).
2. Bảng lỗi: dòng · mức (lỗi/cảnh báo) · mã quy tắc · trích đoạn · căn cứ · câu thay thế.
3. Bản nội dung đã sửa (giữ giọng thương hiệu).
4. Checklist phần không tự động kiểm được, đánh dấu đã/ chưa.
5. Anh/chị tự làm: lưu bằng chứng cho mọi tuyên bố; xin xác nhận nội dung nếu thuộc diện; lưu bằng chứng đồng ý của khách.
6. "Đây là công cụ soát câu chữ, không phải tư vấn pháp lý. Đối chiếu văn bản hiện hành và hỏi luật sư/cơ quan quản lý với sản phẩm thuộc nhóm đặc biệt."

## Không được làm

- Kết luận "hợp pháp 100%", "không thể bị phạt".
- Gợi ý lách luật (viết tắt, đọc lái, dùng ký hiệu thay từ "nhất", "KOC nói như không phải quảng cáo").
- Nêu mức phạt cụ thể khi chưa đối chiếu nghị định xử phạt.
