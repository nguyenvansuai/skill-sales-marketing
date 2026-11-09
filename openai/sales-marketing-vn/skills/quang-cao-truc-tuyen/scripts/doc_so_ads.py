#!/usr/bin/env python3
"""Đọc số quảng cáo (Meta, TikTok, Google… xuất CSV), chẩn đoán theo phễu và phân loại theo hòa vốn.

Không dùng benchmark ngành: so từng chiến dịch với **trung vị của chính tài khoản** và với
ngưỡng hòa vốn của doanh nghiệp (từ skill gia-san-pham-khuyen-mai).

CSV cần các cột (tên cột không phân biệt hoa thường; thiếu cột nào thì chỉ số đó bỏ qua):
    chien_dich, chi_phi, hien_thi, click, ket_qua (tin nhắn/lead/đơn theo nền tảng),
    gia_tri_bao_cao (doanh thu nền tảng tự báo), don_that, doanh_thu_that (từ đối soát)

Ví dụ:
    python3 doc_so_ads.py ads.csv --roas-hoa-von 2,36 --cpl-toi-da 30000 --toi-thieu-chi-phi 1tr
"""
from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_tien, in_pt, in_tien  # noqa: E402

COT = ["chi_phi", "hien_thi", "click", "ket_qua", "gia_tri_bao_cao", "don_that", "doanh_thu_that"]


def doc_csv(duong_dan):
    hang, loi = [], []
    with open(duong_dan, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            d = {k.strip().lower(): (v or "").strip() for k, v in d.items() if k}
            h = {"chien_dich": d.get("chien_dich") or f"(dòng {i})"}
            for c in COT:
                if d.get(c, "") == "":
                    h[c] = None
                    continue
                try:
                    h[c] = doc_tien(d[c])
                except SoKhongDoc:
                    h[c] = None
                    loi.append(f"Dòng {i}, cột {c}: '{d[c]}' không đọc được → [?]")
            hang.append(h)
    return hang, loi


def chia(a, b):
    return a / b if a is not None and b else None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--roas-hoa-von", help="từ gia-san-pham-khuyen-mai")
    p.add_argument("--roas-muc-tieu")
    p.add_argument("--cpl-toi-da", help="chi phí tối đa cho 1 kết quả (tin nhắn/lead)")
    p.add_argument("--toi-thieu-chi-phi", default="0", help="chiến dịch tiêu ít hơn mức này → 'chưa đủ dữ liệu'")
    a = p.parse_args(argv)

    hang, loi = doc_csv(a.csv)
    roas_be = float(a.roas_hoa_von.replace(",", ".")) if a.roas_hoa_von else None
    roas_mt = float(a.roas_muc_tieu.replace(",", ".")) if a.roas_muc_tieu else None
    cpl_max = doc_tien(a.cpl_toi_da) if a.cpl_toi_da else None
    toi_thieu = doc_tien(a.toi_thieu_chi_phi)

    for h in hang:
        h["cpm"] = chia(h["chi_phi"], h["hien_thi"]) * 1000 if chia(h["chi_phi"], h["hien_thi"]) else None
        h["ctr"] = chia(h["click"], h["hien_thi"])
        h["cpc"] = chia(h["chi_phi"], h["click"])
        h["cpl"] = chia(h["chi_phi"], h["ket_qua"])
        h["roas_bao_cao"] = chia(h["gia_tri_bao_cao"], h["chi_phi"])
        h["roas_that"] = chia(h["doanh_thu_that"], h["chi_phi"])

    def trung_vi(k):
        v = [h[k] for h in hang if h[k] is not None]
        return statistics.median(v) if v else None

    tv = {k: trung_vi(k) for k in ("cpm", "ctr", "cpc", "cpl")}
    tong = {c: sum(h[c] or 0 for h in hang) for c in COT}

    print(f"## Đọc số quảng cáo — {len(hang)} chiến dịch, tổng chi {in_tien(tong['chi_phi'])} đồng\n")
    print("| Chiến dịch | Chi phí | CPM | CTR | CPC | Chi phí/kết quả | ROAS nền tảng báo | ROAS thật | Phân loại | Chẩn đoán |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
    dem = {}
    for h in hang:
        if (h["chi_phi"] or 0) < toi_thieu:
            loai = "Chưa đủ dữ liệu"
        else:
            roas = h["roas_that"] if h["roas_that"] is not None else None
            if roas is not None and roas_be:
                loai = ("Dưới hòa vốn — dừng/sửa" if roas < roas_be else
                        "Trên mục tiêu — tăng dần" if roas_mt and roas >= roas_mt else "Giữa — giữ, thử nghiệm")
            elif h["cpl"] is not None and cpl_max:
                loai = "Quá CPL tối đa — dừng/sửa" if h["cpl"] > cpl_max else "Trong ngưỡng CPL"
            else:
                loai = "Thiếu ngưỡng/số thật"
        dem[loai] = dem.get(loai, 0) + 1
        chan_doan = []
        if h["cpm"] and tv["cpm"] and h["cpm"] > 1.5 * tv["cpm"]:
            chan_doan.append("CPM cao: tệp hẹp/cạnh tranh — mở rộng tệp, đổi vị trí")
        if h["ctr"] is not None and tv["ctr"] and h["ctr"] < 0.67 * tv["ctr"]:
            chan_doan.append("CTR thấp: mẫu quảng cáo chưa hút — đổi hook/hình")
        if h["cpl"] and tv["cpl"] and h["cpl"] > 1.5 * tv["cpl"] and not (h["ctr"] is not None and tv["ctr"] and h["ctr"] < 0.67 * tv["ctr"]):
            chan_doan.append("Click ổn nhưng kết quả đắt: xem trang đích/kịch bản inbox")
        if h["roas_bao_cao"] and h["roas_that"] is not None and h["roas_that"] < 0.7 * h["roas_bao_cao"]:
            chan_doan.append("Nền tảng báo cao hơn thực tế >30% — đối soát lại")
        if h["ket_qua"] and h["don_that"] is not None and h["ket_qua"] > 0 and h["don_that"] / h["ket_qua"] < 0.05:
            chan_doan.append("Nhiều kết quả, ít đơn: xem tốc độ trả lời, kịch bản chốt")
        f = lambda v, k=0: in_tien(v, k) if v is not None else "—"
        print(f"| {h['chien_dich']} | {f(h['chi_phi'])} | {f(h['cpm'])} | {in_pt(h['ctr'], 2) if h['ctr'] is not None else '—'} | "
              f"{f(h['cpc'])} | {f(h['cpl'])} | {f(h['roas_bao_cao'], 2)} | {f(h['roas_that'], 2)} | {loai} | "
              f"{'; '.join(chan_doan) or '—'} |")

    print(f"\n**Tổng:** chi {in_tien(tong['chi_phi'])} · kết quả nền tảng báo {in_tien(tong['ket_qua'])} · "
          f"đơn thật {in_tien(tong['don_that'])} · doanh thu thật {in_tien(tong['doanh_thu_that'])}"
          + (f" · ROAS thật toàn tài khoản {in_tien(tong['doanh_thu_that'] / tong['chi_phi'], 2)}" if tong['chi_phi'] and tong['doanh_thu_that'] else ""))
    print("Phân loại: " + ", ".join(f"{k}: {v}" for k, v in dem.items()))
    print("\nĐã kiểm tra phép tính (tổng = cộng từng dòng). Chẩn đoán so với trung vị **của chính tài khoản**, không phải benchmark ngành.")
    can = list(loi)
    if not roas_be and not cpl_max:
        can.append("Chưa có --roas-hoa-von hoặc --cpl-toi-da → không phân loại lãi/lỗ được. Lấy từ gia-san-pham-khuyen-mai.")
    if tong["doanh_thu_that"] == 0:
        can.append("Chưa có doanh thu thật (cột doanh_thu_that) → ROAS chỉ là số nền tảng tự báo. Đối soát bằng bao-cao-doi-soat-hieu-qua.")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))
    return 0


if __name__ == "__main__":
    sys.exit(main())
