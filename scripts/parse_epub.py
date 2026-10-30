#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析带注古籍 EPUB 源，提取正文与注疏，生成结构化 JSON。

数据源：
  ancient-books/unpacked/shiji-master/OEBPS/Text/*.htm       史记（三家注）
  ancient-books/unpacked/zizhitongjian-master/OEBPS/Text/*.html  资治通鉴（胡三省注）

输出：
  data/texts/shiji/chapters_anno.json
  data/texts/zizhitongjian/chapters.json

段落结构：
  {
    "title": 篇名, "juan": 卷次, "section": 体例,
    "paras": [ { "text": 正文(含 <sup data-n="k"> 标记), "notes": [ {"tag":..,"text":..} ] }, ... ]
  }
"""
import os
import re
import json
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_SHJI = os.path.join(ROOT, "..", "ancient-books", "unpacked", "shiji-master", "OEBPS", "Text")
SRC_ZZTJ = os.path.join(ROOT, "..", "ancient-books", "unpacked", "zizhitongjian-master", "OEBPS", "Text")
OUT_DIR = os.path.join(ROOT, "data", "texts")

CN_DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9}


def cn2num(s):
    """中文数字转阿拉伯数字，支持 一 到 一百三十 的常见写法。"""
    s = s.strip()
    if not s:
        return 0
    total = 0
    section = 0
    number = 0
    for ch in s:
        if ch in CN_DIGITS:
            number = CN_DIGITS[ch]
        elif ch == "十":
            section += (number if number else 1) * 10
            number = 0
        elif ch == "百":
            section += (number if number else 1) * 100
            number = 0
        else:
            continue
    total = section + number
    return total


def shiji_section(juan):
    """按卷次判定史记五体。"""
    if 1 <= juan <= 12:
        return "本纪"
    if 13 <= juan <= 22:
        return "表"
    if 23 <= juan <= 30:
        return "书"
    if 31 <= juan <= 60:
        return "世家"
    if 61 <= juan <= 130:
        return "列传"
    return "其他"


NOTE_TAGS = ["集解", "索隱", "索隐", "正義", "正义", "考證", "考证"]


def split_notes(raw):
    """把 〔集解〕..〔索隱〕..〔正義〕.. 形式拆成 (tag, text) 列表。"""
    raw = raw.strip()
    if not raw:
        return []
    pattern = "〔(" + "|".join(NOTE_TAGS) + ")〕"
    parts = re.split(pattern, raw)
    out = []
    # parts[0] 一般是首个标记前的内容，可能为空
    if parts and parts[0].strip():
        out.append(("注", parts[0].strip()))
    i = 1
    while i + 1 < len(parts):
        tag = parts[i].strip()
        text = parts[i + 1].strip()
        if tag in ("索隐",):
            tag = "索隱"
        if tag in ("正义",):
            tag = "正義"
        if tag in ("考证",):
            tag = "考證"
        if text:
            out.append((tag, text))
        i += 2
    return out


def clean_text(s):
    s = s.replace("\u3000", "").strip()
    return s


def parse_shiji_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "lxml")

    h1 = soup.find("h1")
    full_title = clean_text(h1.get_text()) if h1 else ""
    m = re.search(r"卷([一二三四五六七八九十百零〇]+)", full_title)
    juan = cn2num(m.group(1)) if m else 0
    piece = full_title.split("・")[-1] if "・" in full_title else full_title
    piece = re.sub(r"^卷[一二三四五六七八九十百零〇]+・?", "", piece)

    paras = []
    for p in soup.find_all("p"):
        for a in p.find_all("a"):
            a.decompose()
        notes = []
        for sp in p.find_all("span", class_="style7"):
            raw = sp.get_text()
            pairs = split_notes(raw)
            if not pairs:
                sp.decompose()
                continue
            first = len(notes)
            notes.extend({"tag": t, "text": x} for t, x in pairs)
            marker = "".join("⟦%d⟧" % (first + k) for k in range(len(pairs)))
            sp.replace_with(marker)
        for sp in p.find_all("span"):
            sp.unwrap()
        text = clean_text(p.get_text())
        if not text and not notes:
            continue
        paras.append({"text": text, "notes": notes})

    return {
        "title": piece,
        "juan": "卷%s" % (m.group(1) if m else str(juan)),
        "juan_num": juan,
        "section": shiji_section(juan),
        "paras": paras,
    }


def write_split(chapters, book_key):
    """按篇拆分：index.json 存目录，ch/NNNN.json 存正文。"""
    out_dir = os.path.join(OUT_DIR, book_key)
    ch_dir = os.path.join(out_dir, "ch")
    os.makedirs(ch_dir, exist_ok=True)
    index = []
    for i, ch in enumerate(chapters, start=1):
        item = {
            "id": i,
            "title": ch["title"],
            "juan": ch["juan"],
            "juan_num": ch["juan_num"],
            "section": ch["section"],
        }
        index.append(item)
        with open(os.path.join(ch_dir, "%04d.json" % i), "w", encoding="utf-8") as f:
            json.dump(ch, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(out_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    return index


def parse_shiji():
    files = sorted(f for f in os.listdir(SRC_SHJI) if f.endswith(".htm"))
    chapters = []
    for fn in files:
        ch = parse_shiji_file(os.path.join(SRC_SHJI, fn))
        if not ch["paras"]:
            continue
        chapters.append(ch)
    write_split(chapters, "shiji")
    total_note = sum(sum(len(p["notes"]) for p in c["paras"]) for c in chapters)
    print("史记：%d 篇，注疏 %d 条" % (len(chapters), total_note))
    return chapters


def parse_zztj_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "lxml")

    t = soup.find("title")
    full_title = clean_text(t.get_text()) if t else ""
    full_title = re.sub(r"^資治通鑑-?", "", full_title).strip()
    m = re.search(r"卷([一二三四五六七八九十百零〇]+)", full_title)
    juan = cn2num(m.group(1)) if m else 0

    paras = []
    for p in soup.find_all("p"):
        for a in p.find_all("a"):
            a.decompose()
        notes = []
        for sp in p.find_all("span", class_="jiazhu"):
            raw = sp.get_text()
            raw = re.sub(r"\s+", "", raw).strip()
            if not raw:
                sp.decompose()
                continue
            marker = "⟦%d⟧" % len(notes)
            notes.append({"tag": "胡注", "text": raw})
            sp.replace_with(marker)
        for sp in p.find_all("span"):
            sp.unwrap()
        text = clean_text(p.get_text())
        if not text and not notes:
            continue
        paras.append({"text": text, "notes": notes})

    return {
        "title": full_title,
        "juan": "卷%s" % (m.group(1) if m else str(juan)),
        "juan_num": juan,
        "section": "编年",
        "paras": paras,
    }


def parse_zztj():
    files = sorted((f for f in os.listdir(SRC_ZZTJ) if f.endswith(".html")),
                   key=lambda x: int(re.sub(r"\D", "", x) or 0))
    chapters = []
    for fn in files:
        ch = parse_zztj_file(os.path.join(SRC_ZZTJ, fn))
        if not ch["paras"]:
            continue
        chapters.append(ch)
    write_split(chapters, "zizhitongjian")
    total_note = sum(sum(len(p["notes"]) for p in c["paras"]) for c in chapters)
    print("资治通鉴：%d 卷，胡注 %d 条" % (len(chapters), total_note))
    return chapters


if __name__ == "__main__":
    parse_shiji()
    parse_zztj()
