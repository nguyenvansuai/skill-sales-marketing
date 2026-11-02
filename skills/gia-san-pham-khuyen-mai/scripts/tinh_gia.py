#!/usr/bin/env python3
"""P&L từng đơn, giá hòa vốn, ROAS/CPA hòa vốn, mức giảm tối đa còn lãi, giá đại lý theo bậc.

Mỗi loại phí là một biến có tên. Script không chứa tỷ lệ phí của bất kỳ sàn nào — phí lấy từ
Seller Center / file đối soát của chính shop, ghi ngày kiểm bằng --ngay-kiem-phi.

Ví dụ:
    python3 tinh_gia.py --gia-ban 250000 --gia-von 110000 \
        --phi "hoa hồng sàn=8%" --phi "thanh toán=3%" --phi "trợ giá ship=5000" \
        --ty-le-hoan 4% --chi-phi-moi-don-hoan 35000 --ads-moi-don 20000 \
        --loi-nhuan-muc-tieu 10% --giam 30% --ngay-kiem-phi 02/11/2026

    python3 tinh_gia.py --gia-ban 250000 --gia-von 110000 --bac-chiet-khau 10,15,20,25
    python3 tinh_gia.py --csv san_pham.csv          # cột: sku,gia_ban,gia_von,phi,ty_le_hoan,chi_phi_moi_don_hoan,ads_moi_don
                                                    # cột phi: "hoa hồng=8%;thanh toán=3%;ship=5000"

Công thức (khớp minhnv0807/ai-business-skills skill 76, MIT):
    Biên đóng góp trước ads = Giá bán thực nhận − Giá vốn − Σ phí % × giá − Σ phí cố định − Chi phí hoàn kỳ vọng
    ROAS hòa vốn = 1 / (biên đóng góp trước ads %)      CPA hòa vốn = biên đóng góp trước ads (đồng)
    Giá hòa vốn  = (giá vốn + phí cố định + chi phí hoàn [+ ads]) / (1 − Σ phí %)
    Giá cho biên mục tiêu m = (giá vốn + phí cố định + chi phí hoàn + ads) / (1 − Σ phí % − m)
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vn_money import SoKhongDoc, doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402

TRAN_GIAM_GIA = 0.50  # Điều 7 NĐ 81/2018 (sau NĐ 128/2024) — xem references/phap-ly-marketing-vn.md mục 3.1


def doc_phi(chuoi_phi):
    """['hoa hồng=8%', 'ship=5000'] → (dict % , dict cố định)."""
    pt, co_dinh = {}, {}
    for muc in chuoi_phi:
        for phan in str(muc).split(";"):
            phan = phan.strip()
            if not phan:
                continue
            if "=" not in phan:
                raise SoKhongDoc(f"phí phải có dạng tên=giá trị: {phan!r}")
            ten, gt = (x.strip() for x in phan.split("=", 1))
            if gt.endswith("%"):
                pt[ten] = doc_phan_tram(gt)
            else:
                co_dinh[ten] = doc_tien(gt)
    return pt, co_dinh


def tinh(gia_ban, gia_von, phi_pt, phi_cd, ty_le_hoan=0.0, chi_phi_hoan=0.0, ads=0.0):
    tong_pt = sum(phi_pt.values())
    tien_phi_pt = {k: v * gia_ban for k, v in phi_pt.items()}
    hoan = ty_le_hoan * chi_phi_hoan
    bien = gia_ban - gia_von - sum(tien_phi_pt.values()) - sum(phi_cd.values()) - hoan
    bien_pt = bien / gia_ban if gia_ban else float("nan")
    loi_nhuan = bien - ads
    kq = {
        "gia_ban": gia_ban, "gia_von": gia_von, "phi_pt": tien_phi_pt, "phi_co_dinh": dict(phi_cd),
        "chi_phi_hoan_ky_vong": hoan, "bien_truoc_ads": bien, "bien_truoc_ads_pt": bien_pt,
        "ads_moi_don": ads, "loi_nhuan_sau_ads": loi_nhuan,
        "loi_nhuan_sau_ads_pt": loi_nhuan / gia_ban if gia_ban else float("nan"),
        "roas_hoa_von": (1 / bien_pt) if bien_pt > 0 else None,
        "cpa_hoa_von": bien if bien > 0 else None,
        "tong_phi_pt": tong_pt,
    }
    mau = 1 - tong_pt
    kq["gia_hoa_von_truoc_ads"] = (gia_von + sum(phi_cd.values()) + hoan) / mau if mau > 0 else None
    kq["gia_hoa_von_sau_ads"] = (gia_von + sum(phi_cd.values()) + hoan + ads) / mau if mau > 0 else None
    # Kiểm tra lại phép tính bằng cách cộng ngược
    tong = gia_von + sum(tien_phi_pt.values()) + sum(phi_cd.values()) + hoan + bien
    assert math.isclose(tong, gia_ban, rel_tol=1e-9, abs_tol=1e-6), "phép tính P&L không khớp"
    return kq


def gia_cho_bien(gia_von, phi_pt, phi_cd, hoan, ads, m):
    mau = 1 - sum(phi_pt.values()) - m
    return (gia_von + sum(phi_cd.values()) + hoan + ads) / mau if mau > 0 else None


def bang_pl(kq, tieu_de):
    d = [f"### {tieu_de}", "", "| Khoản | Đồng | % giá bán |", "|---|---:|---:|"]
    g = kq["gia_ban"]
    d.append(f"| Giá bán thực nhận | {in_tien(g)} | 100,0% |")
    d.append(f"| − Giá vốn | {in_tien(kq['gia_von'])} | {in_pt(kq['gia_von'] / g)} |")
    for ten, tien in kq["phi_pt"].items():
        d.append(f"| − Phí: {ten} | {in_tien(tien)} | {in_pt(tien / g)} |")
    for ten, tien in kq["phi_co_dinh"].items():
        d.append(f"| − Phí: {ten} (cố định) | {in_tien(tien)} | {in_pt(tien / g)} |")
    if kq["chi_phi_hoan_ky_vong"]:
        d.append(f"| − Chi phí hoàn kỳ vọng | {in_tien(kq['chi_phi_hoan_ky_vong'])} | {in_pt(kq['chi_phi_hoan_ky_vong'] / g)} |")
    d.append(f"| **= Biên đóng góp trước ads** | **{in_tien(kq['bien_truoc_ads'])}** | **{in_pt(kq['bien_truoc_ads_pt'])}** |")
    if kq["ads_moi_don"]:
        d.append(f"| − Chi phí quảng cáo/đơn | {in_tien(kq['ads_moi_don'])} | {in_pt(kq['ads_moi_don'] / g)} |")
        d.append(f"| **= Lợi nhuận sau ads** | **{in_tien(kq['loi_nhuan_sau_ads'])}** | **{in_pt(kq['loi_nhuan_sau_ads_pt'])}** |")
    return d


def bao_cao(a):
    gia_ban, gia_von = doc_tien(a.gia_ban), doc_tien(a.gia_von)
    phi_pt, phi_cd = doc_phi(a.phi or [])
    ty_le_hoan = doc_phan_tram(a.ty_le_hoan) if a.ty_le_hoan else 0.0
    chi_phi_hoan = doc_tien(a.chi_phi_moi_don_hoan) if a.chi_phi_moi_don_hoan else 0.0
    ads = doc_tien(a.ads_moi_don) if a.ads_moi_don else 0.0
    canh_bao = []
    if not phi_pt and not phi_cd:
        canh_bao.append("Chưa nhập phí kênh bán nào — nếu bán trên sàn, lấy phí từ Seller Center/file đối soát [CẦN BỔ SUNG].")
    elif not a.ngay_kiem_phi:
        canh_bao.append("Thiếu --ngay-kiem-phi: phí sàn đổi thường xuyên, ghi ngày lấy số phí.")
    if ty_le_hoan and not chi_phi_hoan:
        canh_bao.append("Có tỷ lệ hoàn nhưng thiếu --chi-phi-moi-don-hoan (ship 2 chiều + hàng hỏng) → chi phí hoàn đang tính = 0 [CẦN BỔ SUNG].")

    kq = tinh(gia_ban, gia_von, phi_pt, phi_cd, ty_le_hoan, chi_phi_hoan, ads)
    d = ["## Kết quả tính giá", ""]
    if kq["bien_truoc_ads"] <= 0:
        d.append(f"**Kết luận:** mỗi đơn đang **lỗ {in_tien(-kq['bien_truoc_ads'])} đồng trước cả quảng cáo** — không nên chạy ads cho sản phẩm này ở giá hiện tại.")
    elif ads and kq["loi_nhuan_sau_ads"] <= 0:
        d.append(f"**Kết luận:** lãi trước ads {in_tien(kq['bien_truoc_ads'])} đồng/đơn nhưng **lỗ {in_tien(-kq['loi_nhuan_sau_ads'])} đồng sau ads**; cần CPA dưới {in_tien(kq['cpa_hoa_von'])} đồng.")
    else:
        d.append(f"**Kết luận:** biên đóng góp trước ads {in_pt(kq['bien_truoc_ads_pt'])} ({in_tien(kq['bien_truoc_ads'])} đồng/đơn); ROAS hòa vốn {in_tien(kq['roas_hoa_von'], 2)}.")
    d.append("")
    d += bang_pl(kq, "P&L một đơn")
    d += ["", "### Chỉ số hòa vốn", "", "| Chỉ số | Giá trị |", "|---|---:|"]
    if kq["roas_hoa_von"]:
        d.append(f"| ROAS hòa vốn (doanh thu/chi phí ads) | {in_tien(kq['roas_hoa_von'], 2)} |")
        d.append(f"| CPA hòa vốn (chi phí ads tối đa/đơn) | {in_tien(kq['cpa_hoa_von'])} |")
    if kq["gia_hoa_von_truoc_ads"]:
        d.append(f"| Giá bán hòa vốn (chưa tính ads) | {in_tien(kq['gia_hoa_von_truoc_ads'])} |")
    if ads and kq["gia_hoa_von_sau_ads"]:
        d.append(f"| Giá bán hòa vốn (đã tính ads/đơn) | {in_tien(kq['gia_hoa_von_sau_ads'])} |")
    if a.loi_nhuan_muc_tieu:
        m = doc_phan_tram(a.loi_nhuan_muc_tieu)
        g = gia_cho_bien(gia_von, phi_pt, phi_cd, kq["chi_phi_hoan_ky_vong"], ads, m)
        if g:
            d.append(f"| Giá bán để lãi ròng {in_pt(m)} sau ads | {in_tien(g)} |")
        if kq["bien_truoc_ads_pt"] - m > 0:
            d.append(f"| ROAS mục tiêu để giữ lãi {in_pt(m)} | {in_tien(1 / (kq['bien_truoc_ads_pt'] - m), 2)} |")
        else:
            d.append(f"| ROAS mục tiêu để giữ lãi {in_pt(m)} | không đạt được ở giá hiện tại |")

    # Mức giảm giá
    if kq["gia_hoa_von_truoc_ads"]:
        d_max = 1 - kq["gia_hoa_von_truoc_ads"] / gia_ban
        d += ["", "### Giảm giá", ""]
        if d_max <= 0:
            d.append("- Không còn dư địa giảm giá: giá hiện tại đã dưới giá hòa vốn.")
        else:
            d.append(f"- Mức giảm tối đa còn hòa vốn (chưa tính ads): **{in_pt(d_max)}** (giá sau giảm {in_tien(kq['gia_hoa_von_truoc_ads'])}).")
            if ads and kq["gia_hoa_von_sau_ads"]:
                d_max2 = 1 - kq["gia_hoa_von_sau_ads"] / gia_ban
                d.append(f"- Mức giảm tối đa còn hòa vốn (đã tính ads): **{in_pt(max(d_max2, 0))}**.")
        if a.giam:
            giam = doc_phan_tram(a.giam)
            kq2 = tinh(gia_ban * (1 - giam), gia_von, phi_pt, phi_cd, ty_le_hoan, chi_phi_hoan, ads)
            d.append("")
            d += bang_pl(kq2, f"P&L khi giảm {in_pt(giam)}")
            if giam > TRAN_GIAM_GIA:
                canh_bao.append(f"Mức giảm {in_pt(giam)} vượt trần 50% (Điều 7 NĐ 81/2018 sau NĐ 128/2024) — chỉ hợp lệ trong khuyến mại tập trung hoặc ngoại lệ. Chạy scripts/kiem_khuyen_mai.py.")

    if a.bac_chiet_khau:
        d += ["", "### Giá đại lý theo bậc chiết khấu (trên giá bán lẻ khuyến nghị)", "",
              "| Bậc | Chiết khấu | Giá đại lý | Lãi gộp của mình/đơn vị | % trên giá đại lý |", "|---|---:|---:|---:|---:|"]
        for i, ck in enumerate(a.bac_chiet_khau.split(","), 1):
            ck = doc_phan_tram(ck.strip() + ("" if "%" in ck else "%"))
            gia_dl = gia_ban * (1 - ck)
            lai = gia_dl - gia_von
            d.append(f"| {i} | {in_pt(ck)} | {in_tien(gia_dl)} | {in_tien(lai)} | {in_pt(lai / gia_dl) if gia_dl else '-'} |")
            if lai <= 0:
                canh_bao.append(f"Bậc {i} (chiết khấu {in_pt(ck)}) bán dưới giá vốn.")

    d += ["", "Đã kiểm tra phép tính (cộng ngược các khoản = giá bán)."]
    if a.ngay_kiem_phi:
        d.append(f"Phí kênh bán lấy ngày {a.ngay_kiem_phi}.")
    if canh_bao:
        d += ["", "### Cần anh/chị kiểm tra", ""] + [f"- {c}" for c in canh_bao]
    return "\n".join(d), kq


def chay_csv(duong_dan):
    ra = ["## P&L theo sản phẩm", "", "| SKU | Giá bán | Giá vốn | Biên trước ads | % | ROAS hòa vốn | CPA hòa vốn | Lãi sau ads | Ghi chú |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    with open(duong_dan, encoding="utf-8-sig", newline="") as f:
        for dong in csv.DictReader(f):
            sku = dong.get("sku", "?")
            try:
                phi_pt, phi_cd = doc_phi([dong.get("phi", "")])
                kq = tinh(doc_tien(dong["gia_ban"]), doc_tien(dong["gia_von"]), phi_pt, phi_cd,
                          doc_phan_tram(dong["ty_le_hoan"]) if dong.get("ty_le_hoan") else 0.0,
                          doc_tien(dong["chi_phi_moi_don_hoan"]) if dong.get("chi_phi_moi_don_hoan") else 0.0,
                          doc_tien(dong["ads_moi_don"]) if dong.get("ads_moi_don") else 0.0)
            except (SoKhongDoc, KeyError, ValueError) as exc:
                ra.append(f"| {sku} | [?] | [?] | | | | | | {exc} |")
                continue
            ghi_chu = "LỖ trước ads" if kq["bien_truoc_ads"] <= 0 else ("lỗ sau ads" if kq["loi_nhuan_sau_ads"] < 0 else "")
            roas = f"{in_tien(kq['roas_hoa_von'], 2)}" if kq["roas_hoa_von"] else "—"
            cpa = in_tien(kq["cpa_hoa_von"]) if kq["cpa_hoa_von"] else "—"
            ra.append(f"| {sku} | {in_tien(kq['gia_ban'])} | {in_tien(kq['gia_von'])} | {in_tien(kq['bien_truoc_ads'])} | "
                      f"{in_pt(kq['bien_truoc_ads_pt'])} | {roas} | {cpa} | {in_tien(kq['loi_nhuan_sau_ads'])} | {ghi_chu} |")
    ra += ["", "Đã kiểm tra phép tính (mỗi dòng cộng ngược = giá bán). Ô [?] là dữ liệu không đọc được — cần anh/chị bổ sung."]
    return "\n".join(ra)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--gia-ban")
    p.add_argument("--gia-von")
    p.add_argument("--phi", action="append", help='"tên=8%%" hoặc "tên=5000"; lặp lại được')
    p.add_argument("--ty-le-hoan")
    p.add_argument("--chi-phi-moi-don-hoan")
    p.add_argument("--ads-moi-don")
    p.add_argument("--loi-nhuan-muc-tieu", help="lãi ròng mong muốn sau ads, vd 10%%")
    p.add_argument("--giam", help="mức giảm giá muốn thử, vd 30%%")
    p.add_argument("--bac-chiet-khau", help="vd 10,15,20")
    p.add_argument("--ngay-kiem-phi")
    p.add_argument("--csv")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if a.csv:
        print(chay_csv(a.csv))
        return 0
    if not (a.gia_ban and a.gia_von):
        p.error("cần --gia-ban và --gia-von (hoặc --csv)")
    try:
        van_ban, kq = bao_cao(a)
    except SoKhongDoc as exc:
        print(f"[?] Không đọc được số liệu: {exc}. Anh/chị kiểm tra lại, script không tự đoán.")
        return 2
    print(json.dumps(kq, ensure_ascii=False, indent=2) if a.json else van_ban)
    return 0


if __name__ == "__main__":
    sys.exit(main())
