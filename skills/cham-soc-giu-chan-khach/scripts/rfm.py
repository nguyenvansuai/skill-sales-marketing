#!/usr/bin/env python3
"""Chia nhóm khách theo RFM (lần mua gần nhất – số lần mua – tổng tiền) từ file đơn hàng.

Chấm 1–3 theo phân vị của chính dữ liệu doanh nghiệp (không dùng ngưỡng ngành).
CSV cột: ma_khach (mã hoặc 4 số cuối SĐT — không cần SĐT đầy đủ), ngay (dd/mm/yyyy), gia_tri, trang_thai
Đơn trạng thái huỷ/hoàn bị loại.

Ví dụ:
    python3 rfm.py don_hang.csv --ngay-tinh 02/11/2026
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_tien, in_pt, in_tien, la_don_bi_loai  # noqa: E402

LOAI = ("huy", "hủy", "huỷ", "hoan", "hoàn", "tra hang", "trả hàng", "cancel", "return")


def diem(v, moc, dao=False):
    s = 1 if v <= moc[0] else 2 if v <= moc[1] else 3
    return 4 - s if dao else s


def phan_vi(ds):
    ds = sorted(ds)
    return ds[len(ds) // 3], ds[2 * len(ds) // 3]


def nhom(r, f, m):
    if r == 3 and f >= 2 and m >= 2:
        return "Trung thành"
    if r == 3 and f == 1:
        return "Mới mua"
    if r == 1 and f >= 2:
        return "Có nguy cơ rời"
    if r == 1:
        return "Đã rời"
    return "Cần nuôi dưỡng"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--ngay-tinh", default=dt.date.today().strftime("%d/%m/%Y"))
    a = p.parse_args(argv)
    ngay_tinh = dt.datetime.strptime(a.ngay_tinh, "%d/%m/%Y").date()
    kh, can, bo = {}, [], 0
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            if la_don_bi_loai(d.get("trang_thai")):
                bo += 1
                continue
            try:
                ma = (d.get("ma_khach") or "").strip()
                if not ma:
                    raise ValueError("thiếu mã khách")
                ngay = dt.datetime.strptime(d["ngay"].strip(), "%d/%m/%Y").date()
                gt = doc_tien(d.get("gia_tri"))
            except (SoKhongDoc, ValueError, KeyError) as exc:
                can.append(f"Dòng {i}: {exc} → [?], bỏ qua")
                continue
            k = kh.setdefault(ma, {"gan_nhat": ngay, "so_lan": 0, "tong": 0.0})
            k["gan_nhat"] = max(k["gan_nhat"], ngay)
            k["so_lan"] += 1
            k["tong"] += gt
    if not kh:
        print("Không có dữ liệu hợp lệ.")
        return 2
    for k in kh.values():
        k["r_ngay"] = (ngay_tinh - k["gan_nhat"]).days
    mr, mf, mm = phan_vi([k["r_ngay"] for k in kh.values()]), phan_vi([k["so_lan"] for k in kh.values()]), phan_vi([k["tong"] for k in kh.values()])
    tk = {}
    for ma, k in kh.items():
        r, f_, m = diem(k["r_ngay"], mr, dao=True), diem(k["so_lan"], mf), diem(k["tong"], mm)
        n = nhom(r, f_, m)
        t = tk.setdefault(n, {"so": 0, "tien": 0.0, "ngay": 0})
        t["so"] += 1
        t["tien"] += k["tong"]
        t["ngay"] += k["r_ngay"]
    tong_kh, tong_tien = len(kh), sum(k["tong"] for k in kh.values())
    assert sum(t["so"] for t in tk.values()) == tong_kh
    print(f"## Nhóm khách RFM — {tong_kh} khách, tính đến {a.ngay_tinh}\n")
    print("| Nhóm | Số khách | % khách | Tổng tiền | % doanh thu | Số ngày từ lần mua gần nhất (TB) |\n|---|---:|---:|---:|---:|---:|")
    for n in ("Trung thành", "Mới mua", "Cần nuôi dưỡng", "Có nguy cơ rời", "Đã rời"):
        if n in tk:
            t = tk[n]
            print(f"| {n} | {t['so']} | {in_pt(t['so'] / tong_kh, 0)} | {in_tien(t['tien'])} | {in_pt(t['tien'] / tong_tien, 0)} | {in_tien(t['ngay'] / t['so'])} |")
    print(f"\nĐã kiểm tra phép tính (tổng số khách các nhóm = {tong_kh}). Đã loại {bo} đơn huỷ/hoàn.")
    print("Ngưỡng R/F/M là phân vị 1/3 và 2/3 của chính dữ liệu này.")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))
    return 0


if __name__ == "__main__":
    sys.exit(main())
