#!/usr/bin/env python3
"""Tạo file Excel quản lý pipeline bán hàng (CRM mini) có công thức thật — cho doanh nghiệp chưa có CRM.

Sheet: Hướng dẫn · Giai đoạn · Cơ hội · Tổng hợp · Chấm điểm lead
Công thức: xác suất theo giai đoạn (VLOOKUP), giá trị kỳ vọng, số ngày nằm ở giai đoạn, cảnh báo quá hạn,
tổng hợp theo giai đoạn và theo sales, tỷ lệ thắng. Cột "Đồng ý nhận tin" để lưu bằng chứng đồng ý (Luật 91/2025).

Ví dụ:
    python3 tao_pipeline.py --mo-hinh b2b --ra pipeline_b2b.xlsx --sales "An,Bình,Chi"
    python3 tao_pipeline.py --mo-hinh b2c --ra pipeline_inbox.xlsx
    python3 tao_pipeline.py --mo-hinh dai-ly --ra phat_trien_dai_ly.xlsx

Cần thư viện openpyxl (pip install openpyxl).
"""
from __future__ import annotations

import argparse
import sys

GIAI_DOAN = {
    "b2c": [
        ("Mới hỏi", "Khách nhắn/gọi lần đầu", "Trả lời trong thời gian cam kết; hỏi nhu cầu", 1, 0.10),
        ("Đang tư vấn", "Đã biết nhu cầu, đang so sánh", "Gửi thông tin, xử lý lo ngại", 2, 0.30),
        ("Đã báo giá", "Khách nhận giá/link đặt hàng", "Nhắc lại sau 24 giờ", 2, 0.50),
        ("Chốt đơn", "Khách xác nhận đặt, đủ địa chỉ", "Lên đơn, xác nhận lại", 1, 0.90),
        ("Đã giao", "Giao thành công", "Hỏi thăm, xin đánh giá thật", 3, 1.00),
        ("Thất bại", "Khách từ chối/không phản hồi", "Ghi lý do", 0, 0.00),
    ],
    "b2b": [
        ("Lead mới", "Có liên hệ, chưa đánh giá", "Gọi trong 24 giờ, chấm điểm lead", 2, 0.05),
        ("Đủ chuẩn", "Có nhu cầu, ngân sách, người quyết định, thời điểm", "Hẹn khảo sát/demo", 5, 0.15),
        ("Khảo sát/Demo", "Đã gặp, hiểu yêu cầu", "Gửi đề xuất", 7, 0.30),
        ("Báo giá", "Đã gửi báo giá có VAT, hiệu lực", "Theo dõi sau 3 ngày", 7, 0.50),
        ("Đàm phán", "Khách phản hồi điều kiện", "Thống nhất điều khoản", 10, 0.70),
        ("Ký hợp đồng", "Hợp đồng đã ký", "Xuất hóa đơn, triển khai", 5, 0.90),
        ("Thắng (đã thu tiền)", "Đã thanh toán", "Chăm sóc, bán thêm", 0, 1.00),
        ("Thất bại", "Mất cơ hội", "Ghi lý do, hẹn liên hệ lại", 0, 0.00),
    ],
    "dai-ly": [
        ("Tiềm năng", "Điểm bán trong danh sách mục tiêu", "Đến chào, để mẫu", 7, 0.10),
        ("Đã gặp", "Chủ điểm bán đã nghe chào", "Đề xuất gói kích hoạt", 7, 0.25),
        ("Đơn thử", "Có đơn đầu", "Trưng bày, hướng dẫn bán", 14, 0.50),
        ("Kích hoạt", "Có đơn thứ 2 trong 30 ngày", "Đưa vào tuyến thăm định kỳ", 30, 0.80),
        ("Hoạt động", "Đặt hàng đều", "Chương trình trade, thưởng", 30, 1.00),
        ("Ngưng", "Không đặt > 60 ngày", "Ghi lý do", 0, 0.00),
    ],
}
SO_DONG = 300


def tao(mo_hinh, duong_dan, sales):
    try:
        from openpyxl import Workbook
        from openpyxl.formatting.rule import FormulaRule
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
        from openpyxl.worksheet.datavalidation import DataValidation
    except ImportError:
        print("Thiếu openpyxl: chạy `pip install openpyxl` rồi thử lại.")
        return 2

    gd = GIAI_DOAN[mo_hinh]
    wb = Workbook()
    dam = Font(bold=True, color="FFFFFF")
    nen = PatternFill("solid", fgColor="1F4E78")

    def tieu_de(ws, hang, cot_rong):
        for i, (ten, rong) in enumerate(cot_rong, 1):
            c = ws.cell(row=hang, column=i, value=ten)
            c.font, c.fill = dam, nen
            c.alignment = Alignment(wrap_text=True, vertical="center")
            ws.column_dimensions[get_column_letter(i)].width = rong
        ws.freeze_panes = ws.cell(row=hang + 1, column=1)

    # Hướng dẫn
    hd = wb.active
    hd.title = "Hướng dẫn"
    for i, dong in enumerate([
        f"PIPELINE BÁN HÀNG — mô hình {mo_hinh.upper()}",
        "1. Sheet 'Giai đoạn': sửa tiêu chí, SLA (số ngày tối đa ở mỗi giai đoạn) và XÁC SUẤT cho đúng thực tế.",
        "   Xác suất đang là mặc định để công thức chạy — thay bằng tỷ lệ thật sau 2–3 tháng (số thắng / số đi qua giai đoạn).",
        "2. Sheet 'Cơ hội': mỗi khách/cơ hội một dòng. Chọn Giai đoạn từ danh sách. Cập nhật 'Ngày cập nhật' mỗi khi đổi giai đoạn.",
        "3. SĐT chỉ ghi 4 số cuối nếu file chia sẻ nhiều người. Cột 'Đồng ý nhận tin': ghi ngày + kênh khách đồng ý (Luật 91/2025).",
        "4. Không gửi tin quảng cáo cho người chưa đồng ý (NĐ 91/2020). Không mua danh sách khách hàng.",
        "5. Sheet 'Tổng hợp' tự tính; không sửa công thức.",
        "Tạo bởi bộ skill skill-sales-marketing (Sự AI) — github.com/nguyenvansuai/skill-sales-marketing",
    ], 1):
        hd.cell(row=i, column=1, value=dong)
    hd.column_dimensions["A"].width = 120
    hd["A1"].font = Font(bold=True, size=14)

    # Giai đoạn
    g = wb.create_sheet("Giai đoạn")
    tieu_de(g, 1, [("Giai đoạn", 22), ("Tiêu chí vào giai đoạn", 40), ("Việc phải làm", 40), ("SLA (ngày tối đa)", 12), ("Xác suất thắng", 12)])
    for r, (ten, tc, viec, sla, xs) in enumerate(gd, 2):
        for c, v in enumerate((ten, tc, viec, sla, xs), 1):
            g.cell(row=r, column=c, value=v)
        g.cell(row=r, column=5).number_format = "0%"
    cuoi_gd = len(gd) + 1
    pham_vi_gd = f"'Giai đoạn'!$A$2:$E${cuoi_gd}"

    # Cơ hội
    ch = wb.create_sheet("Cơ hội")
    cot = [("ID", 7), ("Ngày tạo", 12), ("Khách / Công ty", 26), ("SĐT (4 số cuối)", 12), ("Nguồn", 14),
           ("Chiến dịch", 22), ("Sales", 12), ("Giai đoạn", 18), ("Giá trị (đồng)", 15), ("Xác suất", 9),
           ("Giá trị kỳ vọng", 15), ("Ngày cập nhật", 12), ("Số ngày ở giai đoạn", 10), ("Cảnh báo", 12),
           ("Đồng ý nhận tin (ngày, kênh)", 22), ("Lý do thất bại", 22), ("Ghi chú", 30)]
    tieu_de(ch, 1, cot)
    for r in range(2, SO_DONG + 2):
        ch.cell(row=r, column=1, value=f'=IF(C{r}="","",ROW()-1)')
        ch.cell(row=r, column=10, value=f'=IF(H{r}="","",IFERROR(VLOOKUP(H{r},{pham_vi_gd},5,FALSE),""))')
        ch.cell(row=r, column=11, value=f'=IF(OR(I{r}="",J{r}=""),"",I{r}*J{r})')
        ch.cell(row=r, column=13, value=f'=IF(L{r}="","",TODAY()-L{r})')
        ch.cell(row=r, column=14, value=f'=IF(OR(M{r}="",H{r}=""),"",IF(AND(VLOOKUP(H{r},{pham_vi_gd},4,FALSE)>0,M{r}>VLOOKUP(H{r},{pham_vi_gd},4,FALSE)),"QUÁ HẠN",""))')
        for c in (2, 12):
            ch.cell(row=r, column=c).number_format = "dd/mm/yyyy"
        for c in (9, 11):
            ch.cell(row=r, column=c).number_format = "#,##0"
        ch.cell(row=r, column=10).number_format = "0%"
    dv = DataValidation(type="list", formula1=f"='Giai đoạn'!$A$2:$A${cuoi_gd}", allow_blank=True)
    ch.add_data_validation(dv)
    dv.add(f"H2:H{SO_DONG + 1}")
    if sales:
        dvs = DataValidation(type="list", formula1='"' + ",".join(sales) + '"', allow_blank=True)
        ch.add_data_validation(dvs)
        dvs.add(f"G2:G{SO_DONG + 1}")
    ch.conditional_formatting.add(f"N2:N{SO_DONG + 1}", FormulaRule(formula=[f'N2="QUÁ HẠN"'], fill=PatternFill("solid", fgColor="F8CBAD")))

    # Tổng hợp
    th = wb.create_sheet("Tổng hợp")
    tieu_de(th, 1, [("Giai đoạn", 22), ("Số cơ hội", 10), ("Tổng giá trị", 16), ("Giá trị kỳ vọng", 16), ("Quá hạn", 10)])
    rng = f"'Cơ hội'!$H$2:$H${SO_DONG + 1}"
    for r, (ten, *_rest) in enumerate(gd, 2):
        th.cell(row=r, column=1, value=ten)
        th.cell(row=r, column=2, value=f'=COUNTIF({rng},A{r})')
        th.cell(row=r, column=3, value=f"=SUMIF({rng},A{r},'Cơ hội'!$I$2:$I${SO_DONG + 1})")
        th.cell(row=r, column=4, value=f"=SUMIF({rng},A{r},'Cơ hội'!$K$2:$K${SO_DONG + 1})")
        th.cell(row=r, column=5, value=f"=COUNTIFS({rng},A{r},'Cơ hội'!$N$2:$N${SO_DONG + 1},\"QUÁ HẠN\")")
        for c in (3, 4):
            th.cell(row=r, column=c).number_format = "#,##0"
    r = len(gd) + 2
    th.cell(row=r, column=1, value="TỔNG").font = Font(bold=True)
    for c, L in ((2, "B"), (3, "C"), (4, "D"), (5, "E")):
        th.cell(row=r, column=c, value=f"=SUM({L}2:{L}{r - 1})").number_format = "#,##0"
    thang, thua = gd[-2][0], gd[-1][0]
    th.cell(row=r + 2, column=1, value="Tỷ lệ thắng (thắng / (thắng + thất bại))")
    th.cell(row=r + 2, column=2, value=f'=IFERROR(COUNTIF({rng},"{thang}")/(COUNTIF({rng},"{thang}")+COUNTIF({rng},"{thua}")),"")').number_format = "0%"
    if sales:
        th.cell(row=r + 4, column=1, value="Theo sales").font = Font(bold=True)
        for i, s in enumerate(sales, r + 5):
            th.cell(row=i, column=1, value=s)
            th.cell(row=i, column=2, value=f"=COUNTIF('Cơ hội'!$G$2:$G${SO_DONG + 1},A{i})")
            th.cell(row=i, column=4, value=f"=SUMIF('Cơ hội'!$G$2:$G${SO_DONG + 1},A{i},'Cơ hội'!$K$2:$K${SO_DONG + 1})").number_format = "#,##0"
            th.cell(row=i, column=5, value=f"=COUNTIFS('Cơ hội'!$G$2:$G${SO_DONG + 1},A{i},'Cơ hội'!$N$2:$N${SO_DONG + 1},\"QUÁ HẠN\")")

    # Chấm điểm lead
    cd = wb.create_sheet("Chấm điểm lead")
    tieu_de(cd, 1, [("Tiêu chí", 40), ("Trọng số", 10), ("Điểm (0–3)", 10), ("Điểm × trọng số", 14)])
    tieu_chi = [("Có nhu cầu rõ ràng (vấn đề cụ thể)", 3), ("Có ngân sách / khả năng chi trả", 3),
                ("Đang nói chuyện với người quyết định", 2), ("Thời điểm mua ≤ 3 tháng", 2),
                ("Đúng khách hàng mục tiêu (ngành, quy mô, khu vực)", 2), ("Có tương tác chủ động (hỏi giá, xin demo)", 1)]
    for r, (tc, ts) in enumerate(tieu_chi, 2):
        cd.cell(row=r, column=1, value=tc)
        cd.cell(row=r, column=2, value=ts)
        cd.cell(row=r, column=4, value=f"=IF(C{r}=\"\",\"\",B{r}*C{r})")
    r = len(tieu_chi) + 2
    cd.cell(row=r, column=1, value="Tổng điểm (tối đa = 3 × tổng trọng số)").font = Font(bold=True)
    cd.cell(row=r, column=4, value=f"=SUM(D2:D{r - 1})")
    cd.cell(row=r + 1, column=1, value="Xếp loại")
    cd.cell(row=r + 1, column=4, value=f'=IF(D{r}="","",IF(D{r}>=0.7*3*SUM(B2:B{r - 1}),"Nóng — gọi trong ngày",IF(D{r}>=0.4*3*SUM(B2:B{r - 1}),"Ấm — nuôi dưỡng","Lạnh — để chăm sóc tự động")))')
    cd.cell(row=r + 3, column=1, value="Trọng số và ngưỡng 70%/40% là mặc định — chỉnh theo tỷ lệ chốt thật của doanh nghiệp.")

    wb.save(duong_dan)
    print(f"Đã tạo {duong_dan}: {len(gd)} giai đoạn, {SO_DONG} dòng cơ hội có công thức, tổng hợp theo giai đoạn"
          + (f" và {len(sales)} sales" if sales else "") + ".")
    print("Xác suất từng giai đoạn là mặc định để công thức chạy — thay bằng tỷ lệ thật sau 2–3 tháng.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mo-hinh", choices=sorted(GIAI_DOAN), required=True)
    p.add_argument("--ra", required=True, help="đường dẫn file .xlsx")
    p.add_argument("--sales", help="danh sách tên sales, cách nhau dấu phẩy")
    a = p.parse_args(argv)
    sales = [s.strip() for s in a.sales.split(",")] if a.sales else []
    return tao(a.mo_hinh, a.ra, sales)


if __name__ == "__main__":
    sys.exit(main())
