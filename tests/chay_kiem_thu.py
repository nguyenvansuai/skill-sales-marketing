#!/usr/bin/env python3
"""Chạy thử mọi script với dữ liệu mẫu có lỗi cố ý (tests/du-lieu-mau/) và so kết quả mong đợi.

    python3 tests/chay_kiem_thu.py

Số mong đợi đã tính tay. Sửa script mà test đỏ → kiểm lại công thức trước khi sửa test.
"""
import subprocess
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
D = "tests/du-lieu-mau"
S = "skills"

CA = [
    ("Đối soát: loại trùng, hủy, 'Hoàn thành' không bị loại, dòng lệch cột → [?]",
     f"{S}/bao-cao-doi-soat-hieu-qua/scripts/doi_soat.py --tu 01/10/2026 --den 31/10/2026 --san {D}/san.csv --crm {D}/crm.csv --ads {D}/ads.csv --tk {D}/saoke.csv --ty-le-gia-von 44%",
     ["Doanh thu thật 3.530.000 đồng từ 6 đơn", "SP004", "lệch cột", "KHÔNG ngoại suy", "CRM01, CRM02"]),
    ("Giá: P&L từng đơn, hòa vốn, giảm 50% bị lỗ",
     f"{S}/gia-san-pham-khuyen-mai/scripts/tinh_gia.py --gia-ban 250000 --gia-von 110000 --phi 'hoa hồng sàn=8%' --phi 'thanh toán=3%' --phi 'trợ giá ship=5000' --ty-le-hoan 4% --chi-phi-moi-don-hoan 60000 --giam 50%",
     ["105.100", "2,38", "131.910", "47,2%", "-6.150"]),
    ("Giá theo CSV, ô mờ → [?]", f"{S}/gia-san-pham-khuyen-mai/scripts/tinh_gia.py --csv {D}/san_pham.csv",
     ["39.400", "SON01 | [?]"]),
    ("Khuyến mại: giảm 70% không tập trung → không hợp lệ",
     f"{S}/gia-san-pham-khuyen-mai/scripts/kiem_khuyen_mai.py --hinh-thuc giam-gia --muc-giam 70%",
     ["KHÔNG hợp lệ", "vượt trần 50%"]),
    ("Khuyến mại: phiếu dự thi 150 triệu → phải thông báo",
     f"{S}/gia-san-pham-khuyen-mai/scripts/kiem_khuyen_mai.py --hinh-thuc phieu-du-thi --tong-giai 150tr",
     ["Phải thông báo"]),
    ("KPI B2C: CAC vượt CPA hòa vốn → cảnh báo lỗ",
     f"{S}/ke-hoach-ngan-sach-kpi/scripts/kpi_nguoc.py --mo-hinh b2c --doanh-thu 900tr --so-thang 3 --he-so-mua-vu 1,1,1.5 --aov 350000 --ty-le-chot 12% --chi-phi-lead 25000 --doanh-thu-khach-cu 20% --bien-truoc-ads 42%",
     ["17.143", "428.571.429", "CẢNH BÁO"]),
    ("KPI B2B: làm tròn lên số đếm được",
     f"{S}/ke-hoach-ngan-sach-kpi/scripts/kpi_nguoc.py --mo-hinh b2b --doanh-thu 2ty --so-thang 6 --gia-tri-hop-dong 80tr --ty-le-thang 25% --ty-le-lead-co-hoi 30% --ty-le-hoat-dong-lead 5%",
     ["334 lead → 100 cơ hội → 25 hợp đồng"]),
    ("Quảng cáo mỹ phẩm vi phạm",
     f"{S}/kiem-tra-phap-ly-quang-cao/scripts/validate_copy.py {D}/quang_cao_vi_pham.md --doctype my-pham",
     ["LAW001", "“đặc trị”", "“tận gốc”", "SS001", "SK002", "KM001"]),
    ("Bài KOC thiếu nhãn quảng cáo", f"{S}/kiem-tra-phap-ly-quang-cao/scripts/validate_copy.py {D}/bai_koc_thieu_nhan.md --doctype kol", ["KOL001"]),
    ("Form tick sẵn đồng ý", f"{S}/kiem-tra-phap-ly-quang-cao/scripts/validate_copy.py {D}/form_thu_thap.html --doctype form", ["DL001"]),
    ("Đọc số ads: phân loại theo hòa vốn",
     f"{S}/quang-cao-truc-tuyen/scripts/doc_so_ads.py {D}/ads_chien_dich.csv --roas-hoa-von 2,38 --roas-muc-tieu 3 --toi-thieu-chi-phi 1tr",
     ["11.400.000", "Dưới hòa vốn", "Chưa đủ dữ liệu", "Trên mục tiêu"]),
    ("KOC: số đơn hòa vốn, hoa hồng ≥ biên", f"{S}/koc-affiliate-doi-tac/scripts/tinh_koc.py {D}/koc.csv --aov 350000 --bien-truoc-ads 42%",
     ["| 98 |", "-7.716.000", "mỗi đơn đều lỗ"]),
    ("Trade ROI", f"{S}/trade-marketing-diem-ban/scripts/tinh_trade.py roi --so-diem 40 --chi-phi-moi-diem 600000 --chi-phi-co-dinh 5tr --dt-moi-diem-truoc 8tr --tang-thu-nghiem 12% --bien-gop 30% --so-thang 3",
     ["77.000.000", "26,7%", "-42.440.000"]),
    ("Trade thưởng bậc", f"{S}/trade-marketing-diem-ban/scripts/tinh_trade.py thuong-bac {D}/dai_ly.csv --bac 50tr=1%,100tr=2%,200tr=3%", ["8.700.000"]),
    ("Hoa hồng theo bậc", f"{S}/quan-ly-doi-sales/scripts/hoa_hong_du_bao.py hoa-hong {D}/ket_qua_sales.csv --bac 80%=2%,100%=3%,120%=4%", ["9.450.000", "Chi: "]),
    ("Dự báo: sales có chỉ tiêu nhưng chưa có cơ hội vẫn hiện",
     f"{S}/quan-ly-doi-sales/scripts/hoa_hong_du_bao.py du-bao {D}/co_hoi.csv --thang 12/2026 --chi-tieu An=300tr,Bình=250tr", ["104.000.000", "| Bình | 0 |"]),
    ("RFM", f"{S}/cham-soc-giu-chan-khach/scripts/rfm.py {D}/don_hang_rfm.csv --ngay-tinh 02/11/2026", ["= 4", "loại 1 đơn"]),
    ("Báo giá thiếu thuế suất → tổng tạm tính",
     f"{S}/tim-khach-b2b-bao-gia/scripts/tao_bao_gia.py {D}/bao_gia.csv --ben-ban A --khach B --hieu-luc 15 --ngay 02/11/2026", ["TẠM TÍNH", "thiếu thuế suất"]),
]


def main():
    hong = 0
    for ten, lenh, mong_doi in CA:
        r = subprocess.run(f"{sys.executable} {lenh}", shell=True, cwd=GOC, capture_output=True, text=True)
        out = r.stdout + r.stderr
        thieu = [m for m in mong_doi if m not in out]
        if thieu:
            hong += 1
            print(f"✗ {ten}\n    thiếu: {thieu}")
        else:
            print(f"✓ {ten}")
    for f in sorted((GOC / "skills").glob("*/scripts/*.py")):
        if f.name in ("vn_money.py", "tao_bao_gia.py"):
            r = subprocess.run([sys.executable, "-m", "doctest", str(f)], capture_output=True, text=True)
            print(("✓" if r.returncode == 0 else "✗") + f" doctest {f.parent.parent.name}/{f.name}")
            hong += r.returncode != 0
    print(f"\n{len(CA) - min(hong, len(CA))}/{len(CA)} ca đạt" if not hong else f"\n{hong} lỗi")
    return 1 if hong else 0


if __name__ == "__main__":
    sys.exit(main())
