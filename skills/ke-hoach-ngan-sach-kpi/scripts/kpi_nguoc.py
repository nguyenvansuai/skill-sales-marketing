#!/usr/bin/env python3
"""Tính ngược từ doanh thu mục tiêu ra phễu, ngân sách, KPI — 3 mô hình: b2c, b2b, dai-ly.

Tỷ lệ chuyển đổi và chi phí phải là SỐ LIỆU THẬT của doanh nghiệp. Script không chứa benchmark.
Kịch bản xấu/tốt là độ nhạy ±N% quanh số thật (mặc định 20%), ghi rõ là giả định.

Ví dụ:
    # B2C online: doanh thu 300 triệu/tháng trong 3 tháng, tháng 3 là mùa cao điểm
    python3 kpi_nguoc.py --mo-hinh b2c --doanh-thu 900tr --so-thang 3 --he-so-mua-vu 1,1,1.5 \
        --aov 350000 --ty-le-chot 12% --chi-phi-lead 25000 --doanh-thu-khach-cu 20% \
        --bien-truoc-ads 42% --so-ngay-du-lieu 60

    # B2B
    python3 kpi_nguoc.py --mo-hinh b2b --doanh-thu 2ty --so-thang 6 --gia-tri-hop-dong 80tr \
        --ty-le-thang 25% --ty-le-lead-co-hoi 30% --ty-le-hoat-dong-lead 5% --so-sales 3 --chu-ky-ngay 45

    # Đại lý / điểm bán
    python3 kpi_nguoc.py --mo-hinh dai-ly --doanh-thu 1,2ty --so-thang 3 --dt-moi-diem 8tr \
        --so-diem-hien-co 30 --ty-le-roi-bo 5% --chi-phi-trade-moi-diem 400000 --chi-phi-mo-diem 1,5tr
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402


def chia_thang(tong, he_so):
    s = sum(he_so)
    phan = [tong * h / s for h in he_so]
    assert math.isclose(sum(phan), tong, rel_tol=1e-9), "chia tháng không khớp tổng"
    return phan


def la_dem(k):
    # Chỉ số đếm được (đơn, lead, hợp đồng, điểm bán…) → làm tròn LÊN thành số nguyên.
    return k.startswith(("Số ", "Điểm "))


def dem(v):
    return in_tien(math.ceil(v - 1e-9)) if v is not None else "—"


def b2c(dt, a, nhan):
    aov = doc_tien(a.aov)
    chot = doc_phan_tram(a.ty_le_chot) * nhan["ty_le"]
    cpl = doc_tien(a.chi_phi_lead) * nhan["chi_phi"]
    khach_cu = doc_phan_tram(a.doanh_thu_khach_cu) if a.doanh_thu_khach_cu else 0.0
    dt_moi = dt * (1 - khach_cu)
    don = dt_moi / aov
    lead = don / chot
    ngan_sach = lead * cpl
    kq = {"Doanh thu từ khách mới": dt_moi, "Số đơn mới cần": don, "Số tin nhắn/lead cần": lead,
          "Ngân sách quảng cáo": ngan_sach, "CAC (chi phí/đơn mới)": ngan_sach / don,
          "ROAS kế hoạch (DT mới/ngân sách)": dt_moi / ngan_sach}
    if a.bien_truoc_ads:
        cpa_be = aov * doc_phan_tram(a.bien_truoc_ads)
        kq["CPA hòa vốn (từ biên trước ads)"] = cpa_be
        kq["_lo"] = ngan_sach / don > cpa_be
    return kq


def b2b(dt, a, nhan):
    gt = doc_tien(a.gia_tri_hop_dong)
    thang = doc_phan_tram(a.ty_le_thang) * nhan["ty_le"]
    l2c = doc_phan_tram(a.ty_le_lead_co_hoi) * nhan["ty_le"]
    hd = dt / gt
    co_hoi = hd / thang
    lead = co_hoi / l2c
    kq = {"Số hợp đồng cần": hd, "Số cơ hội (đã đánh giá) cần": co_hoi, "Số lead cần": lead}
    if a.ty_le_hoat_dong_lead:
        hd_lead = doc_phan_tram(a.ty_le_hoat_dong_lead) * nhan["ty_le"]
        kq["Số hoạt động tiếp cận (gọi/email/gặp) cần"] = lead / hd_lead
    if a.chi_phi_lead:
        kq["Ngân sách tạo lead"] = lead * doc_tien(a.chi_phi_lead) * nhan["chi_phi"]
    return kq


def dai_ly(dt, a, nhan, so_thang):
    dt_diem = doc_tien(a.dt_moi_diem) * nhan["ty_le"]
    hien_co = int(a.so_diem_hien_co or 0)
    roi_bo = doc_phan_tram(a.ty_le_roi_bo) if a.ty_le_roi_bo else 0.0
    diem_tb_can = dt / so_thang / dt_diem
    mat_di = hien_co * roi_bo * so_thang
    mo_moi = max(0.0, diem_tb_can - hien_co + mat_di)
    kq = {"Số điểm bán hoạt động bình quân cần": diem_tb_can, "Điểm dự kiến rời bỏ trong kỳ": mat_di,
          "Số điểm cần mở mới": mo_moi}
    if a.chi_phi_trade_moi_diem:
        kq["Ngân sách trade (duy trì)"] = diem_tb_can * so_thang * doc_tien(a.chi_phi_trade_moi_diem) * nhan["chi_phi"]
    if a.chi_phi_mo_diem:
        kq["Ngân sách mở điểm mới"] = mo_moi * doc_tien(a.chi_phi_mo_diem) * nhan["chi_phi"]
    return kq


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mo-hinh", required=True, choices=["b2c", "b2b", "dai-ly"])
    p.add_argument("--doanh-thu", required=True, help="tổng doanh thu mục tiêu của cả kỳ")
    p.add_argument("--so-thang", type=int, default=1)
    p.add_argument("--he-so-mua-vu", help="trọng số từng tháng, vd 1,1,1.5")
    p.add_argument("--do-nhay", type=float, default=20, help="%% cho kịch bản xấu/tốt (mặc định 20)")
    p.add_argument("--so-ngay-du-lieu", type=int, help="số ngày dữ liệu dùng để tính tỷ lệ")
    # b2c
    p.add_argument("--aov"); p.add_argument("--ty-le-chot"); p.add_argument("--chi-phi-lead")
    p.add_argument("--doanh-thu-khach-cu", help="TỶ LỆ %% doanh thu đến từ khách cũ (không cần quảng cáo), vd 20%%")
    p.add_argument("--bien-truoc-ads", help="biên đóng góp trước ads %% (từ gia-san-pham-khuyen-mai)")
    # b2b
    p.add_argument("--gia-tri-hop-dong"); p.add_argument("--ty-le-thang"); p.add_argument("--ty-le-lead-co-hoi")
    p.add_argument("--ty-le-hoat-dong-lead"); p.add_argument("--so-sales", type=int); p.add_argument("--chu-ky-ngay", type=int)
    # đại lý
    p.add_argument("--dt-moi-diem"); p.add_argument("--so-diem-hien-co"); p.add_argument("--ty-le-roi-bo")
    p.add_argument("--chi-phi-trade-moi-diem"); p.add_argument("--chi-phi-mo-diem")
    a = p.parse_args(argv)

    can = []
    bat_buoc = {"b2c": ["aov", "ty_le_chot", "chi_phi_lead"], "b2b": ["gia_tri_hop_dong", "ty_le_thang", "ty_le_lead_co_hoi"],
                "dai-ly": ["dt_moi_diem"]}[a.mo_hinh]
    thieu = [k for k in bat_buoc if not getattr(a, k)]
    if thieu:
        print("[CẦN BỔ SUNG] Thiếu số liệu thật: " + ", ".join("--" + k.replace("_", "-") for k in thieu)
              + ". Script không dùng số trung bình ngành. Lấy từ báo cáo inbox/CRM/sàn 1–3 tháng gần nhất.")
        return 2
    try:
        dt = doc_tien(a.doanh_thu)
        # hệ số cách nhau bằng dấu phẩy, phần thập phân dùng dấu chấm: 1,1,1.5
        he_so = [float(x) for x in a.he_so_mua_vu.split(",")] if a.he_so_mua_vu else [1.0] * a.so_thang
    except (SoKhongDoc, ValueError) as exc:
        if isinstance(exc, ZeroDivisionError):
            print("[?] Có tham số bằng 0 (giá trị đơn, tỷ lệ chốt, doanh thu/điểm…) — kiểm tra lại số liệu đầu vào.")
        else:
            print(f"[?] {exc}")
        return 2
    if len(he_so) != a.so_thang:
        print(f"[?] --he-so-mua-vu có {len(he_so)} giá trị, khác --so-thang {a.so_thang}.")
        return 2
    if a.so_ngay_du_lieu is not None and a.so_ngay_du_lieu < 28:
        can.append(f"Tỷ lệ chuyển đổi tính từ {a.so_ngay_du_lieu} ngày dữ liệu — quá ngắn để lập kế hoạch {a.so_thang} tháng. Thu thêm dữ liệu hoặc coi kết quả là thử nghiệm.")

    n = a.do_nhay / 100
    kb = {"Xấu (giả định)": {"ty_le": 1 - n, "chi_phi": 1 + n}, "Cơ sở (số thật)": {"ty_le": 1, "chi_phi": 1},
          "Tốt (giả định)": {"ty_le": 1 + n, "chi_phi": 1 - n}}
    try:
        ket_qua = {}
        for ten, nhan in kb.items():
            if a.mo_hinh == "b2c":
                ket_qua[ten] = b2c(dt, a, nhan)
            elif a.mo_hinh == "b2b":
                ket_qua[ten] = b2b(dt, a, nhan)
            else:
                ket_qua[ten] = dai_ly(dt, a, nhan, a.so_thang)
    except (SoKhongDoc, ZeroDivisionError) as exc:
        if isinstance(exc, ZeroDivisionError):
            print("[?] Có tham số bằng 0 (giá trị đơn, tỷ lệ chốt, doanh thu/điểm…) — kiểm tra lại số liệu đầu vào.")
        else:
            print(f"[?] {exc}")
        return 2

    co_so = ket_qua["Cơ sở (số thật)"]
    ten_mh = {"b2c": "B2C", "b2b": "B2B", "dai-ly": "ĐẠI LÝ / ĐIỂM BÁN"}[a.mo_hinh]
    print(f"## Tính KPI ngược — mô hình {ten_mh}, doanh thu {in_tien(dt)} đồng / {a.so_thang} tháng\n")
    if a.mo_hinh == "b2c":
        ket_luan = (f"Cần khoảng {dem(co_so['Số tin nhắn/lead cần'])} tin nhắn/lead và ngân sách "
                    f"{in_tien(co_so['Ngân sách quảng cáo'])} đồng (kịch bản cơ sở).")
        if co_so.get("_lo"):
            ket_luan += " **CẢNH BÁO: CAC kế hoạch cao hơn CPA hòa vốn — kế hoạch này lỗ trên mỗi đơn mới.**"
    elif a.mo_hinh == "b2b":
        ket_luan = f"Cần {dem(co_so['Số lead cần'])} lead → {dem(co_so['Số cơ hội (đã đánh giá) cần'])} cơ hội → {dem(co_so['Số hợp đồng cần'])} hợp đồng."
    else:
        ket_luan = f"Cần bình quân {dem(co_so['Số điểm bán hoạt động bình quân cần'])} điểm bán hoạt động; mở mới {dem(co_so['Số điểm cần mở mới'])} điểm."
    print(f"**Kết luận:** {ket_luan}\n")

    chi_so = [k for k in co_so if not k.startswith("_")]
    print("| Chỉ số | " + " | ".join(kb) + " |")
    print("|---|" + "---:|" * len(kb))
    for k in chi_so:
        vals = []
        for ten in kb:
            v = ket_qua[ten].get(k)
            vals.append(dem(v) if la_dem(k) else in_tien(v, 2) if "ROAS" in k else in_tien(v, 1) if v is not None and v < 100 and "Ngân sách" not in k else in_tien(v))
        print(f"| {k} | " + " | ".join(vals) + " |")

    # Chia tháng cho kịch bản cơ sở
    print("\n### Chia theo tháng (kịch bản cơ sở, theo hệ số mùa vụ)\n")
    cot = ["Doanh thu"] + [k for k in chi_so if any(x in k for x in ("Ngân sách", "Số đơn", "lead", "hợp đồng", "hoạt động tiếp cận"))]
    print("| Tháng | Hệ số | " + " | ".join(cot) + " |")
    print("|---|---:|" + "---:|" * len(cot))
    dt_thang = chia_thang(dt, he_so)
    for i, (h, d_t) in enumerate(zip(he_so, dt_thang), 1):
        ty = d_t / dt
        hang = [in_tien(d_t)] + [dem(co_so[k] * ty) if la_dem(k) else in_tien(co_so[k] * ty) for k in cot[1:]]
        print(f"| {i} | {str(h).replace('.', ',')} | " + " | ".join(hang) + " |")

    if a.mo_hinh == "b2b":
        if a.so_sales and "Số hoạt động tiếp cận (gọi/email/gặp) cần" in co_so:
            tuan = a.so_thang * 52 / 12
            print(f"\nMỗi sales cần ~{in_tien(co_so['Số hoạt động tiếp cận (gọi/email/gặp) cần'] / a.so_sales / tuan, 1)} hoạt động tiếp cận/tuần "
                  f"và ~{in_tien(co_so['Số lead cần'] / a.so_sales / tuan, 1)} lead/tuần ({a.so_sales} sales, {in_tien(tuan, 1)} tuần).")
        if a.chu_ky_ngay:
            can.append(f"Chu kỳ bán {a.chu_ky_ngay} ngày: lead của {a.chu_ky_ngay} ngày cuối kỳ khó kịp thành hợp đồng trong kỳ — dồn tạo lead vào đầu kỳ.")

    print("\nSố đếm được (đơn, lead, hợp đồng, điểm bán) làm tròn lên từng ô — tổng các tháng có thể lớn hơn số của cả kỳ; dùng số cả kỳ làm chỉ tiêu tổng.")
    print("\nĐã kiểm tra phép tính (tổng các tháng = doanh thu mục tiêu).")
    print(f"Kịch bản Xấu/Tốt = tỷ lệ chuyển đổi ∓{a.do_nhay:g}% và chi phí ±{a.do_nhay:g}% quanh số thật — **giả định độ nhạy, không phải số trung bình ngành**.")
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))
    return 0


if __name__ == "__main__":
    sys.exit(main())
