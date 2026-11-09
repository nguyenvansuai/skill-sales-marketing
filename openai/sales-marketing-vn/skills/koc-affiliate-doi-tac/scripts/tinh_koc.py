#!/usr/bin/env python3
"""So sánh và đánh giá hợp tác KOC/KOL/affiliate: số đơn hòa vốn trước khi ký, ROI sau chiến dịch.

Không dự đoán số đơn của KOC. Trước khi ký: tính số đơn cần để hòa vốn → doanh nghiệp so với
dữ liệu thật KOC cung cấp (đơn/doanh thu các lần hợp tác trước, ảnh chụp báo cáo).

CSV cột: ten, phi_co_dinh, hoa_hong (vd 10%), gia_tri_hang_tang, don_thuc_te, doanh_thu_thuc_te
(hai cột cuối để trống nếu chưa chạy).

Ví dụ:
    python3 tinh_koc.py koc.csv --aov 350000 --bien-truoc-ads 42% --thue-khau-tru 10%
    # --thue-khau-tru: tỷ lệ doanh nghiệp khấu trừ thuế TNCN khi trả cho cá nhân — HỎI KẾ TOÁN,
    #   script không mặc định tỷ lệ nào (NĐ 253/2026 [CẦN KIỂM TRA]).
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402


def o(d, k, ham, mac_dinh=None):
    v = (d.get(k) or "").strip()
    return ham(v) if v else mac_dinh


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--aov", required=True)
    p.add_argument("--bien-truoc-ads", required=True, help="từ gia-san-pham-khuyen-mai")
    p.add_argument("--thue-khau-tru", help="tỷ lệ kế toán xác nhận; bỏ trống nếu chưa biết")
    a = p.parse_args(argv)
    try:
        aov, bien = doc_tien(a.aov), doc_phan_tram(a.bien_truoc_ads)
        thue = doc_phan_tram(a.thue_khau_tru) if a.thue_khau_tru else None
    except SoKhongDoc as exc:
        print(f"[?] {exc}")
        return 2
    bien_don = aov * bien
    can, tong_cp, tong_dt = [], 0.0, 0.0
    print(f"## Đánh giá hợp tác KOC/affiliate — AOV {in_tien(aov)}, biên trước ads {in_pt(bien)} ({in_tien(bien_don)}/đơn)\n")
    print("| KOC | Phí cố định | Hoa hồng | Hàng tặng | Biên còn lại/đơn | Đơn hòa vốn | Đơn thực tế | Chi phí thực tế | Chi phí/đơn | Lãi/lỗ | Thuế khấu trừ | KOC thực nhận (phí cố định) |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            ten = d.get("ten") or f"(dòng {i})"
            try:
                phi = o(d, "phi_co_dinh", doc_tien, 0.0)
                hh = o(d, "hoa_hong", doc_phan_tram, 0.0)
                hang = o(d, "gia_tri_hang_tang", doc_tien, 0.0)
                don = o(d, "don_thuc_te", doc_tien)
                dt = o(d, "doanh_thu_thuc_te", doc_tien)
            except SoKhongDoc as exc:
                can.append(f"{ten}: {exc} → [?]")
                print(f"| {ten} | [?] |||||||||||")
                continue
            con_lai = bien_don - aov * hh
            co_dinh = phi + hang
            hoa_von = math.ceil(co_dinh / con_lai) if con_lai > 0 else None
            if con_lai <= 0:
                can.append(f"{ten}: hoa hồng {in_pt(hh)} ≥ biên trước ads → mỗi đơn đều lỗ.")
            cp_tt = cpd = ll = None
            if don is not None:
                dt_tt = dt if dt is not None else don * aov
                if dt is None:
                    can.append(f"{ten}: thiếu doanh_thu_thuc_te, tạm tính = đơn × AOV.")
                cp_tt = co_dinh + dt_tt * hh
                cpd = cp_tt / don if don else None
                ll = dt_tt * bien - cp_tt
                tong_cp += cp_tt
                tong_dt += dt_tt
            thue_tien = phi * thue if thue is not None else None
            f_ = lambda v: in_tien(v) if v is not None else "—"
            print(f"| {ten} | {f_(phi)} | {in_pt(hh)} | {f_(hang)} | {f_(con_lai)} | {hoa_von if hoa_von else 'không'} | "
                  f"{f_(don)} | {f_(cp_tt)} | {f_(cpd)} | {f_(ll)} | {f_(thue_tien) if thue is not None else '[CẦN KIỂM TRA]'} | "
                  f"{f_(phi - thue_tien) if thue_tien is not None else '—'} |")
    if tong_dt:
        print(f"\n**Tổng đã chạy:** doanh thu {in_tien(tong_dt)} · chi phí KOC {in_tien(tong_cp)} · "
              f"lãi/lỗ sau KOC {in_tien(tong_dt * bien - tong_cp)} · ROAS {in_tien(tong_dt / tong_cp, 2) if tong_cp else '—'}")
    print("\nĐã kiểm tra phép tính. 'Đơn hòa vốn' = (phí cố định + hàng tặng) / (biên trước ads − hoa hồng mỗi đơn).")
    print("So số đơn hòa vốn với **số liệu thật** KOC cung cấp từ các lần hợp tác trước (ảnh báo cáo có ngày), không dựa vào lượt theo dõi.")
    if thue is None:
        can.append("Chưa có tỷ lệ khấu trừ thuế TNCN khi trả tiền cho cá nhân — hỏi kế toán (NĐ 253/2026 [CẦN KIỂM TRA]).")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))
    return 0


if __name__ == "__main__":
    sys.exit(main())
