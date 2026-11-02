#!/usr/bin/env python3
"""Tính hoa hồng theo mức đạt chỉ tiêu và dự báo doanh số từ pipeline.

Chế độ:
  hoa-hong  CSV: ten, chi_tieu, doanh_so_thu_duoc  (tiền đã thu, sau trả hàng — không phải doanh số đặt)
            --bac "80%=2%,100%=3%,120%=4%"  : đạt ≥ 80% chỉ tiêu hưởng 2% trên doanh số thu được, …
            --tran 6%  (tùy chọn, trần tỷ lệ hoa hồng)
  du-bao    CSV: sales, giai_doan, gia_tri, xac_suat, ngay_du_kien_chot (dd/mm/yyyy)
            (xuất từ sheet 'Cơ hội' của file pipeline) --chi-tieu "An=300tr,Bình=250tr" --thang 12/2026

Ví dụ:
    python3 hoa_hong_du_bao.py hoa-hong ket_qua.csv --bac "80%=2%,100%=3%,120%=4%"
    python3 hoa_hong_du_bao.py du-bao co_hoi.csv --thang 12/2026 --chi-tieu "An=300tr,Bình=250tr"
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402


def hoa_hong(a):
    bac = sorted((doc_phan_tram(k), doc_phan_tram(v)) for k, v in (x.split("=") for x in a.bac.split(",")))
    tran = doc_phan_tram(a.tran) if a.tran else None
    can, tong_ds, tong_hh = [], 0.0, 0.0
    print("## Hoa hồng theo mức đạt chỉ tiêu\n")
    print("Cơ chế: " + "; ".join(f"đạt ≥ {in_pt(m, 0)} → {in_pt(t)} doanh số thu được" for m, t in bac) + "\n")
    print("| Sales | Chỉ tiêu | Doanh số thu được | % đạt | Tỷ lệ hoa hồng | Hoa hồng | Thiếu để lên bậc |\n|---|---:|---:|---:|---:|---:|---:|")
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            ten = d.get("ten") or f"(dòng {i})"
            try:
                ct, ds = doc_tien(d.get("chi_tieu")), doc_tien(d.get("doanh_so_thu_duoc"))
            except SoKhongDoc as exc:
                can.append(f"{ten}: {exc} → [?]")
                print(f"| {ten} | [?] | [?] | | | | |")
                continue
            dat = ds / ct if ct else 0
            ty = 0.0
            for moc, t in bac:
                if dat >= moc:
                    ty = t
            if tran is not None:
                ty = min(ty, tran)
            hh = ds * ty
            ke = next((moc for moc, _ in bac if moc > dat), None)
            tong_ds += ds
            tong_hh += hh
            print(f"| {ten} | {in_tien(ct)} | {in_tien(ds)} | {in_pt(dat)} | {in_pt(ty)} | {in_tien(hh)} | "
                  f"{in_tien(ke * ct - ds) if ke else '—'} |")
    print(f"| **Tổng** | | **{in_tien(tong_ds)}** | | {in_pt(tong_hh / tong_ds, 2) if tong_ds else '—'} | **{in_tien(tong_hh)}** | |")
    print("\nĐã kiểm tra phép tính. Hoa hồng tính trên **tiền đã thu**, sau trả hàng.")
    print("Hoa hồng có thể là một phần tiền lương theo Bộ luật Lao động — ghi rõ trong hợp đồng/quy chế lương; thuế TNCN hỏi kế toán `[CẦN KIỂM TRA]`.")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))


def du_bao(a):
    thang, nam = (int(x) for x in a.thang.split("/"))
    chi_tieu = {}
    if a.chi_tieu:
        for x in a.chi_tieu.split(","):
            k, v = x.split("=")
            chi_tieu[k.strip()] = doc_tien(v)
    theo_sales, can = {}, []
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            s = (d.get("sales") or "").strip() or "(chưa giao)"
            try:
                gt = doc_tien(d.get("gia_tri"))
                xs = doc_phan_tram(d.get("xac_suat"))
                ngay = dt.datetime.strptime((d.get("ngay_du_kien_chot") or "").strip(), "%d/%m/%Y").date()
            except (SoKhongDoc, ValueError) as exc:
                can.append(f"Dòng {i}: thiếu/sai giá trị, xác suất hoặc ngày dự kiến chốt ({exc}) → loại khỏi dự báo")
                continue
            if (ngay.month, ngay.year) != (thang, nam) or xs == 0.0:  # khác tháng hoặc đã thất bại
                continue
            t = theo_sales.setdefault(s, {"cam_ket": 0.0, "kha_nang": 0.0, "ky_vong": 0.0, "so": 0})
            t["ky_vong"] += gt * xs
            t["so"] += 1
            if xs >= 0.7:
                t["cam_ket"] += gt
            elif xs >= 0.3:
                t["kha_nang"] += gt
    print(f"## Dự báo doanh số tháng {thang:02d}/{nam}\n")
    print("| Sales | Số cơ hội | Cam kết (xác suất ≥ 70%) | Có khả năng (30–69%) | Kỳ vọng (Σ giá trị × xác suất) | Chỉ tiêu | Kỳ vọng / chỉ tiêu |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    tong = {"cam_ket": 0.0, "kha_nang": 0.0, "ky_vong": 0.0, "so": 0}
    for s in chi_tieu:  # sales có chỉ tiêu nhưng chưa có cơ hội trong tháng vẫn phải hiện (0) — không bỏ sót
        theo_sales.setdefault(s, {"cam_ket": 0.0, "kha_nang": 0.0, "ky_vong": 0.0, "so": 0})
    for s, t in sorted(theo_sales.items()):
        for k in tong:
            tong[k] += t[k]
        ct = chi_tieu.get(s)
        print(f"| {s} | {t['so']} | {in_tien(t['cam_ket'])} | {in_tien(t['kha_nang'])} | {in_tien(t['ky_vong'])} | "
              f"{in_tien(ct) if ct else '—'} | {in_pt(t['ky_vong'] / ct) if ct else '—'} |")
    tong_ct = sum(chi_tieu.values())
    print(f"| **Tổng** | {tong['so']} | **{in_tien(tong['cam_ket'])}** | {in_tien(tong['kha_nang'])} | **{in_tien(tong['ky_vong'])}** | "
          f"{in_tien(tong_ct) if tong_ct else '—'} | {in_pt(tong['ky_vong'] / tong_ct) if tong_ct else '—'} |")
    print("\nĐã kiểm tra phép tính (tổng = cộng từng sales).")
    print("Xác suất lấy từ giai đoạn pipeline; chỉ đáng tin khi đã thay bằng tỷ lệ thắng thật của doanh nghiệp.")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="che_do", required=True)
    h = sub.add_parser("hoa-hong"); h.add_argument("csv"); h.add_argument("--bac", required=True); h.add_argument("--tran")
    d = sub.add_parser("du-bao"); d.add_argument("csv"); d.add_argument("--thang", required=True); d.add_argument("--chi-tieu")
    a = p.parse_args(argv)
    try:
        hoa_hong(a) if a.che_do == "hoa-hong" else du_bao(a)
    except (SoKhongDoc, ValueError) as exc:
        print(f"[?] {exc}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
