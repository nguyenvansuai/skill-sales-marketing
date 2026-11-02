# Kế hoạch bộ skill Sales – Marketing cho thị trường Việt Nam

> Repo: github.com/nguyenvansuai/skill-sales-marketing
> Ngày tổng hợp: 02/11/2026 · Trạng thái: đã làm xong cả 17 skill (một đợt, theo yêu cầu 02/11/2026). Pháp lý cập nhật ở `shared/phap-ly-marketing-vn.md` — ưu tiên file đó nếu khác bảng dưới.
> Người dùng cuối: doanh nghiệp/hộ kinh doanh bán **B2C và B2B**, online lẫn offline.
> Khác `agency-agents-vi`: repo đó chuyên sâu kênh online cho agency (TikTok, sàn, livestream, ads, Zalo); repo này phủ toàn bộ marketing–sales ở mức doanh nghiệp.

---

## 1. Danh sách skill

Nguồn (đều MIT, trừ K là Apache 2.0): **C** coreyhaines31/marketingskills · **M** minhnv0807/ai-business-skills · **T** trussary/vietnamese-language-skill · **K** anthropics/knowledge-work-plugins (sales)

| # | Skill | Nhóm | Nguồn | Script | Đợt |
|---|---|---|---|---|---|
| 1 | `ho-so-doanh-nghiep` | Chiến lược | modify C + M | – | **1** |
| 2 | `nghien-cuu-thi-truong` | Chiến lược | modify C + M | – | 2 |
| 3 | `gia-san-pham-khuyen-mai` | Chiến lược | modify C + M | ✅ | **1** |
| 4 | `ke-hoach-ngan-sach-kpi` | Chiến lược | modify M | ✅ | **1** |
| 5 | `thuong-hieu-noi-dung` | Thương hiệu | modify C + M | – | 2 |
| 6 | `kiem-tra-phap-ly-quang-cao` | Thương hiệu | **fork validator T** | ✅ | **1** |
| 7 | `pr-su-kien-khung-hoang` | Thương hiệu | modify C + M | – | 2 |
| 8 | `quang-cao-truc-tuyen` | Thu hút khách | modify C + M | ✅ | 2 |
| 9 | `seo-website-landing` | Thu hút khách | modify C | – | 2 |
| 10 | `trade-marketing-diem-ban` | Thu hút khách | **viết mới** | ✅ | 2 |
| 11 | `koc-affiliate-doi-tac` | Thu hút khách | modify C + M | ✅ | 2 |
| 12 | `quy-trinh-ban-hang-crm` | Bán hàng | modify C + K | ✅ | **1** |
| 13 | `tim-khach-b2b-bao-gia` | Bán hàng | modify C + T + K | ✅ | 2 |
| 14 | `kich-ban-tu-van-chot-don` | Bán hàng | modify C + K | – | 2 |
| 15 | `quan-ly-doi-sales` | Bán hàng | modify K | ✅ | 2 |
| 16 | `cham-soc-giu-chan-khach` | Giữ khách | modify C + T | – | 2 |
| 17 | `bao-cao-doi-soat-hieu-qua` | Đo lường | modify M + **script mới** | ✅ | **1** |

Chuỗi dữ liệu: `1` → mọi skill đọc trước · `3` → `4`, `8`, `10` · `12` → `15`, `17` · `6` được gọi bởi `5`, `8`, `11`, `16` trước khi đăng/gửi.

---

## 2. Biến quyết định chung (lưu trong hồ sơ doanh nghiệp, skill khác đọc lại)

| Biến | Giá trị | Ảnh hưởng |
|---|---|---|
| Mô hình | B2C / B2B / cả hai | Phễu KPI, quy trình bán, kịch bản |
| Kênh bán | Sàn TMĐT · online tự vận hành (web, inbox, Zalo) · điểm bán/đại lý · sales trực tiếp | Cách tính giá, đối soát, nguồn dữ liệu |
| Ngành đặc biệt | Có/không thuộc danh mục sản phẩm đặc biệt (NĐ 342/2025: 11 nhóm, gồm mỹ phẩm, thực phẩm…) `[cần lấy danh mục nguyên văn]` | Bật quy tắc quảng cáo riêng ở skill 6 |
| Pháp nhân | Hộ kinh doanh / doanh nghiệp | Hóa đơn, VAT trong báo giá, thủ tục khuyến mại |
| Quy mô đội | Chủ tự làm / có đội sales–marketing | Mức chi tiết quy trình, KPI cá nhân |

---

## 3. Bảng trường hợp — Đợt 1 (chi tiết)

### Skill 1 · `ho-so-doanh-nghiep`
Khác các skill còn lại: chỉ thu thập và lưu context, không đưa ra kế hoạch.

| TH | Việc | Đầu ra |
|---|---|---|
| Chưa có hồ sơ | Hỏi bộ trường cố định, chia ≤ 2 lượt | `.agents/ho-so-doanh-nghiep.md` |
| Có tài liệu (web, catalogue, bảng giá) | Trích tự động, trường thiếu ghi `[?]`, chỉ hỏi phần thiếu | Như trên |
| Đã có hồ sơ | Đọc, hỏi trường hay đổi (giá, kênh, mục tiêu) | Bản cập nhật + ngày cập nhật |

Trường bắt buộc: ngành · sản phẩm/dịch vụ chủ lực · giá bán & giá vốn · mô hình · kênh · khách hàng mục tiêu · đối thủ chính · pháp nhân · ngành đặc biệt? · giọng thương hiệu · chính sách đổi trả/bảo hành · mục tiêu doanh thu.
Không được: lưu CCCD, số tài khoản, mật khẩu.

### Skill 3 · `gia-san-pham-khuyen-mai`
Khác skill 4: tính trên **từng đơn/sản phẩm**; skill 4 tính trên tổng doanh thu kỳ.

| TH | Việc phải làm | Đầu ra | Căn cứ |
|---|---|---|---|
| A. Bán trên sàn | Giá vốn + phí sàn (cố định, thanh toán, dịch vụ, voucher, affiliate) → giá hòa vốn, biên lợi nhuận | Bảng P&L/đơn | Biểu phí sàn hiện hành, ghi ngày kiểm |
| B. Online tự vận hành | + phí ship, COD, chi phí quảng cáo/đơn | Bảng P&L/đơn | Số liệu của doanh nghiệp |
| C. B2B / đại lý | Bậc chiết khấu, giá đại lý vs giá bán lẻ khuyến nghị, công nợ | Bảng giá theo bậc | – |
| D. Dịch vụ | Giá theo gói/giờ, chi phí nhân sự | Bảng giá gói | – |
| E. Có chương trình khuyến mại | Kiểm mức giảm tối đa, hàng cấm khuyến mại, thủ tục thông báo/đăng ký | Mức giảm còn lãi + thủ tục + hạn | Luật TM 2005; NĐ 81/2018 sửa bởi NĐ 128/2024 và NĐ 239/2026 |

Script: `tinh_gia.py` (P&L/đơn, hòa vốn, giá sau giảm), `kiem_khuyen_mai.py` (hình thức → mức tối đa → thủ tục).
Không được: dùng tỷ lệ phí sàn ghi cứng không có ngày kiểm.

### Skill 4 · `ke-hoach-ngan-sach-kpi`
Khác skill 8: phân bổ ngân sách giữa các kênh; skill 8 lo chi tiết trong từng kênh quảng cáo.

| TH | Phễu tính ngược | Đầu ra |
|---|---|---|
| B2C online | Doanh thu → số đơn → tin nhắn/lượt truy cập → chi phí quảng cáo | Phễu + ngân sách theo kênh |
| B2B | Doanh thu → hợp đồng → cơ hội → lead → hoạt động sales/tuần | Phễu + chỉ tiêu hoạt động |
| Đại lý/điểm bán | Doanh thu → sell-in/sell-out → số điểm bán, độ phủ, chương trình trade | Phễu + ngân sách trade |
| Kỳ có mùa vụ (Tết, ngày đôi…) | Tách kỳ cao điểm | Lịch theo tháng |

Quy tắc: tỷ lệ chuyển đổi lấy từ số liệu thật của doanh nghiệp. Thiếu số liệu → hỏi, hoặc chạy 3 kịch bản và ghi rõ giả định. **Không dùng benchmark không có nguồn.**
Script: `kpi_nguoc.py`.

### Skill 6 · `kiem-tra-phap-ly-quang-cao`
Khác skill 5: không viết nội dung, chỉ soát và đề xuất sửa.

| TH | Việc | Căn cứ |
|---|---|---|
| Nội dung thường | Soát tuyệt đối hóa ("số 1", "tốt nhất") khi thiếu bằng chứng, so sánh trực tiếp, sai sự thật | Luật QC 2012 sửa bởi Luật 75/2025 `[đối chiếu điều, khoản]` |
| Sản phẩm đặc biệt | Áp yêu cầu nội dung riêng của nhóm; kiểm diện phải có xác nhận nội dung trước khi quảng cáo | NĐ 342/2025 |
| KOC/người có ảnh hưởng quảng cáo | Nghĩa vụ của người chuyển tải sản phẩm quảng cáo (thông báo là quảng cáo…) | Luật 75/2025 `[đối chiếu]` |
| Nội dung khuyến mại | Mức giảm, thể lệ → chuyển sang skill 3 | NĐ 81/2018 (đã sửa) |
| Tin nhắn, email, cuộc gọi quảng cáo | Đồng ý trước, khung giờ, tần suất, cách từ chối | NĐ 91/2020; TT 22/2021 |
| Có thu thập dữ liệu khách hàng | Câu xin đồng ý, mục đích xử lý | Luật 91/2025; NĐ 356/2025 |
| Bán qua sàn/website/livestream | Nghĩa vụ thông tin người bán, livestream | Luật TMĐT 122/2025 `[đối chiếu]` |

Đầu ra: bảng lỗi (dòng · mức · quy tắc · căn cứ · cách sửa) + kết luận 1 trong 3: **được đăng / sửa rồi đăng / cần xin xác nhận nội dung**.
Script: fork `validate_copy.py` của T, thêm bộ quy tắc từ văn bản mới.
Không được: kết luận "hợp pháp 100%"; luôn kèm câu chốt "đối chiếu quy định hiện hành".

### Skill 12 · `quy-trinh-ban-hang-crm`
Khác skill 15: thiết kế quy trình và công cụ; skill 15 quản lý con người (KPI, hoa hồng).

| TH | Giai đoạn pipeline | Đầu ra |
|---|---|---|
| B2C inbox, đơn nhỏ | Hỏi → tư vấn → chốt → giao → sau bán | Quy trình + thời gian phản hồi |
| B2B chu kỳ dài | Lead → đánh giá → khảo sát/demo → báo giá → đàm phán → hợp đồng → thanh toán | Tiêu chí chuyển giai đoạn + chấm điểm lead |
| Kênh đại lý | Tuyển → kích hoạt → đặt hàng lại → chăm sóc | Quy trình phát triển đại lý |
| Chưa có CRM | Tạo mẫu Google Sheet/Excel | File có công thức thật |
| Đã có CRM (HubSpot, Getfly, Bitrix, Base…) | Map giai đoạn và trường dữ liệu | Bảng map |

Bắt buộc có: điểm xin đồng ý xử lý dữ liệu khi thu SĐT/email (Luật 91/2025).
Script: `tao_pipeline.py` → xlsx.

### Skill 17 · `bao-cao-doi-soat-hieu-qua`
Khác skill 4: đo kết quả thật sau kỳ; skill 4 lập kế hoạch trước kỳ.

| Nguồn dữ liệu | Mã | Trùng/loại cần xử lý |
|---|---|---|
| Báo cáo sàn (đơn, phí, hoàn) | `[Sàn]` | Đơn hủy/hoàn loại |
| Nền tảng quảng cáo (chi phí, chuyển đổi tự báo) | `[Ads]` | Chuyển đổi do nền tảng tự báo ≠ đơn thật; đơn ads dẫn về sàn chỉ đếm 1 lần |
| CRM/inbox (lead, đơn chốt) | `[CRM]` | Lead trùng SĐT |
| Sao kê/kế toán (tiền về) | `[TK]` | Tiền sàn chuyển về đã nằm trong `[Sàn]` |
| POS/đại lý | `[POS]` | – |

| TH | Chỉ số chính |
|---|---|
| Chỉ bán sàn | Doanh thu thực, lợi nhuận sau phí, ROAS theo đơn thật |
| Online tự vận hành | CPL, tỷ lệ chốt, CAC, lợi nhuận/đơn |
| Đa kênh | Đóng góp từng kênh sau loại trùng |
| B2B | Giá trị pipeline, tỷ lệ thắng, chu kỳ bán |

Đầu ra: kết luận 1 câu → bảng → "Đã kiểm tra phép tính" → chênh lệch giữa số nền tảng tự báo và số thật → 3 việc cần làm.
Script: `doi_soat.py` (đọc CSV/XLSX export).
Không được: ngoại suy từ dữ liệu một phần (vd. 1 tuần → cả tháng).

---

## 4. Bảng trường hợp — Đợt 2 (rút gọn, chi tiết hóa khi vào đợt)

| # | Biến quyết định | Trường hợp chính | Đầu ra | Căn cứ/nguồn cần |
|---|---|---|---|---|
| 2 | Mô hình, có dữ liệu khách hay chưa | Khách cá nhân / doanh nghiệp; có khảo sát / chỉ có đối thủ | Chân dung khách, bản đồ đối thủ, định vị | Dữ liệu thật của DN |
| 5 | Kênh, mục tiêu nội dung | Fanpage/TikTok/Zalo/web/email; nhận biết / chuyển đổi | Giọng thương hiệu, lịch tháng, bài viết | Gọi skill 6 trước khi giao |
| 7 | Loại sự việc | Thông cáo báo chí / sự kiện / khủng hoảng truyền thông | Thông cáo, kịch bản sự kiện, quy trình xử lý 24h | Luật Báo chí `[cần kiểm tra]` |
| 8 | Nền tảng, mục tiêu, ngân sách | Meta / TikTok / Google; lead / đơn / tin nhắn | Cấu trúc chiến dịch, đọc số, chẩn đoán | Chính sách quảng cáo nền tảng, ghi ngày kiểm |
| 9 | Có website hay chưa | Web mới / web cũ / chỉ landing | Kiểm SEO, cấu trúc trang, landing | – |
| 10 | Kênh truyền thống | Đại lý / nhà phân phối / tạp hóa / siêu thị | Chương trình trưng bày, chiết khấu, đo sell-out | Luật TM về khuyến mại giữa thương nhân |
| 11 | Loại đối tác | KOC/KOL / affiliate / đối tác chéo | Tiêu chí chọn, hợp đồng, tính phí | Luật 75/2025 (người chuyển tải QC); thuế TNCN khấu trừ — dùng lại `shared/` từ skill-ho-kinh-doanh |
| 13 | Kênh tiếp cận | Email / Zalo / gọi điện / LinkedIn | Danh sách khách tiềm năng, thư chào, báo giá có VAT | NĐ 91/2020; quy định hóa đơn, VAT `[cần kiểm tra]` |
| 14 | Kênh tư vấn | Inbox / điện thoại / trực tiếp | Kịch bản, xử lý từ chối, tài liệu đào tạo | – |
| 15 | Quy mô đội | 1–3 người / có trưởng nhóm | KPI, cơ chế hoa hồng, dự báo doanh số | Bộ luật Lao động (lương, thưởng) `[cần kiểm tra]` |
| 16 | Kênh chăm sóc | Zalo OA/ZNS / email / SMS / gọi | Hành trình chăm sóc, chương trình khách thân thiết | NĐ 91/2020; Luật 91/2025; quy định mẫu ZNS (ghi ngày kiểm) |

---

## 5. Nguồn sự thật (Bước 3)

Mức tin cậy hiện tại: **nguồn thứ cấp** (báo, công ty luật, cổng tra cứu). Tất cả phải lấy toàn văn từ nguồn chính thức vào `van-ban/` và đối chiếu điều, khoản trước khi viết con số vào skill.

| Văn bản | Hiệu lực | Ghi chú | Skill |
|---|---|---|---|
| Luật Quảng cáo 16/2012/QH13 + Luật sửa đổi 75/2025/QH15 | 01/01/2026 | Bổ sung trách nhiệm người chuyển tải sản phẩm quảng cáo (influencer) | 5, 6, 8, 11 |
| NĐ 342/2025/NĐ-CP hướng dẫn Luật Quảng cáo | 15/02/2026 | Thay NĐ 181/2013 và NĐ 70/2021; danh mục sản phẩm đặc biệt mở rộng từ 8 lên 11 nhóm | 6 |
| Luật Thương mại 36/2005/QH11 + NĐ 81/2018 (sửa bởi NĐ 128/2024 và NĐ 239/2026) | NĐ 239: 26/06/2026 | NĐ 128/2024: giảm tối đa 50%, KM tập trung 100%. NĐ 239/2026: bỏ giới hạn 120 ngày/năm cho giảm giá, thu hẹp nghĩa vụ thông báo, chỉ còn thuốc kê đơn bị cấm khuyến mại | 3, 10 |
| Luật Thương mại điện tử 122/2025/QH15 + NĐ 248/2026/NĐ-CP | 01/07/2026 | Định danh người bán, livestream bán hàng `[đối chiếu số hiệu NĐ]` | 3, 6, 17 |
| Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 + NĐ 356/2025/NĐ-CP | 01/01/2026 | NĐ 356 thay NĐ 13/2023 | 6, 12, 13, 16 |
| NĐ 91/2020/NĐ-CP chống tin nhắn, email, cuộc gọi rác + TT 22/2021/TT-BTTTT | Còn hiệu lực | Bộ Công an đang có dự thảo nghị định thay thế (9/2026) → theo dõi | 6, 13, 16 |
| Luật Bảo vệ quyền lợi người tiêu dùng 2023 | `[cần kiểm tra]` | – | 6, 14, 16 |
| Biểu phí sàn, chính sách quảng cáo Meta/TikTok/Google, quy định ZNS | Thay đổi thường xuyên | Skill có bước "kiểm tra mới nhất", ghi ngày | 3, 8, 16 |

**Phát hiện ảnh hưởng tới nguồn sẽ fork/modify:**
- Quy định khuyến mại vừa đổi (NĐ 239/2026, 26/06/2026). Mọi quy tắc khuyến mại lấy từ M và T phải đối chiếu lại, đặc biệt quy tắc giới hạn thời gian giảm giá.
- Validator T trích "Luật Quảng cáo Điều 8 khoản 11", nhưng Điều 8 đã bị Luật 75/2025 sửa → kiểm lại số khoản trước khi dùng.
- NĐ 181/2013 đã hết hiệu lực từ 15/02/2026 → bất kỳ skill nguồn nào còn dẫn NĐ 181 đều phải sửa.

---

## 6. Cấu trúc repo

```
skills/<ten-skill>/SKILL.md · references/ · scripts/
shared/          # nguyen-tac-chung.md, phap-ly/ (sửa ở đây, build chép vào skill)
van-ban/         # toàn văn văn bản gốc + URL + ngày lấy
qua-tang/        # mẫu Excel pipeline, P&L, KPI dùng ngay
chatgpt/ dist/ .claude-plugin/marketplace.json   # sinh tự động
scripts/build.py # đồng bộ shared, kiểm name/description/file tham chiếu
NOTICE.md        # ghi công C, M, T (MIT), K (Apache 2.0)
upstream.md      # repo nguồn + commit đã lấy, để theo dõi cập nhật
```

## 7. Việc tiếp theo

1. Lấy toàn văn 7 nhóm văn bản ở mục 5 vào `van-ban/`, đối chiếu và gỡ dần các nhãn `[đối chiếu]`.
2. Clone C, M, T, K; ghi commit vào `upstream.md`; trích phần dùng cho đợt 1.
3. Viết đợt 1 theo thứ tự 1 → 3 → 4 → 6 → 12 → 17, kèm dữ liệu mẫu có lỗi cố ý để kiểm thử.
