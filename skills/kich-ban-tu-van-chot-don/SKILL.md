---
name: kich-ban-tu-van-chot-don
description: Viết kịch bản tư vấn và chốt đơn cho đội bán hàng Việt Nam — trả lời inbox Facebook/Zalo/TikTok, gọi điện tư vấn (telesale cho khách đã để lại thông tin), tư vấn tại cửa hàng, demo B2B; câu mở đầu, câu hỏi khai thác nhu cầu, giới thiệu theo lợi ích, xử lý từ chối ("đắt quá", "để suy nghĩ", "bên kia rẻ hơn", "hỏi chồng/vợ đã", "sợ không hợp"), chốt đơn, bán thêm, theo dõi khách im lặng; bộ câu trả lời mẫu cho chatbot/nhân viên; tài liệu đào tạo sales mới và chấm điểm cuộc tư vấn từ bản ghi chat. Không hứa hẹn sai sự thật, không gây áp lực giả. Dùng khi người dùng nói "viết kịch bản chốt sale", "khách chê đắt trả lời sao", "kịch bản trả lời inbox", "khách seen không rep", "đào tạo nhân viên tư vấn", "chấm điểm đoạn chat này", "kịch bản telesale".
---

# Kịch bản tư vấn và chốt đơn

Đọc `references/nguyen-tac-chung.md`, `references/khung-tu-van.md`.
Khác `quy-trinh-ban-hang-crm` (giai đoạn, công cụ) và `tim-khach-b2b-bao-gia` (tiếp cận khách chưa quen): skill này lo **lời nói trong cuộc tư vấn** khi khách đã có quan tâm.

## 1. Xác định trường hợp (hỏi tối đa 2 câu: kênh, sản phẩm/giá)

| # | Trường hợp | Việc phải làm | Đầu ra |
|---|---|---|---|
| A | Inbox (Facebook, Zalo, TikTok) | Câu chào theo nguồn quảng cáo → 2–3 câu hỏi nhu cầu → tư vấn → chốt → xác nhận đơn | Kịch bản theo nhánh + câu trả lời mẫu |
| B | Gọi điện cho khách đã để lại thông tin | Mở đầu 15 giây, xác nhận khách có đăng ký, khai thác, hẹn/chốt | Kịch bản gọi + xử lý từ chối |
| C | Tại cửa hàng / demo B2B | Chào, hỏi, cho trải nghiệm, so sánh lựa chọn, chốt | Kịch bản + checklist demo |
| D | Xử lý từ chối | Từng câu từ chối thật của khách (từ dữ liệu chat) → nhận diện lo ngại thật → trả lời | Bảng từ chối – lo ngại – trả lời |
| E | Đào tạo / chấm điểm | Chấm bản ghi chat theo thang 5 tiêu chí, chỉ ra câu cần sửa | Phiếu chấm + câu thay thế |

## 2. Kiểm tra mới nhất

Chính sách giá, khuyến mại, tồn kho, phí ship đang áp dụng → lấy từ hồ sơ doanh nghiệp hoặc người dùng xác nhận **ngày hiện tại**; khuyến mại phải đúng thể lệ đã công bố.

## 3. Xử lý

- Dùng từ ngữ của khách (từ `nghien-cuu-thi-truong` hoặc bản ghi chat người dùng đưa).
- Mỗi lợi ích nói trong kịch bản phải có trong hồ sơ/tài liệu sản phẩm; không tự thêm công dụng.
- Xử lý từ chối theo 4 bước: ghi nhận → hỏi lại để hiểu lo ngại thật → trả lời bằng bằng chứng/lựa chọn phù hợp → đề nghị bước tiếp.
- Khan hiếm, hạn chót chỉ dùng khi **có thật** (số lượng thật, hạn khuyến mại thật).
- Gửi tin chăm sóc sau đó chỉ cho khách đã đồng ý nhận tin (`cham-soc-giu-chan-khach`).
- Mỹ phẩm, thực phẩm chức năng: kịch bản qua soát `kiem-tra-phap-ly-quang-cao` (không tư vấn như thuốc).

## 4. Đầu ra

1. Kết luận 1 câu: điểm mấu chốt để tăng tỷ lệ chốt (nếu có dữ liệu chat).
2. Kịch bản theo nhánh (bảng: tình huống – câu nói – mục đích) / bảng xử lý từ chối / phiếu chấm.
3. Bộ câu trả lời mẫu ngắn (dán vào tin nhắn nhanh, chatbot).
4. Anh/chị tự làm: duyệt, huấn luyện đội, cài tin nhắn nhanh.
5. Chỉ số theo dõi: tỷ lệ trả lời trong SLA, tỷ lệ chốt theo nhân viên (đo bằng `quan-ly-doi-sales`).

## Không được làm

- Viết câu nói sai sự thật: "chỉ còn 2 suất" khi không đúng, "giá này hôm nay thôi" khi không có hạn.
- Tư vấn sức khỏe như bác sĩ; hứa kết quả 100%.
- Kịch bản nói xấu đối thủ nêu tên; ép khách, gọi dồn dập (NĐ 91/2020: ≤ 1 cuộc gọi quảng cáo/24 giờ trừ khi khách thỏa thuận khác).

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **Google Drive** · **Notion** · **Gmail**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Đọc tin nhắn, email khách hỏi thường gặp (file xuất, hộp thư) để viết kịch bản sát câu hỏi thật.
2. Lưu bộ kịch bản vào Notion hoặc Docs trên Drive cho cả đội dùng chung.

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
