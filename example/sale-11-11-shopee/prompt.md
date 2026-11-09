# Prompt – Sale 11.11 trên Shopee

## Chuẩn bị (trước giờ dạy)

1. Cài bộ skill Sales – Marketing (trọn bộ, hoặc tối thiểu 2 skill `gia-san-pham-khuyen-mai`, `kiem-tra-phap-ly-quang-cao`).
2. Bật **Code execution** (claude.ai: Settings → Capabilities; ChatGPT: Code Interpreter).
3. Mở cuộc trò chuyện mới, **đính kèm 3 file trong `dau-vao/`**: `ho-so-shop.md`, `bang-phi-shopee.xlsx`, `noi-dung-quang-cao.txt`.

## Prompt demo (chép nguyên văn)

```
Shop tôi bán serum trên Shopee (hồ sơ shop và bảng phí đính kèm).
Sếp muốn giảm 40% dịp 11.11, từ 10/11 đến 12/11/2026. Hãy:
1. Tính mỗi đơn lãi hay lỗ bao nhiêu sau toàn bộ phí sàn, đóng gói, hoàn đơn và quảng cáo.
2. Giảm tối đa bao nhiêu % thì vẫn có lãi? ROAS Shopee Ads bao nhiêu thì hòa vốn?
3. Chương trình có vi phạm quy định khuyến mại không?
4. Soát tiêu đề, mô tả, banner trong file noi-dung-quang-cao.txt, chỉ ra câu vi phạm
   và viết lại bản đúng luật mà vẫn hấp dẫn.
```

Kết quả đúng: xem `ket-qua-mau/ket-qua.md` – **giảm 40% lỗ 14.400đ/đơn**, giảm tối đa 35,8% để hòa vốn, ROAS hòa vốn 4,86; banner "giá gốc 750.000đ" và "duy nhất hôm nay" sai; ít nhất 8 câu vi phạm trong nội dung.

## Prompt hỏi tiếp (nếu còn thời gian)

```
Nếu giảm 25% thì lãi bao nhiêu mỗi đơn? Cần bán bao nhiêu đơn trong 3 ngày để lãi 20 triệu?
```

```
Thay vì giảm giá, đề xuất 2 phương án khuyến mại khác (tặng quà, combo) và kiểm tra hạn mức theo luật.
```

## Prompt đầy đủ khi đã kết nối connector (chỉ giảng trên slide, không demo)

```
Lấy giá vốn và tỷ lệ hoàn đơn 3 tháng gần nhất của serum Lumi Glow trong Shopify / file đối soát trên Drive,
tính phương án giảm giá 11.11, soát nội dung quảng cáo,
rồi làm banner 1200x1200 trên Canva bằng câu chữ đã duyệt.
```

Lý do không demo phần connector: Shopee chưa có connector chính thức (phải tải file báo cáo), Canva cần đăng nhập tài khoản thiết kế – dễ trục trặc trên lớp. Đặt sẵn file trong `dau-vao/` cho kết quả ổn định.
