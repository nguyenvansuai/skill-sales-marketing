#!/usr/bin/env python3
"""Kiểm tra một chương trình khuyến mại theo NĐ 81/2018 (sửa bởi NĐ 128/2024, NĐ 239/2026) và TT 39/2025/TT-BCT (trần 50%/100%).

In ra: hợp lệ hay không, giới hạn áp dụng, thủ tục phải làm, căn cứ và nhãn tin cậy.
Căn cứ chi tiết: references/phap-ly-marketing-vn.md mục 3. Không phải tư vấn pháp lý.

Ví dụ:
    python3 kiem_khuyen_mai.py --hinh-thuc giam-gia --gia-truoc 300000 --gia-sau 120000
    python3 kiem_khuyen_mai.py --hinh-thuc giam-gia --muc-giam 70% --tap-trung
    python3 kiem_khuyen_mai.py --hinh-thuc tang-qua --gia-hang 300000 --gia-tri-qua 200000
    python3 kiem_khuyen_mai.py --hinh-thuc phieu-du-thi --tong-giai 150tr
    python3 kiem_khuyen_mai.py --hinh-thuc phieu-du-thi --tong-giai 150tr --chi-online
    python3 kiem_khuyen_mai.py --hinh-thuc may-rui --tong-giai 80tr --mat-hang "son môi"

Hình thức: hang-mau | tang-qua | tang-khong-kem-mua | giam-gia | phieu-mua-hang | phieu-du-thi |
           may-rui | khach-hang-thuong-xuyen | van-hoa-giai-tri
"""
from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402

NGAY_TONG_HOP = "02/11/2026"

# Hàng hóa, dịch vụ không được khuyến mại / dùng để khuyến mại (Điều 5 NĐ 81/2018 sửa bởi Điều 1 NĐ 239/2026) [NGUYÊN VĂN]
CAM = {
    "rượu": "rượu", "xổ số": "xổ số", "vé số": "xổ số", "thuốc lá": "thuốc lá", "thuốc lá điện tử": "thuốc lá",
    "sữa thay thế sữa mẹ": "sữa thay thế sữa mẹ", "sữa công thức": "sữa thay thế sữa mẹ [CẦN KIỂM TRA theo độ tuổi]",
    "thuốc kê đơn": "thuốc kê đơn (chỉ khuyến mại giữa thương nhân kinh doanh thuốc)",
}
CAN_KIEM_TRA = {
    "bia": "bia — đối chiếu Luật Phòng, chống tác hại của rượu, bia [CẦN KIỂM TRA]",
    "thuốc": "thuốc — chỉ thuốc kê đơn bị cấm khuyến mại cho người tiêu dùng; thuốc không kê đơn theo pháp luật dược [CẦN KIỂM TRA]",
    "khám bệnh": "dịch vụ khám chữa bệnh — cấm nếu là cơ sở công lập",
    "học phí": "dịch vụ giáo dục — cấm nếu là cơ sở giáo dục công lập hoặc cơ sở giáo dục nghề nghiệp công lập",
    "hàng cấm khuyến mại": "hàng cấm khuyến mại theo Điều 100 Luật Thương mại",
}

HINH_THUC = {
    "hang-mau": "Đưa hàng mẫu, cung ứng dịch vụ mẫu để dùng thử không trả tiền (Điều 8)",
    "tang-qua": "Tặng hàng hóa, dịch vụ kèm theo mua hàng (Điều 9)",
    "tang-khong-kem-mua": "Tặng hàng hóa, dịch vụ không kèm mua (khoản 2 Điều 9)",
    "giam-gia": "Bán hàng, cung ứng dịch vụ với giá thấp hơn giá trước đó (Điều 10)",
    "phieu-mua-hang": "Bán hàng kèm phiếu mua hàng, phiếu sử dụng dịch vụ (Điều 11)",
    "phieu-du-thi": "Bán hàng kèm phiếu dự thi trúng thưởng (Điều 12)",
    "may-rui": "Chương trình mang tính may rủi (Điều 13)",
    "khach-hang-thuong-xuyen": "Chương trình khách hàng thường xuyên — thẻ, phiếu tích điểm (Điều 14)",
    "van-hoa-giai-tri": "Chương trình văn hóa, nghệ thuật, giải trí (khoản 8 Điều 92 Luật Thương mại)",
}

# Hình thức không chịu hạn mức 50% giá trị hàng dùng để khuyến mại (khoản 1 Điều 3 TT 39/2025/TT-BCT) [NGUYÊN VĂN]
KHONG_HAN_MUC_QUA = {"hang-mau", "tang-khong-kem-mua", "phieu-du-thi", "may-rui", "khach-hang-thuong-xuyen", "van-hoa-giai-tri"}


def _bo_dau(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn").replace("đ", "d")


def kiem_mat_hang(mat_hang: str):
    ra = []
    if not mat_hang:
        return ra, []
    mh = _bo_dau(mat_hang)
    cam = [ly_do for tu, ly_do in CAM.items() if _bo_dau(tu) in mh]
    if any(_bo_dau(x) in mh for x in ("thuoc khong ke don",)):
        cam = [c for c in cam if not c.startswith("thuốc kê đơn")]
    can = [ly_do for tu, ly_do in CAN_KIEM_TRA.items() if _bo_dau(tu) in mh.split() or (_bo_dau(tu) in mh and " " in tu)]
    if "thuoc" in mh.split() and not cam:
        can.append(CAN_KIEM_TRA["thuoc"])
    return cam, sorted(set(can))


def kiem(a):
    hop_le, gioi_han, thu_tuc, luu_y, can = True, [], [], [], []
    ht = a.hinh_thuc

    cam, can_mh = kiem_mat_hang(a.mat_hang or "")
    if cam:
        hop_le = False
        gioi_han.append("Mặt hàng thuộc danh mục **không được khuyến mại / dùng để khuyến mại**: " + "; ".join(cam) + " — Điều 5 NĐ 81/2018 (khoản 2 Điều 17 NĐ 81 sửa bởi NĐ 239/2026) [NGUYÊN VĂN].")
    can += can_mh

    if ht == "giam-gia":
        if a.muc_giam:
            giam = doc_phan_tram(a.muc_giam)
        elif a.gia_truoc and a.gia_sau:
            gt, gs = doc_tien(a.gia_truoc), doc_tien(a.gia_sau)
            giam = 1 - gs / gt
            luu_y.append(f"Giá trước {in_tien(gt)} → giá sau {in_tien(gs)} đồng.")
        else:
            raise SoKhongDoc("giảm giá cần --muc-giam hoặc --gia-truoc và --gia-sau")
        if a.ngoai_le:
            gioi_han.append(f"Mức giảm {in_pt(giam)} — **không áp hạn mức** do thuộc ngoại lệ '{a.ngoai_le}' (khoản 3 Điều 4 TT 39/2025/TT-BCT) [NGUYÊN VĂN]. Giữ hồ sơ chứng minh ngoại lệ.")
        elif a.tap_trung:
            gioi_han.append(f"Mức giảm {in_pt(giam)} ≤ 100% (khuyến mại tập trung, khoản 2 Điều 4 TT 39/2025/TT-BCT; Tết Âm lịch: 30 ngày trước mùng 1) [NGUYÊN VĂN]. Ghi rõ tên chương trình khuyến mại tập trung và văn bản tổ chức.")
            if giam > 1:
                hop_le = False
        elif giam > 0.5:
            hop_le = False
            gioi_han.append(f"Mức giảm **{in_pt(giam)} vượt trần 50%** giá ngay trước khuyến mại (khoản 1 Điều 4 TT 39/2025/TT-BCT; NĐ 239/2026 đã bãi bỏ Điều 7 NĐ 81) [NGUYÊN VĂN]. Hạ xuống ≤ 50%, hoặc chỉ chạy trong khuyến mại tập trung.")
        else:
            gioi_han.append(f"Mức giảm {in_pt(giam)} ≤ trần 50% (khoản 1 Điều 4 TT 39/2025/TT-BCT) [NGUYÊN VĂN].")
        luu_y.append("Không còn giới hạn tổng 120 ngày/năm cho giảm giá — đã bãi bỏ bởi khoản 2 Điều 11 NĐ 239/2026 từ 26/06/2026 [NGUYÊN VĂN].")
        luu_y.append("'Giá trước khuyến mại' phải là giá thật đã bán ngay trước đó; nâng giá rồi gạch là vi phạm riêng.")
        thu_tuc.append("Không phải thông báo với Sở Công Thương (khoản 2 Điều 17 NĐ 81 sửa bởi NĐ 239/2026) [NGUYÊN VĂN]. Vẫn phải công khai thông tin khuyến mại cho khách.")

    elif ht in ("tang-qua", "phieu-mua-hang"):
        if a.gia_hang and a.gia_tri_qua:
            gh, gq = doc_tien(a.gia_hang), doc_tien(a.gia_tri_qua)
            ty_le = gq / gh
            if a.tap_trung:
                gioi_han.append(f"Giá trị quà/phiếu {in_tien(gq)} = {in_pt(ty_le)} giá hàng; trần 100% trong khuyến mại tập trung (khoản 4 Điều 3 TT 39/2025/TT-BCT) [NGUYÊN VĂN].")
                hop_le = hop_le and ty_le <= 1
            elif ty_le > 0.5:
                hop_le = False
                gioi_han.append(f"Giá trị quà/phiếu **{in_pt(ty_le)} giá hàng — vượt trần 50%** (khoản 1 Điều 3 TT 39/2025/TT-BCT) [NGUYÊN VĂN].")
            else:
                gioi_han.append(f"Giá trị quà/phiếu {in_pt(ty_le)} giá hàng ≤ 50% (khoản 1 Điều 3 TT 39/2025/TT-BCT) [NGUYÊN VĂN].")
        else:
            can.append("Thiếu --gia-hang và --gia-tri-qua để kiểm hạn mức 50% giá trị hàng dùng để khuyến mại.")
        thu_tuc.append("Không phải thông báo (khoản 2 Điều 17 NĐ 81 sửa bởi NĐ 239/2026) [NGUYÊN VĂN].")

    elif ht == "phieu-du-thi":
        if not a.tong_giai:
            raise SoKhongDoc("phiếu dự thi cần --tong-giai (tổng giá trị giải thưởng, quà tặng)")
        tg = doc_tien(a.tong_giai)
        if tg >= 100e6 and not a.chi_online:
            thu_tuc.append(f"**Phải thông báo** hoạt động khuyến mại cho Sở Công Thương nơi tổ chức (tổng giải {in_tien(tg)} ≥ 100 triệu và có triển khai ngoài sàn/web/app khuyến mại trực tuyến) — khoản 2 Điều 17 NĐ 81 sửa bởi NĐ 239/2026 [NGUYÊN VĂN]. Hồ sơ phải đến Sở Công Thương **tối thiểu 03 ngày làm việc trước** khi thực hiện, gửi qua bưu chính hoặc Cổng Dịch vụ công quốc gia (khoản 1, 3 Điều 17 sửa bởi NĐ 239/2026) [NGUYÊN VĂN].")
        else:
            ly_do = "chỉ thực hiện qua sàn TMĐT/website/ứng dụng" if a.chi_online else f"tổng giải {in_tien(tg)} < 100 triệu"
            thu_tuc.append(f"Không phải thông báo ({ly_do}) — khoản 2 Điều 17 NĐ 81 sửa bởi NĐ 239/2026 [NGUYÊN VĂN].")
        luu_y.append("Thể lệ, cơ cấu giải, thời gian, cách xác định người thắng phải công khai.")

    elif ht == "may-rui":
        thu_tuc.append("Chương trình may rủi (Điều 13): phải **đăng ký và được xác nhận trước** khi thực hiện (khoản 1 Điều 19 NĐ 81/2018) [NGUYÊN VĂN]; nộp qua bưu chính hoặc Cổng Dịch vụ công quốc gia (khoản 3 Điều 19 sửa bởi NĐ 239/2026) [NGUYÊN VĂN]. Cơ quan tiếp nhận (Sở Công Thương nếu 1 tỉnh, Bộ Công Thương nếu từ 2 tỉnh — khoản 2 Điều 19) sau các đợt phân cấp [CẦN KIỂM TRA].")
        luu_y.append("Xác định trúng thưởng phải công khai, theo thể lệ, có khách chứng kiến trực tiếp hoặc trực tuyến và lập biên bản — khoản 1 Điều 13 NĐ 81 sửa bởi NĐ 239/2026 [NGUYÊN VĂN].")
        luu_y.append("Giải không có người trúng: trích nộp 50% giá trị vào ngân sách, trừ giải trao quá hạn do bất khả kháng/trở ngại khách quan — khoản 4, 5 Điều 13 NĐ 81 (khoản 5 sửa bởi NĐ 239/2026) [NGUYÊN VĂN].")
        if a.tong_giai:
            luu_y.append(f"Tổng giải khai báo: {in_tien(doc_tien(a.tong_giai))} đồng.")

    elif ht == "khach-hang-thuong-xuyen":
        thu_tuc.append("Không còn phải thông báo (điểm a khoản 2 Điều 17 NĐ 81 sửa bởi NĐ 239/2026) [NGUYÊN VĂN].")
        luu_y.append("Thể lệ tích điểm, quy đổi, thời hạn điểm phải công khai và áp dụng thống nhất.")

    elif ht in ("hang-mau", "tang-khong-kem-mua", "van-hoa-giai-tri"):
        gioi_han.append("Không chịu hạn mức 50% giá trị hàng dùng để khuyến mại (khoản 1 Điều 3 TT 39/2025/TT-BCT) [NGUYÊN VĂN].")
        thu_tuc.append("Không phải thông báo (khoản 2 Điều 17 NĐ 81 sửa bởi NĐ 239/2026) [NGUYÊN VĂN].")
        if ht == "hang-mau":
            luu_y.append("Hàng mẫu phải là hàng đang kinh doanh hoặc sắp kinh doanh; người nhận không phải trả tiền.")

    return hop_le, gioi_han, thu_tuc, luu_y, can


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--hinh-thuc", required=True, choices=sorted(HINH_THUC))
    p.add_argument("--muc-giam")
    p.add_argument("--gia-truoc")
    p.add_argument("--gia-sau")
    p.add_argument("--gia-hang")
    p.add_argument("--gia-tri-qua")
    p.add_argument("--tong-giai")
    p.add_argument("--chi-online", action="store_true", help="chỉ thực hiện qua sàn TMĐT/website/ứng dụng khuyến mại trực tuyến")
    p.add_argument("--tap-trung", action="store_true", help="nằm trong chương trình khuyến mại tập trung")
    p.add_argument("--ngoai-le", choices=["binh-on-gia", "tuoi-song", "pha-san-giai-the"])
    p.add_argument("--mat-hang", default="")
    a = p.parse_args(argv)
    try:
        hop_le, gioi_han, thu_tuc, luu_y, can = kiem(a)
    except SoKhongDoc as exc:
        print(f"[?] {exc}. Script không tự đoán — anh/chị bổ sung số liệu.")
        return 2
    print(f"## Kiểm tra khuyến mại — {HINH_THUC[a.hinh_thuc]}\n")
    print(f"**Kết luận:** {'Có thể thực hiện, kèm các điều kiện dưới đây.' if hop_le else 'KHÔNG hợp lệ như đang thiết kế — sửa theo mục Giới hạn.'}\n")
    for tieu_de, ds in (("Giới hạn", gioi_han), ("Thủ tục", thu_tuc), ("Lưu ý", luu_y), ("Cần anh/chị kiểm tra", can)):
        if ds:
            print(f"### {tieu_de}\n" + "\n".join(f"- {x}" for x in ds) + "\n")
    print(f"Căn cứ tổng hợp ngày {NGAY_TONG_HOP} (references/phap-ly-marketing-vn.md mục 3). "
          "Đối chiếu văn bản hiện hành và hỏi Sở Công Thương/luật sư trước khi chạy chương trình.")
    return 0 if hop_le else 1


if __name__ == "__main__":
    sys.exit(main())
