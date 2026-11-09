#!/usr/bin/env python3
"""Tính hiệu quả chương trình trade marketing và thưởng doanh số theo bậc cho đại lý/điểm bán.

Hai chế độ:
  roi        — chương trình trưng bày/POSM/thưởng: chi phí vs lợi nhuận gộp tăng thêm, mức tăng hòa vốn
  thuong-bac — tính thưởng từng đại lý theo bậc doanh số (CSV), tổng chi thưởng, % trên doanh số

Mức tăng doanh số phải lấy từ THỬ NGHIỆM THẬT (nhóm có chương trình so với nhóm không có), không giả định.

Ví dụ:
    python3 tinh_trade.py roi --so-diem 40 --chi-phi-moi-diem 600000 --chi-phi-co-dinh 5tr \
        --dt-moi-diem-truoc 8tr --tang-thu-nghiem 12% --bien-gop 35% --so-thang 3
    python3 tinh_trade.py thuong-bac dai_ly.csv --bac "50tr=1%,100tr=2%,200tr=3%" [--luy-tien]
        # CSV: ma,ten,doanh_so   (doanh số thuần trong kỳ, đã trừ hàng trả lại)
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402


def roi(a):
    n = int(a.so_diem)
    cp_diem, cp_cd = doc_tien(a.chi_phi_moi_diem), doc_tien(a.chi_phi_co_dinh or 0)
    dt_truoc, bien = doc_tien(a.dt_moi_diem_truoc), doc_phan_tram(a.bien_gop)
    thang = int(a.so_thang)
    tong_cp = n * cp_diem * thang + cp_cd
    print(f"## Hiệu quả chương trình trade — {n} điểm, {thang} tháng\n")
    print("| Khoản | Giá trị |\n|---|---:|")
    print(f"| Tổng chi phí chương trình | {in_tien(tong_cp)} |")
    tang_hv = tong_cp / bien / (n * dt_truoc * thang)
    print(f"| Doanh số tăng thêm cần để hòa vốn | {in_tien(tong_cp / bien)} ({in_pt(tang_hv)} so với trước) |")
    can = []
    if a.tang_thu_nghiem:
        tang = doc_phan_tram(a.tang_thu_nghiem)
        dt_them = n * dt_truoc * thang * tang
        ln_them = dt_them * bien
        print(f"| Doanh số tăng thêm (theo thử nghiệm {in_pt(tang)}) | {in_tien(dt_them)} |")
        print(f"| Lợi nhuận gộp tăng thêm | {in_tien(ln_them)} |")
        print(f"| Lãi/lỗ của chương trình | {in_tien(ln_them - tong_cp)} |")
        print(f"| ROI | {in_pt((ln_them - tong_cp) / tong_cp)} |")
        ket = "có lãi" if ln_them > tong_cp else "LỖ"
        print(f"\n**Kết luận:** với mức tăng {in_pt(tang)} đo từ thử nghiệm, chương trình {ket}; cần tăng ≥ {in_pt(tang_hv)} để hòa vốn.")
    else:
        print(f"\n**Kết luận:** cần doanh số mỗi điểm tăng ≥ {in_pt(tang_hv)} để hòa vốn.")
        can.append("Chưa có --tang-thu-nghiem: chạy thử ở 5–10 điểm (so với nhóm điểm không có chương trình) trước khi mở rộng.")
    print("\nĐã kiểm tra phép tính.")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))


def doc_bac(chuoi):
    bac = []
    for phan in chuoi.split(","):
        nguong, ty_le = phan.split("=")
        bac.append((doc_tien(nguong), doc_phan_tram(ty_le)))
    return sorted(bac)


def thuong(ds, bac, luy_tien):
    if not luy_tien:
        ty = 0.0
        for nguong, t in bac:
            if ds >= nguong:
                ty = t
        return ds * ty, ty
    # lũy tiến: mỗi bậc áp tỷ lệ cho phần doanh số nằm trong bậc đó
    tien, moc = 0.0, [n for n, _ in bac] + [float("inf")]
    for i, (nguong, t) in enumerate(bac):
        if ds > nguong:
            tien += (min(ds, moc[i + 1]) - nguong) * t
    return tien, (tien / ds if ds else 0)


def thuong_bac(a):
    bac = doc_bac(a.bac)
    tong_ds = tong_th = 0.0
    loi = []
    print(f"## Thưởng doanh số theo bậc ({'lũy tiến từng phần' if a.luy_tien else 'đạt bậc nào hưởng tỷ lệ bậc đó trên toàn bộ doanh số'})\n")
    print("Bậc: " + "; ".join(f"từ {in_tien(n)} → {in_pt(t)}" for n, t in bac) + "\n")
    print("| Mã | Tên | Doanh số | Tỷ lệ thưởng hiệu dụng | Tiền thưởng | Thiếu để lên bậc tiếp |\n|---|---|---:|---:|---:|---:|")
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            try:
                ds = doc_tien(d.get("doanh_so"))
            except SoKhongDoc:
                loi.append(f"Dòng {i} ({d.get('ma', '?')}): doanh số '{d.get('doanh_so')}' không đọc được → [?]")
                print(f"| {d.get('ma', '')} | {d.get('ten', '')} | [?] | | | |")
                continue
            th, ty = thuong(ds, bac, a.luy_tien)
            ke = next((n for n, _ in bac if n > ds), None)
            tong_ds += ds
            tong_th += th
            print(f"| {d.get('ma', '')} | {d.get('ten', '')} | {in_tien(ds)} | {in_pt(ty, 2)} | {in_tien(th)} | {in_tien(ke - ds) if ke else '—'} |")
    print(f"| **Tổng** | | **{in_tien(tong_ds)}** | {in_pt(tong_th / tong_ds, 2) if tong_ds else '—'} | **{in_tien(tong_th)}** | |")
    print("\nĐã kiểm tra phép tính (tổng = cộng từng đại lý).")
    print("Thưởng/chiết khấu cho đại lý: thể hiện trên hợp đồng và hóa đơn theo hướng dẫn kế toán; quy định khuyến mại giữa thương nhân `[CẦN KIỂM TRA]`.")
    if loi:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {x}" for x in loi))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="che_do", required=True)
    r = sub.add_parser("roi")
    r.add_argument("--so-diem", required=True); r.add_argument("--chi-phi-moi-diem", required=True)
    r.add_argument("--chi-phi-co-dinh"); r.add_argument("--dt-moi-diem-truoc", required=True)
    r.add_argument("--tang-thu-nghiem"); r.add_argument("--bien-gop", required=True); r.add_argument("--so-thang", default="1")
    t = sub.add_parser("thuong-bac")
    t.add_argument("csv"); t.add_argument("--bac", required=True); t.add_argument("--luy-tien", action="store_true")
    a = p.parse_args(argv)
    try:
        roi(a) if a.che_do == "roi" else thuong_bac(a)
    except (SoKhongDoc, ValueError) as exc:
        print(f"[?] {exc} — script không tự đoán, anh/chị kiểm tra lại số liệu.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
