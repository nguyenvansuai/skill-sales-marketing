#!/usr/bin/env python3
"""Đọc và in số tiền, phần trăm kiểu Việt Nam. Dùng chung cho các script trong bộ skill.

Bản gốc ở shared/scripts/vn_money.py — scripts/build.py chép vào skills/<skill>/scripts/.
Sửa ở shared, không sửa bản chép.

    >>> doc_tien("1.250.000")
    1250000.0
    >>> doc_tien("1,25tr")
    1250000.0
    >>> doc_tien("250k")
    250000.0
    >>> doc_tien("1,2 tỷ")
    1200000000.0
    >>> doc_phan_tram("12,5%")
    0.125
    >>> in_tien(1250000)
    '1.250.000'
"""
from __future__ import annotations

import re
import unicodedata

_DON_VI = {
    "k": 1e3, "nghìn": 1e3, "ngàn": 1e3, "ng": 1e3,
    "tr": 1e6, "triệu": 1e6, "m": 1e6,
    "tỷ": 1e9, "tỉ": 1e9, "ty": 1e9, "b": 1e9,
}
_DON_VI_RE = "|".join(sorted((re.escape(k) for k in _DON_VI), key=len, reverse=True))
_SO_RE = re.compile(rf"^\s*(-?[\d.,]+)\s*({_DON_VI_RE})?\s*(đ|đồng|vnd|vnđ|₫)?\s*$", re.I)


class SoKhongDoc(ValueError):
    """Ô số không đọc được — script phải đánh dấu [?], không được đoán."""


def _chuan_hoa_so(phan_so: str, co_don_vi: bool) -> float:
    s = phan_so.strip()
    if "," in s and "." in s:
        # 1.250.000,5 (kiểu VN) hoặc 1,250,000.5 (kiểu Mỹ): dấu xuất hiện sau cùng là thập phân
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        nhom = s.split(",")
        # 1,250,000 → nhóm nghìn; 1,25 → thập phân
        if len(nhom) > 2 or (len(nhom) == 2 and len(nhom[1]) == 3 and not co_don_vi):
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")
    elif "." in s:
        nhom = s.split(".")
        if len(nhom) > 2 or (len(nhom) == 2 and len(nhom[1]) == 3 and not co_don_vi):
            s = s.replace(".", "")
    return float(s)


def doc_tien(gia_tri) -> float:
    """'1.250.000' | '1,25tr' | '250k' | '1,2 tỷ' | 1250000 → float đồng. Không đọc được → SoKhongDoc."""
    if gia_tri is None:
        raise SoKhongDoc("trống")
    if isinstance(gia_tri, (int, float)):
        return float(gia_tri)
    s = str(gia_tri).strip()
    if not s or s in ("-", "?", "[?]"):
        raise SoKhongDoc(f"ô trống hoặc mờ: {gia_tri!r}")
    m = _SO_RE.match(s)
    if not m:
        raise SoKhongDoc(f"không đọc được số: {gia_tri!r}")
    don_vi = (m.group(2) or "").lower()
    try:
        so = _chuan_hoa_so(m.group(1), bool(don_vi))
    except ValueError as exc:
        raise SoKhongDoc(f"không đọc được số: {gia_tri!r}") from exc
    return so * _DON_VI.get(don_vi, 1.0)


def doc_phan_tram(gia_tri) -> float:
    """'12,5%' | '12.5' | 0.125 → 0.125. Số > 1 không có dấu % được hiểu là phần trăm."""
    if isinstance(gia_tri, (int, float)):
        so = float(gia_tri)
        return so / 100 if so > 1 else so
    s = str(gia_tri).strip().replace(" ", "")
    if not s or s in ("?", "[?]"):
        raise SoKhongDoc(f"ô trống hoặc mờ: {gia_tri!r}")
    co_dau = s.endswith("%")
    s = s.rstrip("%").replace(",", ".")
    try:
        so = float(s)
    except ValueError as exc:
        raise SoKhongDoc(f"không đọc được phần trăm: {gia_tri!r}") from exc
    return so / 100 if (co_dau or so > 1) else so


def in_tien(so: float, le: int = 0) -> str:
    """1250000 → '1.250.000'; in_tien(1234.5, 1) → '1.234,5'."""
    am = so < 0
    so = abs(so)
    chuoi = f"{so:,.{le}f}".replace(",", "§").replace(".", ",").replace("§", ".")
    return ("-" if am else "") + chuoi


def in_pt(ty_le: float, le: int = 1) -> str:
    """0.125 → '12,5%'."""
    return f"{ty_le * 100:.{le}f}%".replace(".", ",")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("vn_money: doctest OK")


# --- Trạng thái đơn ---------------------------------------------------------
# "Hoàn thành" chứa chữ "hoàn" nhưng là đơn hợp lệ → phải gỡ cụm hợp lệ trước khi dò từ khoá loại.
_TT_HOP_LE = re.compile(r"ho[aà]n\s*(th[aà]nh|t[aấ]t)|completed|delivered|th[aà]nh\s*c[oô]ng|đ[aã]\s*giao|da\s*giao", re.I)
_TT_LOAI = re.compile(r"h[uủ][yỷ]|ho[aà]n|tr[aả]\s*h[aà]ng|th[aấ]t\s*b[aạ]i|cancel|return|refund|kh[oô]ng\s*nh[aậ]n|\bbom\b", re.I)


def la_don_bi_loai(trang_thai) -> bool:
    """Đơn huỷ / hoàn / trả hàng / thất bại → True. "Hoàn thành", "Đã giao" → False.

    >>> la_don_bi_loai("Hoàn thành"), la_don_bi_loai("Đã hủy"), la_don_bi_loai("Hoàn tiền"), la_don_bi_loai("")
    (False, True, True, False)
    """
    t = unicodedata.normalize("NFC", str(trang_thai or "")).lower().strip()
    if not t:
        return False
    return bool(_TT_LOAI.search(_TT_HOP_LE.sub(" ", t)))
