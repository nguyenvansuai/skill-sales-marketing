#!/usr/bin/env python3
"""Tạo báo giá B2B (Markdown) từ bảng hàng hóa: thành tiền, chiết khấu, thuế GTGT từng dòng, tổng, số tiền bằng chữ.

Thuế suất GTGT phải ghi cho TỪNG dòng (cột thue_suat). Script không mặc định thuế suất vì:
thuế suất phổ thông 10%, chính sách giảm còn 8% áp dụng cho một số hàng hóa, dịch vụ đến hết 2026
và có danh mục loại trừ [THỨ CẤP] — kế toán xác định. Hộ kinh doanh không kê khai GTGT khấu trừ:
dùng --khong-vat (giá đã bao gồm thuế, không tách VAT).

CSV cột: ten_hang, dvt, so_luong, don_gia, thue_suat (vd 8% / 10% / KCT), ghi_chu
Ví dụ:
    python3 tao_bao_gia.py hang.csv --ben-ban "Công ty TNHH ABC" --khach "Công ty CP XYZ" \
        --nguoi-nhan "anh Minh — Trưởng phòng Mua hàng" --hieu-luc 15 --ngay 02/11/2026 \
        --chiet-khau 5% --thanh-toan "50% khi ký, 50% khi giao" --giao-hang "Trong 7 ngày làm việc"
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402

SO = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def _ba_so(n, day_du):
    tram, chuc, dv = n // 100, (n // 10) % 10, n % 10
    ra = []
    if day_du or tram:
        ra.append(f"{SO[tram]} trăm")
    if chuc == 0:
        if dv and (day_du or tram):
            ra.append("lẻ")
    elif chuc == 1:
        ra.append("mười")
    else:
        ra.append(f"{SO[chuc]} mươi")
    if dv:
        if dv == 1 and chuc >= 2:
            ra.append("mốt")
        elif dv == 5 and chuc >= 1:
            ra.append("lăm")
        elif dv == 4 and chuc >= 2:
            ra.append("tư")
        else:
            ra.append(SO[dv])
    return " ".join(ra)


def doc_so(n: int) -> str:
    """Đọc số nguyên thành chữ.

    >>> doc_so(1250000)
    'Một triệu hai trăm năm mươi nghìn đồng'
    >>> doc_so(1005000)
    'Một triệu không trăm lẻ năm nghìn đồng'
    >>> doc_so(2000000021)
    'Hai tỷ không trăm hai mươi mốt đồng'
    """
    if n == 0:
        return "Không đồng"
    ten = ["", "nghìn", "triệu", "tỷ", "nghìn tỷ", "triệu tỷ"]
    nhom = []
    while n > 0:
        nhom.append(n % 1000)
        n //= 1000
    ra = []
    for i in range(len(nhom) - 1, -1, -1):
        if nhom[i] == 0:
            continue
        chu = _ba_so(nhom[i], day_du=(i != len(nhom) - 1))
        ra.append(f"{chu} {ten[i]}".strip())
    s = " ".join(ra)
    return s[0].upper() + s[1:] + " đồng"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--ben-ban", default="[CẦN BỔ SUNG: tên bên bán, MST, địa chỉ]")
    p.add_argument("--khach", default="[CẦN BỔ SUNG: tên khách hàng]")
    p.add_argument("--nguoi-nhan", default="")
    p.add_argument("--ngay", default=dt.date.today().strftime("%d/%m/%Y"))
    p.add_argument("--hieu-luc", type=int, required=True, help="số ngày báo giá có hiệu lực")
    p.add_argument("--chiet-khau", help="chiết khấu thương mại trên tổng trước thuế, vd 5%%")
    p.add_argument("--khong-vat", action="store_true", help="hộ kinh doanh/không tách VAT: giá đã gồm thuế")
    p.add_argument("--thanh-toan", default="[CẦN BỔ SUNG]")
    p.add_argument("--giao-hang", default="[CẦN BỔ SUNG]")
    a = p.parse_args(argv)

    dong, can = [], []
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            try:
                sl, dg = doc_tien(d.get("so_luong")), doc_tien(d.get("don_gia"))
            except SoKhongDoc as exc:
                can.append(f"Dòng {i} ({d.get('ten_hang', '?')}): {exc} → [?]")
                continue
            ts_raw = (d.get("thue_suat") or "").strip()
            if a.khong_vat:
                ts = None
            elif ts_raw.upper() in ("KCT", "KHÔNG CHỊU THUẾ", "0%", "0"):
                ts = 0.0 if ts_raw.upper() not in ("KCT", "KHÔNG CHỊU THUẾ") else "KCT"
            elif ts_raw:
                ts = doc_phan_tram(ts_raw)
            else:
                ts = "?"
                can.append(f"Dòng {i} ({d.get('ten_hang')}): thiếu thuế suất GTGT — hỏi kế toán (10% / 8% / 5% / 0% / KCT).")
            dong.append({"ten": d.get("ten_hang", ""), "dvt": d.get("dvt", ""), "sl": sl, "dg": dg, "ts": ts,
                         "tt": sl * dg, "gc": d.get("ghi_chu", "")})

    ck = doc_phan_tram(a.chiet_khau) if a.chiet_khau else 0.0
    tong_truoc = sum(x["tt"] for x in dong)
    tien_ck = tong_truoc * ck
    thue = 0.0
    for x in dong:
        x["sau_ck"] = x["tt"] * (1 - ck)
        x["thue"] = x["sau_ck"] * x["ts"] if isinstance(x["ts"], float) else 0.0
        thue += x["thue"]
    tong = tong_truoc - tien_ck + thue
    assert math.isclose(sum(x["sau_ck"] for x in dong) + thue, tong, abs_tol=1)
    het_han = (dt.datetime.strptime(a.ngay, "%d/%m/%Y") + dt.timedelta(days=a.hieu_luc)).strftime("%d/%m/%Y")

    print(f"# BÁO GIÁ\n\nNgày: {a.ngay} · Có hiệu lực đến hết ngày **{het_han}** ({a.hieu_luc} ngày)\n")
    print(f"**Bên báo giá:** {a.ben_ban}  \n**Kính gửi:** {a.khach}" + (f" — {a.nguoi_nhan}" if a.nguoi_nhan else "") + "\n")
    print("| STT | Hàng hóa, dịch vụ | ĐVT | Số lượng | Đơn giá | Thành tiền | Thuế suất GTGT | Tiền thuế | Ghi chú |")
    print("|---:|---|---|---:|---:|---:|---:|---:|---|")
    for i, x in enumerate(dong, 1):
        ts = "Giá đã gồm thuế" if a.khong_vat else ("KCT" if x["ts"] == "KCT" else "[?]" if x["ts"] == "?" else in_pt(x["ts"], 0))
        print(f"| {i} | {x['ten']} | {x['dvt']} | {in_tien(x['sl'])} | {in_tien(x['dg'])} | {in_tien(x['tt'])} | {ts} | "
              f"{'' if a.khong_vat else in_tien(x['thue'])} | {x['gc']} |")
    print(f"\n| | Số tiền (đồng) |\n|---|---:|\n| Cộng tiền hàng | {in_tien(tong_truoc)} |")
    if ck:
        print(f"| Chiết khấu thương mại {in_pt(ck)} | -{in_tien(tien_ck)} |")
    if not a.khong_vat:
        print(f"| Tiền thuế GTGT | {in_tien(thue)} |")
    print(f"| **Tổng thanh toán** | **{in_tien(tong)}** |")
    print(f"\nBằng chữ: *{doc_so(round(tong))}*.\n")
    print(f"**Điều kiện thanh toán:** {a.thanh_toan}  \n**Giao hàng:** {a.giao_hang}  \n"
          f"**Giá trên {'đã bao gồm thuế (bên bán không tách thuế GTGT)' if a.khong_vat else 'đã tách thuế GTGT theo từng dòng'}.**\n")
    print("Trân trọng,  \n[Tên, chức danh, SĐT người báo giá]\n")
    print("---\nĐã kiểm tra phép tính (thành tiền, chiết khấu, thuế, tổng).")
    if any(x["ts"] == 0.08 for x in dong):
        can.append("Có dòng thuế suất 8%: xác nhận hàng hóa/dịch vụ thuộc diện giảm thuế GTGT và thời hạn áp dụng [THỨ CẤP] với kế toán.")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))
    return 0


if __name__ == "__main__":
    sys.exit(main())
