# -*- coding: utf-8 -*-
"""Quy tắc pháp lý quảng cáo – khuyến mại – dữ liệu cá nhân cho validate_copy.py.

Tự nạp vì tên file bắt đầu bằng rules_. Chỉ dùng thư viện chuẩn. Hợp đồng với engine:
    check_line(ctx, lineno, raw, masked)  -> (rule, severity, col, snippet, message, hint)
    check_document(ctx)                   -> (rule, severity, lineno, col, snippet, message, hint)

Căn cứ: references/phap-ly-marketing-vn.md (ngày tổng hợp 02/11/2026). Đây là công cụ soát
câu chữ, không thay luật sư; cảnh báo là để người duyệt xem lại, không phải kết luận vi phạm.

Một số quy tắc chỉ chạy khi khai --doctype (vd. tpbvsk, kol, form) vì chỉ đúng với loại tài liệu đó.
"""
from __future__ import annotations

import re

ERROR = "error"
WARN = "warning"

RULE_DOCS = {
    "SK001": "tuyên bố như thuốc/điều trị — mỹ phẩm, thực phẩm không được gây hiểu nhầm là thuốc (NĐ 342/2025 Đ4, Đ5)",
    "SK002": "dùng hình ảnh/danh nghĩa bác sĩ, dược sĩ, cơ sở y tế trong quảng cáo mỹ phẩm (NĐ 342/2025 Đ4 k4)",
    "TP001": "quảng cáo thực phẩm bảo vệ sức khỏe thiếu cụm từ 'Thực phẩm bảo vệ sức khỏe' (NĐ 342/2025 Đ5)",
    "TP002": "quảng cáo TPBVSK thiếu câu khuyến cáo 'không phải là thuốc…' (NĐ 342/2025 Đ5)",
    "TP003": "quảng cáo thực phẩm bổ sung thiếu cụm từ 'Thực phẩm bổ sung' (NĐ 342/2025 Đ5)",
    "MP001": "quảng cáo mỹ phẩm/thực phẩm chưa thấy tên, địa chỉ tổ chức chịu trách nhiệm (NĐ 342/2025 Đ4, Đ5)",
    "KM001": "mức giảm giá trên 50% (Điều 7 NĐ 81/2018 sau NĐ 128/2024) — chỉ hợp lệ khi khuyến mại tập trung/ngoại lệ",
    "SS001": "quảng cáo so sánh — cần tài liệu hợp pháp chứng minh (khoản 10 Điều 8 Luật QC, sửa 2025)",
    "KOL001": "nội dung KOL/KOC/tài trợ không có dấu hiệu nhận biết là quảng cáo (Điều 15a, khoản 2 Điều 23 Luật QC sửa 2025)",
    "KOL002": "nội dung KOL/KOC tự nhận 'không phải quảng cáo' trong khi có hợp tác (Điều 15a Luật QC sửa 2025)",
    "DL001": "ô đồng ý được tick sẵn — không được đặt đồng ý mặc định (Luật 91/2025, NĐ 356/2025)",
    "DL002": "form thu thông tin không có câu xin đồng ý (Luật 91/2025 Đ9)",
    "DL003": "form thu thông tin không nhắc chính sách bảo mật / mục đích xử lý (Luật 91/2025)",
    "SPAM001": "tin nhắn/email quảng cáo hàng loạt không có cách từ chối nhận (NĐ 91/2020 Đ11 k5, Đ13 k4)",
    "CK001": "cam kết kết quả tuyệt đối ('cam kết khỏi', 'hiệu quả 100%', 'an toàn tuyệt đối')",
}

DOCTYPES = {
    "my-pham": "quảng cáo mỹ phẩm (nhóm 1, NĐ 342/2025)",
    "tpbvsk": "quảng cáo thực phẩm bảo vệ sức khỏe",
    "thuc-pham-bo-sung": "quảng cáo thực phẩm bổ sung",
    "thuc-pham": "quảng cáo thực phẩm thông thường",
    "kol": "bài/kịch bản của KOL, KOC, người có ảnh hưởng, bài được tài trợ",
    "form": "form/landing thu SĐT, email, thông tin khách",
    "bulk-message": "SMS, email, tin Zalo gửi hàng loạt",
    "promo": "nội dung khuyến mại",
}

# Từ ngữ như thuốc. "trị" đứng một mình quá rộng (trị giá) → chỉ bắt các cụm cụ thể.
THUOC_RE = re.compile(
    r"(?<!\w)(điều trị|chữa khỏi|chữa trị|chữa bệnh|đặc trị|trị dứt điểm|trị tận gốc|khỏi hẳn|khỏi bệnh|"
    r"dứt điểm|tận gốc|thay thế thuốc|kháng sinh|kháng viêm|tiêu viêm|liều dùng|phác đồ|trị mụn|trị nám|trị hói|"
    r"trị sẹo|trị viêm|giảm đau|hạ huyết áp|hạ đường huyết|ngừa ung thư|chống ung thư|tăng chiều cao vượt trội)(?!\w)",
    re.IGNORECASE)
Y_TE_RE = re.compile(r"(?<!\w)(bác sĩ|bs\.|dược sĩ|bệnh viện|phòng khám|y tá|chuyên gia da liễu|áo blouse)(?!\w)", re.IGNORECASE)
CAM_KET_RE = re.compile(
    r"(?<!\w)(cam kết khỏi|cam kết hiệu quả|hiệu quả 100\s*%|100\s*% hiệu quả|an toàn tuyệt đối|không tác dụng phụ|"
    r"không có tác dụng phụ|hoàn tiền nếu không hiệu quả|thấy ngay sau)(?!\w)", re.IGNORECASE)
GIAM_RE = re.compile(
    r"(?<!\w)(?:giảm|sale|off|khuyến mãi|khuyến mại|ưu đãi)\s*(?:giá\s*)?(?:đến|tới|lên đến|lên tới|up to|còn)?\s*"
    r"(\d{1,3})\s*%", re.IGNORECASE)
TAP_TRUNG_RE = re.compile(r"(?:<!--|//|/\*|#)\s*khuyen-mai-tap-trung\s*:|khuyến mại tập trung", re.IGNORECASE)
SO_SANH_RE = re.compile(
    r"(?<!\w)(?:(?i:rẻ|tốt|nhanh|bền|đẹp|mạnh|hiệu quả|chất lượng|an toàn)\s+hơn\s+(?:hẳn\s+)?(?=[A-ZĐ][\w]+)|"
    r"hơn\s+(?:hẳn\s+)?(?:các\s+|mọi\s+)?(?:hãng|thương hiệu|sản phẩm|loại|bên|shop|đối thủ)(?:\s+khác)?|"
    r"vượt trội so với|so với (?:các )?(?:hãng|thương hiệu|sản phẩm|shop|bên|đối thủ)\s+(?:khác|\w+))",
    re.UNICODE)
PROOF_RE = re.compile(r"(?:<!--|//|/\*|#)\s*proof\s*:", re.IGNORECASE)
NHAN_QC_RE = re.compile(
    r"(#\s*quangcao|#\s*quảngcáo|quảng cáo|được tài trợ|tài trợ bởi|hợp tác cùng|hợp tác với|#\s*hoptac|"
    r"#\s*ad\b|#\s*sponsored|sponsored|#\s*taitro|nội dung có trả phí)", re.IGNORECASE)
CHOI_QC_RE = re.compile(r"(không phải quảng cáo|không được tài trợ|không ai trả tiền|review thật không pr|"
                        r"không pr|chẳng ai thuê)", re.IGNORECASE)
TICK_SAN_RE = re.compile(r"(\[\s*[xX✓✔]\s*\]|☑|✅\s*tôi đồng ý|checked(?:=\S+)?\b)", re.IGNORECASE)
DONG_Y_RE = re.compile(r"(đồng ý|chấp thuận|cho phép .* (?:liên hệ|gửi))", re.IGNORECASE)
CHINH_SACH_RE = re.compile(r"(chính sách bảo mật|chính sách quyền riêng tư|bảo vệ dữ liệu|mục đích)", re.IGNORECASE)
THU_TT_RE = re.compile(r"(số điện thoại|sđt|email|e-mail|họ tên|họ và tên|địa chỉ|zalo)", re.IGNORECASE)
TU_CHOI_RE = re.compile(r"(từ chối nhận|hủy nhận|huỷ nhận|hủy đăng ký|huỷ đăng ký|ngừng nhận|dừng nhận|soạn\s+t[uư]\s|"
                        r"unsubscribe|opt[- ]?out|không muốn nhận)", re.IGNORECASE)
CHIU_TN_RE = re.compile(r"(chịu trách nhiệm|phân phối bởi|nhà phân phối|sản xuất bởi|công ty|cty|đơn vị công bố|"
                        r"tổ chức công bố|nhập khẩu bởi|địa chỉ)", re.IGNORECASE)
TPBVSK_RE = re.compile(r"thực phẩm bảo vệ sức kh[oỏ][eẻ]", re.IGNORECASE)
KHUYEN_CAO_RE = re.compile(r"không phải là thuốc[^.\n]*thay thế thuốc chữa bệnh", re.IGNORECASE)
TPBS_RE = re.compile(r"thực phẩm bổ sung", re.IGNORECASE)

DOCTYPE_SUC_KHOE = ("my-pham", "tpbvsk", "thuc-pham-bo-sung", "thuc-pham")


def _bo_qua(raw):
    s = raw.strip()
    return not s or s.startswith(("<!--", "//")) or s.startswith("# ") and s.lower().startswith("# vlc")


def check_line(ctx, lineno, raw, masked):
    dt = ctx.doctype
    if _bo_qua(raw):
        return

    muc = ERROR if dt in DOCTYPE_SUC_KHOE else WARN
    for m in THUOC_RE.finditer(masked):
        yield ("SK001", muc, m.start() + 1, m.group(0),
               f"“{m.group(0)}” là cách nói của thuốc/điều trị",
               "mỹ phẩm, thực phẩm không được gây hiểu nhầm là thuốc — mô tả công dụng đã công bố "
               "(vd. 'hỗ trợ làm sạch', 'giúp da ẩm mịn'); thuốc thật thì phải có xác nhận nội dung quảng cáo")

    for m in CAM_KET_RE.finditer(masked):
        yield ("CK001", WARN, m.start() + 1, m.group(0),
               f"cam kết kết quả tuyệt đối “{m.group(0)}”",
               "chỉ giữ nếu có tài liệu chứng minh; thay bằng chính sách đổi trả cụ thể")

    if not TAP_TRUNG_RE.search(raw):
        for m in GIAM_RE.finditer(masked):
            pt = int(m.group(1))
            if pt > 50:
                yield ("KM001", WARN, m.start() + 1, m.group(0),
                       f"mức giảm {pt}% vượt trần 50%",
                       "hạ xuống ≤ 50%, hoặc ghi tên chương trình khuyến mại tập trung "
                       "<!-- khuyen-mai-tap-trung: ... -->; kiểm tra bằng skill gia-san-pham-khuyen-mai")

    if not (PROOF_RE.search(raw)):
        for m in SO_SANH_RE.finditer(raw):
            yield ("SS001", WARN, m.start() + 1, m.group(0),
                   f"so sánh “{m.group(0).strip()}”",
                   "so với sản phẩm của người khác cần tài liệu hợp pháp chứng minh; an toàn hơn: so với "
                   "phiên bản cũ của chính mình. Có tài liệu → ghi <!-- proof: ... -->")

    if dt in DOCTYPE_SUC_KHOE:
        for m in Y_TE_RE.finditer(masked):
            ghi_chu = ("NĐ 342/2025 Đ4 k4" if dt == "my-pham"
                       else "với thực phẩm: điều khoản tương ứng [CẦN KIỂM TRA]")
            yield ("SK002", WARN, m.start() + 1, m.group(0),
                   f"“{m.group(0)}” trong quảng cáo sản phẩm sức khỏe/làm đẹp",
                   f"{ghi_chu}: không dùng hình ảnh, trang phục, tên, thư tín, bài viết của "
                   "cơ sở y tế, bác sĩ, dược sĩ, nhân viên y tế")

    if dt == "kol":
        for m in CHOI_QC_RE.finditer(masked):
            yield ("KOL002", ERROR, m.start() + 1, m.group(0),
                   f"“{m.group(0)}” trong nội dung có hợp tác",
                   "người có ảnh hưởng phải thông báo về việc quảng cáo ngay trước và trong khi thực hiện")

    if dt == "form":
        for m in TICK_SAN_RE.finditer(raw):
            yield ("DL001", ERROR, m.start() + 1, m.group(0),
                   "ô đồng ý có vẻ đã được chọn sẵn",
                   "để trống mặc định; khách tự tick. Tách 2 ô: liên hệ về đơn hàng / nhận tin khuyến mại")


def _van_ban(ctx):
    return "\n".join(l for l in ctx.lines if not l.strip().startswith("<!--"))


def check_document(ctx):
    dt = ctx.doctype
    if not dt:
        return
    body = _van_ban(ctx)

    if dt == "tpbvsk":
        if not TPBVSK_RE.search(body):
            yield ("TP001", ERROR, 1, 1, "", "thiếu cụm từ “Thực phẩm bảo vệ sức khỏe”",
                   "NĐ 342/2025 Điều 5: quảng cáo TPBVSK phải có cụm từ này")
        if not KHUYEN_CAO_RE.search(body):
            yield ("TP002", ERROR, 1, 1, "", "thiếu câu khuyến cáo bắt buộc",
                   "thêm nguyên văn: “Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh”")
    if dt == "thuc-pham-bo-sung" and not TPBS_RE.search(body):
        yield ("TP003", ERROR, 1, 1, "", "thiếu cụm từ “Thực phẩm bổ sung”", "NĐ 342/2025 Điều 5")
    if dt in DOCTYPE_SUC_KHOE and not CHIU_TN_RE.search(body):
        yield ("MP001", WARN, 1, 1, "", "chưa thấy tên, địa chỉ tổ chức/cá nhân chịu trách nhiệm về sản phẩm",
               "NĐ 342/2025 Điều 4 (mỹ phẩm), Điều 5 (thực phẩm): thông tin bắt buộc")
    if dt == "kol" and not NHAN_QC_RE.search(body):
        yield ("KOL001", ERROR, 1, 1, "", "không có dấu hiệu nhận biết là quảng cáo/hợp tác",
               "thêm 'Quảng cáo' / 'Hợp tác cùng [thương hiệu]' / #quangcao ở đầu bài, nhìn thấy không cần mở rộng")
    if dt == "form" and THU_TT_RE.search(body):
        if not DONG_Y_RE.search(body):
            yield ("DL002", ERROR, 1, 1, "", "form thu thông tin nhưng không có câu xin đồng ý",
                   "thêm ô: 'Tôi đồng ý để [công ty] liên hệ tư vấn về [mục đích]' (không tick sẵn)")
        if not CHINH_SACH_RE.search(body):
            yield ("DL003", WARN, 1, 1, "", "không nhắc mục đích xử lý / chính sách bảo mật",
                   "nêu mục đích và link chính sách bảo mật dữ liệu cá nhân")
    if dt == "bulk-message" and not TU_CHOI_RE.search(body):
        yield ("SPAM001", WARN, 1, 1, "", "không thấy cách từ chối nhận tin",
               "thêm cách từ chối (vd. 'Soạn TC gửi …' / link hủy nhận); chỉ gửi người đã đồng ý; "
               "SMS 07:00–22:00, gọi 08:00–17:00, ≤ 3 tin/24 giờ (NĐ 91/2020 Đ13)")
