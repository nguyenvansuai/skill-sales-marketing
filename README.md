# Skill AI Sales – Marketing cho doanh nghiệp Việt Nam (2026)

Bộ **17 skill** giúp Claude (và ChatGPT) làm việc như một phòng sales – marketing cho **doanh nghiệp, hộ kinh doanh Việt Nam**: bán **B2C và B2B**, **online lẫn offline** (sàn TMĐT, inbox, Zalo, website, đại lý, sales trực tiếp). Các skill tuân theo pháp luật hiện hành năm 2026:

- **Quảng cáo:** Luật Quảng cáo sửa đổi 75/2025/QH15, NĐ 342/2025/NĐ-CP.
- **Khuyến mại:** NĐ 81/2018/NĐ-CP sửa bởi NĐ 128/2024/NĐ-CP và NĐ 239/2026/NĐ-CP.
- **Thương mại điện tử:** Luật Thương mại điện tử 122/2025/QH15.
- **Dữ liệu cá nhân:** Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15, NĐ 356/2025/NĐ-CP.
- **Tin nhắn, cuộc gọi quảng cáo:** NĐ 91/2020/NĐ-CP.

Mọi skill dùng chung một bộ nguyên tắc:

- **Không bịa, không dùng benchmark không nguồn.** Thiếu số liệu thì hỏi, hoặc chạy kịch bản và ghi rõ giả định.
- **Tính toán bằng script**, không tính nhẩm.
- **Pháp lý có số hiệu, điều, khoản và nhãn tin cậy.**
- **AI chuẩn bị, con người quyết định.** Skill không đăng bài, không gửi tin, không bật quảng cáo, không ký hợp đồng thay người dùng.

> Biên soạn bởi **Sự AI** (suai.vn). Kế thừa có chọn lọc từ các bộ skill mã nguồn mở — xem [NOTICE.md](NOTICE.md).
> Muốn chuyên sâu kênh TikTok, livestream, sàn, Zalo cho agency: dùng thêm [agency-agents-vi](https://github.com/nguyenvansuai/agency-agents-vi).

## Danh sách skill

| Nhóm | Skill | Làm gì | Script |
|---|---|---|---|
| **Chiến lược** | `ho-so-doanh-nghiep` | Hồ sơ dùng chung: sản phẩm, giá vốn, khách, kênh, đối thủ, giọng thương hiệu. Mọi skill khác đọc file này trước | – |
| | `nghien-cuu-thi-truong` | Chân dung khách, đối thủ, định vị từ dữ liệu thật (inbox, đánh giá, đơn hàng) | – |
| | `gia-san-pham-khuyen-mai` | P&L từng đơn sau phí sàn, giá hòa vốn, ROAS/CPA hòa vốn, mức giảm tối đa còn lãi, giá đại lý theo bậc; kiểm khuyến mại hợp lệ (trần 50%, khuyến mại tập trung, thông báo/đăng ký) | `tinh_gia.py`, `kiem_khuyen_mai.py` |
| | `ke-hoach-ngan-sach-kpi` | Tính ngược từ doanh thu mục tiêu ra số đơn, lead, ngân sách theo kênh; 3 kịch bản; B2C, B2B, đại lý | `kpi_nguoc.py` |
| **Thương hiệu** | `thuong-hieu-noi-dung` | Giọng thương hiệu, lịch nội dung tháng, viết bài đa kênh | – |
| | `kiem-tra-phap-ly-quang-cao` | Soát quảng cáo, bài KOC, livestream, tin nhắn hàng loạt, form thu thông tin; kết luận "được đăng / sửa rồi đăng / cần xác nhận nội dung" | `validate_copy.py` + `rules_quangcao.py` |
| | `pr-su-kien-khung-hoang` | Thông cáo báo chí, kế hoạch sự kiện, xử lý khủng hoảng truyền thông | – |
| **Thu hút khách** | `quang-cao-truc-tuyen` | Meta, TikTok, Google: cấu trúc chiến dịch, mẫu quảng cáo, đọc số và phân loại theo hòa vốn | `doc_so_ads.py` |
| | `seo-website-landing` | SEO tiếng Việt, landing page, Google Business Profile | – |
| | `trade-marketing-diem-ban` | Đại lý, nhà phân phối, tạp hóa: trưng bày, thưởng bậc, đo ROI | `tinh_trade.py` |
| | `koc-affiliate-doi-tac` | Chọn KOC/affiliate, hợp đồng, nghĩa vụ công khai quảng cáo, số đơn hòa vốn | `tinh_koc.py` |
| **Bán hàng** | `quy-trinh-ban-hang-crm` | Pipeline B2C/B2B/đại lý, tiêu chí chuyển giai đoạn, chấm điểm lead, file CRM Excel có công thức, điểm xin đồng ý dữ liệu | `tao_pipeline.py` |
| | `tim-khach-b2b-bao-gia` | Chân dung khách lý tưởng, thư chào hàng, báo giá có VAT và hiệu lực, số tiền bằng chữ | `tao_bao_gia.py` |
| | `kich-ban-tu-van-chot-don` | Kịch bản inbox, gọi điện, gặp trực tiếp; xử lý từ chối; tài liệu đào tạo | – |
| | `quan-ly-doi-sales` | Chỉ tiêu, KPI hoạt động, hoa hồng theo bậc, dự báo doanh số từ pipeline | `hoa_hong_du_bao.py` |
| **Giữ khách & đo lường** | `cham-soc-giu-chan-khach` | Hành trình chăm sóc sau bán, khách thân thiết, phân nhóm RFM, tin nhắn đúng luật | `rfm.py` |
| | `bao-cao-doi-soat-hieu-qua` | Gộp sàn + quảng cáo + CRM + POS + sao kê → doanh thu thật, ROAS/CAC thật, lợi nhuận sau marketing; loại trùng, không ngoại suy | `doi_soat.py` |

Chuỗi dùng gợi ý: `ho-so-doanh-nghiep` → `gia-san-pham-khuyen-mai` → `ke-hoach-ngan-sach-kpi` → (nội dung, quảng cáo, KOC, trade) → `kiem-tra-phap-ly-quang-cao` trước khi đăng → `quy-trinh-ban-hang-crm` → `bao-cao-doi-soat-hieu-qua` cuối kỳ.

## Tải nhanh – không cần cài

| File | Dùng để |
|---|---|
| [`qua-tang/Pipeline_ban_hang_B2B.xlsx`](qua-tang/Pipeline_ban_hang_B2B.xlsx) | Quản lý cơ hội B2B: giai đoạn, giá trị trọng số, việc tiếp theo, đồng ý dữ liệu |
| [`qua-tang/Pipeline_ban_hang_B2C.xlsx`](qua-tang/Pipeline_ban_hang_B2C.xlsx) | Theo dõi khách inbox, Zalo, điện thoại đến khi chốt đơn |
| [`qua-tang/Quan_ly_dai_ly.xlsx`](qua-tang/Quan_ly_dai_ly.xlsx) | Phát triển và chăm sóc đại lý, điểm bán |
| [`van-ban/`](van-ban/) | Toàn văn 10 văn bản pháp luật gốc (bản chữ) để đối chiếu hoặc nạp vào Claude/ChatGPT Project |

## Cài đặt

### claude.ai (web, desktop, điện thoại)
1. Vào [`dist/`](dist/), tải `<ten-skill>.zip` (hoặc `tat-ca-skill.zip` rồi giải nén lấy từng thư mục).
2. Claude → **Customize → Skills → + Create skill → Upload a skill** → chọn file zip.
3. Chỉ cài skill thật sự cần; nên cài `ho-so-doanh-nghiep` trước.

### Claude Code
```
/plugin marketplace add nguyenvansuai/skill-sales-marketing
/plugin install tron-bo-skill-sales-marketing@skill-sales-marketing
```
Hoặc cài từng skill: `/plugin install gia-san-pham-khuyen-mai@skill-sales-marketing`.

### ChatGPT
Mở [`chatgpt/<ten-skill>.md`](chatgpt/) và làm theo hướng dẫn trong file: dán Instructions vào Project hoặc Custom GPT, tải các file `references/` (và `scripts/` nếu có) lên Knowledge.

## Câu lệnh mẫu

- "Lập hồ sơ doanh nghiệp cho shop mỹ phẩm của tôi, đây là bảng giá"
- "Serum giá 250k, giá vốn 110k, phí Shopee 8% + 3%, giảm 50% có lỗ không?"
- "Tháng 12 muốn 500 triệu doanh thu, cần bao nhiêu tiền quảng cáo?"
- "Kiểm tra bài quảng cáo này trước khi đăng"
- "Làm báo giá khóa đào tạo cho công ty ABC, có VAT"
- "Đối soát doanh thu tháng 10 từ file Shopee, file Ads và CRM"

## Cấu trúc repo

```
skills/<ten-skill>/SKILL.md · references/ · scripts/
shared/                 # nguyen-tac-chung.md, phap-ly-marketing-vn.md, scripts/vn_money.py — SỬA Ở ĐÂY
van-ban/                # toàn văn văn bản pháp luật (nguồn, ngày lấy)
qua-tang/               # file Excel dùng ngay
tests/du-lieu-mau/      # dữ liệu mẫu có lỗi cố ý để chạy thử script
docs/ke-hoach.md        # kế hoạch, bảng trường hợp
chatgpt/ dist/ .claude-plugin/marketplace.json   # sinh tự động
scripts/build.py        # đồng bộ shared → skills, sinh bản ChatGPT/zip/marketplace, kiểm lỗi
```

Sửa pháp lý hoặc nguyên tắc: sửa `shared/` → `python3 scripts/build.py` → commit ghi rõ thay đổi.

## Lưu ý pháp lý

- Đây là công cụ hỗ trợ, **không phải tư vấn pháp lý, thuế**. Nhãn `[NGUYÊN VĂN]` nghĩa là đã đối chiếu bản chữ trong `van-ban/` (lấy từ cổng tra cứu, chưa so Công báo); `[THỨ CẤP]` lấy từ bản tin công ty luật/kiểm toán; `[CẦN KIỂM TRA]` chưa xác minh.
- **NĐ 239/2026/NĐ-CP** (khuyến mại, hiệu lực 26/06/2026) chưa có toàn văn trong repo — đang dùng bản tin KPMG, PwC.
- Biểu phí sàn, chính sách quảng cáo nền tảng, mẫu Zalo ZNS thay đổi thường xuyên: skill luôn yêu cầu kiểm tra mới nhất và ghi ngày.
- Đối chiếu văn bản hiện hành và hỏi luật sư/cơ quan quản lý trước khi áp dụng.

## Giấy phép

MIT — xem [LICENSE](LICENSE). Giữ ghi công các dự án nguồn theo [NOTICE.md](NOTICE.md).
