---
name: quy-trinh-ban-hang-crm
description: Thiết kế quy trình bán hàng và CRM cho doanh nghiệp Việt Nam — B2C chốt qua inbox Facebook/Zalo/điện thoại, B2B chu kỳ dài (lead → đánh giá → khảo sát/demo → báo giá → đàm phán → hợp đồng → thu tiền), phát triển đại lý/điểm bán — định nghĩa giai đoạn và tiêu chí chuyển, chấm điểm lead, quy tắc chia lead cho sales, thời gian phản hồi cam kết, chuyển giao marketing → sales, lý do thất bại; tạo file Excel pipeline có công thức thật khi chưa có CRM, hoặc map giai đoạn/trường dữ liệu vào CRM đang dùng (HubSpot, Getfly, Bitrix24, Base, Pancake, Zalo OA…); lưu bằng chứng đồng ý của khách theo Luật 91/2025. Dùng khi người dùng nói "xây quy trình bán hàng", "quản lý khách hàng tiềm năng", "làm CRM bằng Excel", "chia lead cho sales", "lead bị bỏ sót", "chấm điểm lead", "pipeline", "marketing đẩy lead sales không gọi".
---

# Quy trình bán hàng và CRM

Đọc `references/nguyen-tac-chung.md`, `references/khung-pipeline.md`.
Khác `quan-ly-doi-sales` (KPI, hoa hồng, dự báo theo người) và `kich-ban-tu-van-chot-don` (lời nói trong từng cuộc tư vấn): skill này thiết kế **dòng chảy khách hàng và công cụ ghi nhận**.

## 1. Xác định trường hợp (hỏi tối đa 2 câu: mô hình bán, đang dùng công cụ gì)

| # | Trường hợp | Giai đoạn pipeline | Đầu ra |
|---|---|---|---|
| A | B2C inbox, đơn nhỏ | Mới hỏi → Đang tư vấn → Đã báo giá → Chốt đơn → Đã giao / Thất bại | Quy trình + thời gian phản hồi cam kết + mẫu nhắc lại |
| B | B2B chu kỳ dài | Lead mới → Đủ chuẩn → Khảo sát/Demo → Báo giá → Đàm phán → Ký HĐ → Thắng / Thất bại | Tiêu chí chuyển + chấm điểm lead + SLA |
| C | Đại lý/điểm bán | Tiềm năng → Đã gặp → Đơn thử → Kích hoạt → Hoạt động / Ngưng | Quy trình phát triển + tuyến thăm |
| D | Chưa có CRM | Tạo file Excel có công thức | `pipeline_<mô hình>.xlsx` |
| E | Đã có CRM | Map giai đoạn, trường bắt buộc, tự động hóa nhắc việc | Bảng map + danh sách cấu hình (người dùng tự làm) |

## 2. Kiểm tra mới nhất

Tên tính năng, giới hạn gói miễn phí của CRM người dùng đang dùng → tra trang chính thức, ghi ngày. Không kiểm được → đưa bảng map chung, nói rõ "đối chiếu trong cài đặt của [CRM]".

## 3. Xử lý

- Tạo file: `python3 scripts/tao_pipeline.py --mo-hinh b2b --ra pipeline_b2b.xlsx --sales "An,Bình,Chi"`
- Mỗi giai đoạn phải có: **tiêu chí vào** (sự kiện kiểm chứng được, không phải cảm giác), việc phải làm, SLA (số ngày tối đa), xác suất.
- Xác suất trong file là mặc định để công thức chạy → ghi rõ, hướng dẫn thay bằng tỷ lệ thật sau 2–3 tháng.
- Chuyển giao marketing → sales: định nghĩa lead đủ chuẩn chung; marketing ghi nguồn + chiến dịch (đặt tên theo `quang-cao-truc-tuyen`) để `bao-cao-doi-soat-hieu-qua` đối soát.
- Dữ liệu khách: cột "Đồng ý nhận tin (ngày, kênh)"; form thu lead soát bằng `kiem-tra-phap-ly-quang-cao --doctype form`; không mua danh sách; file chia sẻ chỉ ghi 4 số cuối SĐT.
- Lý do thất bại theo danh mục cố định (giá, chưa có nhu cầu, chọn đối thủ, không liên lạc được, khác) để phân tích được.

## 4. Đầu ra

1. Kết luận 1 câu: quy trình mấy giai đoạn, điểm nghẽn lớn nhất hiện tại (nếu có số liệu).
2. Bảng giai đoạn (tiêu chí, việc, SLA, xác suất) + quy tắc chia lead + thời gian phản hồi.
3. File Excel hoặc bảng map CRM.
4. Anh/chị tự làm: cấu hình CRM, phổ biến cho đội, kiểm tra cập nhật hằng tuần.
5. "Thu thập và lưu dữ liệu khách theo Luật 91/2025, NĐ 356/2025 — chỉ định người phụ trách bảo vệ dữ liệu."

## Không được làm

- Đăng nhập CRM, sửa cấu hình, nhập dữ liệu khách thay người dùng.
- Đề xuất mua data, cào SĐT, nhắn tin cho người chưa đồng ý.
- Đặt xác suất "chuẩn ngành" như sự thật.

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **HubSpot CRM (ChatGPT chưa có connector này)** · **Notion** · **Google Drive**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Đọc cấu hình pipeline hiện có trong HubSpot (giai đoạn, thuộc tính) để đề xuất quy trình sát thực tế.
2. Báo cáo deal tồn đọng, deal không có hoạt động tiếp theo; cập nhật giai đoạn deal chỉ sau khi xác nhận.
3. Không dùng HubSpot: dựng CRM đơn giản bằng cơ sở dữ liệu Notion hoặc Sheets trên Drive.

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
