#!/usr/bin/env python3
"""Đồng bộ tài liệu dùng chung, sinh bản ChatGPT, marketplace và đóng gói zip.

Chạy từ thư mục gốc repo:  python3 scripts/build.py

1. Chép shared/*.md vào skills/<skill>/references/ và shared/scripts/vn_money.py
   vào skills/<skill>/scripts/ (nếu skill có script) — mỗi skill tự đủ, cài riêng được.
2. Sinh chatgpt/<skill>.md (dán vào Custom GPT / Project).
3. Sinh .claude-plugin/marketplace.json (cài bằng /plugin trong Claude Code).
4. Kiểm tra: name khớp thư mục, độ dài description, file nhắc trong SKILL.md tồn tại.
5. Đóng gói dist/<skill>.zip (upload claude.ai) và dist/tat-ca-skill.zip.
"""
import json
import re
import shutil
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SKILLS = GOC / "skills"
SHARED = GOC / "shared"
SHARED_MD = ["nguyen-tac-chung.md", "phap-ly-marketing-vn.md"]
SHARED_PY = ["vn_money.py"]
GIOI_HAN_GPT = 8000
MO_TA_BO = ("Bộ 17 skill AI Sales – Marketing cho doanh nghiệp, hộ kinh doanh Việt Nam (B2C, B2B, online, offline) "
            "theo pháp luật 2026: hồ sơ doanh nghiệp, nghiên cứu thị trường, giá – khuyến mại, KPI – ngân sách, nội dung, "
            "kiểm tra pháp lý quảng cáo, PR, quảng cáo trực tuyến, SEO, trade marketing, KOC – affiliate, pipeline CRM, "
            "báo giá B2B, kịch bản tư vấn, quản lý đội sales, giữ chân khách, đối soát hiệu quả.")


def ds_skill():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def dong_bo():
    for sk in ds_skill():
        ref = sk / "references"
        ref.mkdir(exist_ok=True)
        for f in SHARED_MD:
            shutil.copy(SHARED / f, ref)
        sc = sk / "scripts"
        if sc.exists():
            for f in SHARED_PY:
                shutil.copy(SHARED / "scripts" / f, sc)
            shutil.rmtree(sc / "__pycache__", ignore_errors=True)


def tach_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    meta = {k: v.strip().strip('"') for k, v in meta.items()}
    return meta, m.group(2).strip()


def sinh_chatgpt():
    out = GOC / "chatgpt"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    canh_bao = []
    for sk in ds_skill():
        meta, body = tach_frontmatter((sk / "SKILL.md").read_text(encoding="utf-8"))
        body = body.replace("references/", "file Knowledge ").replace("scripts/", "")
        hd = ("Bạn là trợ lý Sales – Marketing cho doanh nghiệp, hộ kinh doanh Việt Nam. Luôn trả lời bằng tiếng Việt có dấu.\n"
              "Các file nhắc tới (nguyen-tac-chung.md, phap-ly-marketing-vn.md, ...) đã được tải lên mục Knowledge; đọc khi cần.\n\n" + body)
        files = sorted(f.name for f in (sk / "references").glob("*.md"))
        scripts = sorted(f.name for f in (sk / "scripts").glob("*.py")) if (sk / "scripts").exists() else []
        nd = [f"# {sk.name} – bản dùng cho ChatGPT", "", f"**Mô tả:** {meta.get('description', '')}", "",
              "## Cách cài",
              "1. ChatGPT miễn phí: tạo Project mới, mở phần hướng dẫn (instructions). Bản trả phí: có thể tạo Custom GPT (Explore GPTs → Create → Configure).",
              f"2. Name: `{sk.name}`. Description: copy dòng Mô tả ở trên.",
              "3. Dán toàn bộ khối **Instructions** bên dưới vào ô hướng dẫn.",
              "4. Tải lên (Project files hoặc Knowledge) các file " + ", ".join(f"`skills/{sk.name}/references/{f}`" for f in files) + "."]
        if scripts:
            nd.append("5. Bật **Code Interpreter & Data Analysis** và tải thêm " + ", ".join(f"`skills/{sk.name}/scripts/{s}`" for s in scripts) + ".")
        nd += ["", "## Instructions", "", "````markdown", hd, "````", ""]
        (out / f"{sk.name}.md").write_text("\n".join(nd), encoding="utf-8")
        if len(hd) > GIOI_HAN_GPT:
            canh_bao.append(f"  ! {sk.name}: Instructions {len(hd)} ký tự > {GIOI_HAN_GPT}")
    return canh_bao


def sinh_marketplace():
    plugins = []
    for sk in ds_skill():
        meta, _ = tach_frontmatter((sk / "SKILL.md").read_text(encoding="utf-8"))
        plugins.append({"name": sk.name, "source": f"./skills/{sk.name}",
                        "description": meta["description"], "category": "sales-marketing"})
    plugins.append({"name": "tron-bo-skill-sales-marketing", "source": "./",
                    "description": "Cài cả bộ 17 skill Sales – Marketing Việt Nam trong một lần.", "category": "sales-marketing"})
    data = {"name": "skill-sales-marketing", "description": MO_TA_BO,
            "owner": {"name": "nguyenvansuai", "url": "https://github.com/nguyenvansuai"}, "plugins": plugins}
    out = GOC / ".claude-plugin"
    out.mkdir(exist_ok=True)
    (out / "marketplace.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def kiem_tra():
    loi = []
    for sk in ds_skill():
        meta, body = tach_frontmatter((sk / "SKILL.md").read_text(encoding="utf-8"))
        if meta.get("name") != sk.name:
            loi.append(f"{sk.name}: name trong frontmatter không khớp tên thư mục")
        d = meta.get("description", "")
        if not 50 < len(d) <= 1024:
            loi.append(f"{sk.name}: description dài {len(d)} ký tự (cần 51–1024)")
        if len(re.findall(r'["“]', d)) < 8:
            loi.append(f"{sk.name}: description nên có ≥ 4 câu người dùng hay nói (trong ngoặc kép)")
        for ref in re.findall(r"`((?:references|scripts)/[\w./-]+)`", body):
            if not (sk / ref).exists():
                loi.append(f"{sk.name}: thiếu file {ref}")
        for cu in ("181/2013", "13/2023/NĐ-CP", "Điều 7 NĐ 81", "Điều 6 NĐ 81", "Đ7 NĐ 81"):
            for f in [sk / "SKILL.md", *(sk / "references").glob("*.md")]:
                if f.name == "phap-ly-marketing-vn.md":
                    continue
                if cu in f.read_text(encoding="utf-8"):
                    loi.append(f"{sk.name}: {f.name} viện dẫn văn bản đã hết hiệu lực {cu}")
    return loi


def dong_goi():
    dist = GOC / "dist"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    with zipfile.ZipFile(dist / "tat-ca-skill.zip", "w", zipfile.ZIP_DEFLATED) as tat_ca:
        for sk in ds_skill():
            with zipfile.ZipFile(dist / f"{sk.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
                for f in sorted(sk.rglob("*")):
                    if f.is_file() and "__pycache__" not in f.parts:
                        z.write(f, f.relative_to(SKILLS))
                        tat_ca.write(f, f.relative_to(SKILLS))


if __name__ == "__main__":
    import sys as _sys
    _sys.path.insert(0, str(GOC / "scripts"))
    import ket_noi
    ket_noi.chuan_bi()
    dong_bo()
    cb = sinh_chatgpt()
    sinh_marketplace()
    loi = kiem_tra() + ket_noi.kiem_tra()
    dong_goi()
    ket_noi.hoan_tat()  # mcpServers cho skill lẻ + dist/<plugin>.plugin (sau dong_goi vì dong_goi xóa dist/)
    import subprocess
    subprocess.run([_sys.executable, str(GOC / "scripts" / "build_openai.py")], check=True)
    print(f"Đã build {len(ds_skill())} skill.")
    for c in cb:
        print(c)
    if loi:
        print("LỖI:\n" + "\n".join("  - " + l for l in loi))
        raise SystemExit(1)
