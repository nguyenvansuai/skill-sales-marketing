#!/usr/bin/env python3
"""Đối soát hiệu quả marketing – bán hàng đa kênh: doanh thu thật, chi phí, ROAS/CAC thật, loại trùng.

Đầu vào là các file CSV xuất từ hệ thống (đã che SĐT còn 4 số cuối nếu cần). Mỗi dòng ra có mã nguồn:
  [Sàn]  --san     cột: ma_don, ngay, kenh (shopee/tiktok/lazada), doanh_thu, phi_san, trang_thai, ma_theo_doi
  [CRM]  --crm     cột: ma_don, ngay, kenh (inbox/zalo/web/dien-thoai…), doanh_thu, trang_thai, sdt4, chien_dich
  [POS]  --pos     cột: ma_don, ngay, doanh_thu, trang_thai           (bán tại cửa hàng/đại lý)
  [Ads]  --ads     cột: ngay, nen_tang, chien_dich, chi_phi, ket_qua_bao_cao, gia_tri_bao_cao
  [TK]   --tk      cột: ngay, so_tien, noi_dung                      (sao kê — CHỈ để đối chiếu tiền về, không cộng doanh thu)
  Chi phí khác      --chi-phi "KOC=15tr" --chi-phi "trade=20tr"
  Giá vốn           --ty-le-gia-von 44%   (hoặc cột gia_von trong từng file)

Quy tắc chống trùng / chống sót (từ phương pháp làm skill thực tế):
  1. Đơn huỷ/hoàn/thất bại bị loại khỏi doanh thu.
  2. Cùng ma_don xuất hiện ở nhiều file → đếm 1 lần (ưu tiên [Sàn] > [POS] > [CRM]); liệt kê.
  3. CRM ghi đơn chốt qua inbox nhưng khách đặt trên sàn (có ma_don sàn hoặc ghi chú "đặt sàn") → không cộng lại.
  4. Tiền sàn chuyển về tài khoản [TK] đã nằm trong [Sàn] → không cộng; sao kê chỉ dùng để kiểm tiền về.
  5. Lead/đơn CRM trùng sdt4 + ngày + doanh thu → cảnh báo trùng có thể.
  6. "Chuyển đổi" nền tảng quảng cáo tự báo ≠ đơn thật → báo cáo chênh lệch.
  7. Dữ liệu chỉ phủ một phần kỳ → cảnh báo, KHÔNG ngoại suy.

Ví dụ:
    python3 doi_soat.py --tu 01/10/2026 --den 31/10/2026 --san san.csv --crm crm.csv --ads ads.csv \
        --tk saoke.csv --ty-le-gia-von 44% --chi-phi "KOC=15tr"
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien, la_don_bi_loai  # noqa: E402

LOAI_TT = ("huy", "hủy", "huỷ", "hoan", "hoàn", "tra hang", "trả hàng", "that bai", "thất bại", "cancel", "return",
           "refund", "không nhận", "khong nhan", "bom")
UU_TIEN = {"Sàn": 0, "POS": 1, "CRM": 2}


def ngay(s):
    s = (s or "").strip()
    for f in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    raise ValueError(f"ngày không đọc được: {s!r}")


def doc(duong_dan):
    with open(duong_dan, encoding="utf-8-sig", newline="") as f:
        for i, d in enumerate(csv.DictReader(f), 2):
            row = {k.strip().lower(): (v or "").strip() for k, v in d.items() if k}
            if None in d:  # dòng có nhiều ô hơn tiêu đề: thường do số viết "1,500" không có ngoặc kép
                row["_lech_cot"] = ",".join(d[None]) or "(ô trống)"
            yield i, row


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tu", required=True); p.add_argument("--den", required=True)
    for k in ("san", "crm", "pos", "ads", "tk"):
        p.add_argument(f"--{k}")
    p.add_argument("--ty-le-gia-von")
    p.add_argument("--chi-phi", action="append", default=[])
    a = p.parse_args(argv)
    tu, den = ngay(a.tu), ngay(a.den)
    so_ngay_ky = (den - tu).days + 1
    gv_mac_dinh = doc_phan_tram(a.ty_le_gia_von) if a.ty_le_gia_von else None

    can, trung, loai = [], [], defaultdict(lambda: [0, 0.0])
    don = {}            # ma_don -> bản ghi được giữ
    ngay_co_du_lieu = defaultdict(set)
    crm_khoa = defaultdict(list)

    def them(nguon, i, d):
        try:
            nd = ngay(d.get("ngay"))
        except ValueError as exc:
            can.append(f"[{nguon}] dòng {i}: {exc} → [?], bỏ qua")
            return
        if not (tu <= nd <= den):
            return
        ngay_co_du_lieu[nguon].add(nd)
        tt = d.get("trang_thai", "").lower()
        try:
            if d.get("_lech_cot"):
                raise SoKhongDoc(f"dòng lệch cột (thừa ô: {d['_lech_cot']!r}) — có thể số có dấu phẩy không đặt trong ngoặc kép")
            dtu = doc_tien(d.get("doanh_thu"))
        except SoKhongDoc as exc:
            can.append(f"[{nguon}] dòng {i} (đơn {d.get('ma_don', '?')}): doanh thu {exc} → [?], chưa cộng")
            return
        if la_don_bi_loai(tt):
            loai[nguon][0] += 1
            loai[nguon][1] += dtu
            return
        ma = d.get("ma_don") or f"{nguon}-dong{i}"
        ghi_chu = (d.get("ghi_chu", "") + " " + d.get("kenh", "")).lower()
        if nguon == "CRM" and ("đặt sàn" in ghi_chu or "dat san" in ghi_chu):
            trung.append(f"[CRM] {ma}: ghi chú 'đặt sàn' → đơn nằm trong báo cáo sàn, không cộng lại")
            return
        try:
            gv = doc_tien(d["gia_von"]) if d.get("gia_von") else (dtu * gv_mac_dinh if gv_mac_dinh is not None else None)
            phi = doc_tien(d["phi_san"]) if d.get("phi_san") else 0.0
        except SoKhongDoc as exc:
            can.append(f"[{nguon}] đơn {ma}: giá vốn/phí {exc} → [?]")
            gv, phi = None, 0.0
        ban_ghi = {"nguon": nguon, "ma": ma, "ngay": nd, "kenh": d.get("kenh") or nguon.lower(), "dt": dtu,
                   "phi": phi, "gv": gv, "chien_dich": d.get("chien_dich") or d.get("ma_theo_doi") or ""}
        if ma in don:
            cu = don[ma]
            giu, bo_ = (ban_ghi, cu) if UU_TIEN[nguon] < UU_TIEN[cu["nguon"]] else (cu, ban_ghi)
            if not giu["chien_dich"] and bo_["chien_dich"]:
                giu["chien_dich"] = bo_["chien_dich"]
            don[ma] = giu
            trung.append(f"Đơn {ma} có ở [{cu['nguon']}] và [{nguon}] → đếm 1 lần theo [{giu['nguon']}]")
            return
        don[ma] = ban_ghi
        if nguon == "CRM" and d.get("sdt4"):
            crm_khoa[(d["sdt4"], nd, round(dtu))].append(ma)

    for nguon, f in (("Sàn", a.san), ("POS", a.pos), ("CRM", a.crm)):
        if f:
            for i, d in doc(f):
                them(nguon, i, d)
    for (s4, nd, gt), ds in crm_khoa.items():
        if len(ds) > 1:
            trung.append(f"[CRM] có thể trùng: {', '.join(ds)} cùng khách …{s4}, ngày {nd:%d/%m}, {in_tien(gt)} — kiểm tra tay (chưa tự loại)")

    # Ads
    ads = defaultdict(lambda: {"chi_phi": 0.0, "kq": 0.0, "gt": 0.0})
    if a.ads:
        for i, d in doc(a.ads):
            try:
                nd = ngay(d.get("ngay"))
                if not (tu <= nd <= den):
                    continue
                ngay_co_du_lieu["Ads"].add(nd)
                k = (d.get("nen_tang") or "?", d.get("chien_dich") or "?")
                ads[k]["chi_phi"] += doc_tien(d.get("chi_phi"))
                ads[k]["kq"] += doc_tien(d["ket_qua_bao_cao"]) if d.get("ket_qua_bao_cao") else 0
                ads[k]["gt"] += doc_tien(d["gia_tri_bao_cao"]) if d.get("gia_tri_bao_cao") else 0
            except (SoKhongDoc, ValueError) as exc:
                can.append(f"[Ads] dòng {i}: {exc} → [?], bỏ qua")
    chi_phi_khac = {}
    for x in a.chi_phi:
        k, v = x.split("=", 1)
        chi_phi_khac[k.strip()] = doc_tien(v)

    # Tổng hợp
    theo_kenh = defaultdict(lambda: {"don": 0, "dt": 0.0, "phi": 0.0, "gv": 0.0, "thieu_gv": 0})
    theo_cd = defaultdict(lambda: {"don": 0, "dt": 0.0})
    for b in don.values():
        k = theo_kenh[b["kenh"]]
        k["don"] += 1; k["dt"] += b["dt"]; k["phi"] += b["phi"]
        if b["gv"] is None:
            k["thieu_gv"] += 1
        else:
            k["gv"] += b["gv"]
        if b["chien_dich"]:
            theo_cd[b["chien_dich"]]["don"] += 1
            theo_cd[b["chien_dich"]]["dt"] += b["dt"]
    tong_dt = sum(k["dt"] for k in theo_kenh.values())
    tong_don = sum(k["don"] for k in theo_kenh.values())
    assert math.isclose(tong_dt, sum(b["dt"] for b in don.values()), abs_tol=0.5)
    tong_ads = sum(v["chi_phi"] for v in ads.values())
    tong_khac = sum(chi_phi_khac.values())
    tong_phi_san = sum(k["phi"] for k in theo_kenh.values())
    tong_gv = sum(k["gv"] for k in theo_kenh.values())
    thieu_gv = sum(k["thieu_gv"] for k in theo_kenh.values())

    print(f"## Báo cáo đối soát {a.tu} – {a.den} ({so_ngay_ky} ngày)\n")
    roas_that = tong_dt / tong_ads if tong_ads else None
    gt_bao_cao = sum(v["gt"] for v in ads.values())
    loi_nhuan = tong_dt - tong_gv - tong_phi_san - tong_ads - tong_khac if not thieu_gv else None
    kl = f"Doanh thu thật {in_tien(tong_dt)} đồng từ {tong_don} đơn (đã loại trùng, huỷ, hoàn)"
    if roas_that:
        kl += f"; ROAS thật {in_tien(roas_that, 2)}"
        if gt_bao_cao:
            kl += f" so với nền tảng tự báo {in_tien(gt_bao_cao / tong_ads, 2)}"
    if loi_nhuan is not None:
        kl += f"; lợi nhuận sau marketing {in_tien(loi_nhuan)} đồng"
    print(f"**Kết luận:** {kl}.\n")

    print("### Theo kênh\n\n| Kênh | Đơn | Doanh thu | Phí sàn | Giá vốn | Lãi gộp sau phí sàn | % doanh thu |\n|---|---:|---:|---:|---:|---:|---:|")
    for k, v in sorted(theo_kenh.items(), key=lambda x: -x[1]["dt"]):
        gv = "[?]" if v["thieu_gv"] else in_tien(v["gv"])
        lg = "[?]" if v["thieu_gv"] else in_tien(v["dt"] - v["phi"] - v["gv"])
        print(f"| {k} | {v['don']} | {in_tien(v['dt'])} | {in_tien(v['phi'])} | {gv} | {lg} | {in_pt(v['dt'] / tong_dt) if tong_dt else '—'} |")
    print(f"| **Tổng** | **{tong_don}** | **{in_tien(tong_dt)}** | {in_tien(tong_phi_san)} | {'[?]' if thieu_gv else in_tien(tong_gv)} | | 100% |")

    if ads:
        print("\n### Quảng cáo: nền tảng tự báo so với đơn thật (gắn theo tên chiến dịch)\n")
        print("| Nền tảng | Chiến dịch | Chi phí | Kết quả tự báo | Giá trị tự báo | Đơn thật | Doanh thu thật | ROAS tự báo | ROAS thật | CAC thật |")
        print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for (nt, cd), v in sorted(ads.items(), key=lambda x: -x[1]["chi_phi"]):
            th = theo_cd.get(cd, {"don": 0, "dt": 0.0})
            f2 = lambda x: in_tien(x, 2) if x is not None else "—"
            print(f"| {nt} | {cd} | {in_tien(v['chi_phi'])} | {in_tien(v['kq'])} | {in_tien(v['gt'])} | {th['don']} | {in_tien(th['dt'])} | "
                  f"{f2(v['gt'] / v['chi_phi'] if v['chi_phi'] and v['gt'] else None)} | {f2(th['dt'] / v['chi_phi'] if v['chi_phi'] else None)} | "
                  f"{in_tien(v['chi_phi'] / th['don']) if th['don'] else '—'} |")
        khong_gan = tong_dt - sum(theo_cd[cd]["dt"] for (_, cd) in ads if cd in theo_cd)
        print(f"\nDoanh thu chưa gắn được chiến dịch: {in_tien(khong_gan)} đồng (khách tự tìm, khách cũ, hoặc thiếu tên chiến dịch trong đơn).")

    print("\n### Lãi lỗ tổng\n\n| Khoản | Đồng |\n|---|---:|")
    print(f"| Doanh thu thật | {in_tien(tong_dt)} |\n| − Giá vốn | {'[?]' if thieu_gv else in_tien(tong_gv)} |\n| − Phí sàn | {in_tien(tong_phi_san)} |")
    print(f"| − Quảng cáo | {in_tien(tong_ads)} |")
    for k, v in chi_phi_khac.items():
        print(f"| − {k} | {in_tien(v)} |")
    print(f"| **= Lợi nhuận sau marketing** | **{'[?]' if loi_nhuan is None else in_tien(loi_nhuan)}** |")
    if tong_don and (tong_ads + tong_khac):
        print(f"| Chi phí marketing / đơn | {in_tien((tong_ads + tong_khac) / tong_don)} |")

    if a.tk:
        tien_ve, dong_tk = 0.0, 0
        for i, d in doc(a.tk):
            try:
                if tu <= ngay(d.get("ngay")) <= den:
                    tien_ve += doc_tien(d.get("so_tien")); dong_tk += 1
            except (SoKhongDoc, ValueError):
                can.append(f"[TK] dòng {i}: không đọc được → bỏ qua")
        print(f"\n### Đối chiếu tiền về tài khoản [TK]\n\nTổng tiền vào {in_tien(tien_ve)} đồng ({dong_tk} giao dịch). "
              "**Không cộng vào doanh thu** — tiền sàn chuyển về đã nằm trong [Sàn]; tiền COD, chuyển khoản của đơn CRM đã nằm trong [CRM]. "
              f"Chênh lệch với doanh thu đơn không qua sàn: {in_tien(tien_ve - sum(b['dt'] for b in don.values() if b['nguon'] != 'Sàn'))} đồng "
              "(gồm tiền sàn chuyển về, tiền nội bộ, tiền vay, đơn kỳ trước — xem từng dòng nếu lệch lớn).")

    print("\nĐã kiểm tra phép tính (tổng theo kênh = tổng đơn sau loại trùng).")
    for nguon, (n, gt) in loai.items():
        print(f"- [{nguon}] loại {n} đơn huỷ/hoàn, {in_tien(gt)} đồng.")
    for nguon, ngs in ngay_co_du_lieu.items():
        if len(ngs) < so_ngay_ky * 0.8:
            can.append(f"[{nguon}] chỉ có dữ liệu {len(ngs)}/{so_ngay_ky} ngày — báo cáo phản ánh phần đã có, KHÔNG ngoại suy cho cả kỳ.")
    for nguon in ("san", "crm", "ads"):
        if not getattr(a, nguon):
            can.append(f"Thiếu file --{nguon}: nếu kênh này có hoạt động trong kỳ thì báo cáo đang sót.")
    if thieu_gv:
        can.append(f"{thieu_gv} đơn thiếu giá vốn → lợi nhuận [?]. Thêm --ty-le-gia-von hoặc cột gia_von.")
    if trung:
        print("\n### Đã xử lý trùng\n" + "\n".join(f"- {t}" for t in trung))
    if can:
        print("\n### Cần anh/chị kiểm tra\n" + "\n".join(f"- {c}" for c in can))
    return 0


if __name__ == "__main__":
    sys.exit(main())
