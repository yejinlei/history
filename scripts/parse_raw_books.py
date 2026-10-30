#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 data/raw 下二十四史纯文本（古诗文网原文格式），生成按篇拆分的 JSON。

文本格式：
    ===== （原文） =====
    <书名>-<部类>
    下一节：
    第X章-<篇名> 原文
    <正文>

输出与 parse_epub.py 一致：index.json + ch/NNNN.json
"""
import os
import re
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data", "texts")

# key: (书名, 作者)
BOOK_META = {
    "hanshu": ("汉书", "[汉] 班固 撰"),
    "houhanshu": ("后汉书", "[南朝宋] 范晔 撰"),
    "sanguozhi": ("三国志", "[晋] 陈寿 撰"),
    "jinshu": ("晋书", "[唐] 房玄龄 等撰"),
    "songshu": ("宋书", "[南朝梁] 沈约 撰"),
    "nanqishu": ("南齐书", "[南朝梁] 萧子显 撰"),
    "liangshu": ("梁书", "[唐] 姚思廉 撰"),
    "chenshu": ("陈书", "[唐] 姚思廉 撰"),
    "weishu": ("魏书", "[北齐] 魏收 撰"),
    "beiqiishu": ("北齐书", "[唐] 李百药 撰"),
    "zhoushu": ("周书", "[唐] 令狐德棻 等撰"),
    "suishu": ("隋书", "[唐] 魏征 等撰"),
    "nanshi": ("南史", "[唐] 李延寿 撰"),
    "beishi": ("北史", "[唐] 李延寿 撰"),
    "jiutangshu": ("旧唐书", "[后晋] 刘昫 等撰"),
    "xintangshu": ("新唐书", "[宋] 欧阳修 等撰"),
    "jiusidai": ("旧五代史", "[宋] 薛居正 等撰"),
    "xinwudaishi": ("新五代史", "[宋] 欧阳修 撰"),
    "songshi": ("宋史", "[元] 脱脱 等撰"),
    "liaoshi": ("辽史", "[元] 脱脱 等撰"),
    "jinshi": ("金史", "[元] 脱脱 等撰"),
    "yuanshi": ("元史", "[明] 宋濂 等撰"),
    "mingshi": ("明史", "[清] 张廷玉 等撰"),
}

CN_DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9}
CN = "一二三四五六七八九十百零〇"


def cn2num(s):
    if not s:
        return 0
    total, num = 0, 0
    for ch in s:
        if ch in CN_DIGITS:
            num = CN_DIGITS[ch]
        elif ch == "十":
            total += (num or 1) * 10
            num = 0
        elif ch == "百":
            total += (num or 1) * 100
            num = 0
    return total + num


def parse_book(key):
    path = os.path.join(RAW, key + ".txt")
    if not os.path.exists(path):
        return []
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="ignore").replace("\x00", "")
    blocks = re.split(r"=====\s*（原文）\s*=====", text)
    chapters = []
    for blk in blocks:
        blk = blk.strip()
        if not blk:
            continue
        lines = [l.strip() for l in blk.split("\n")]
        title, start, sec = None, 0, None
        for i, l in enumerate(lines):
            m = re.match(r"第[" + CN + r"]+章[-－](.*?)\s*原文", l)
            if m:
                title = m.group(1).strip() or "正文"
                start = i + 1
                break
            m2 = re.match(r"(卷[" + CN + r"]+)\s*原文", l)
            if m2:
                title = m2.group(1).strip()
                start = i + 1
                break
        if title is None:
            continue
        for l in lines[:start]:
            m3 = re.match(r"^(.+?)-(.+)$", l)
            if m3 and "节" not in l and not l.startswith("第"):
                sec = m3.group(2).strip()
        body = []
        for l in lines[start:]:
            if not l or l in ("上一节：", "下一节："):
                continue
            if re.match(r"^(上一节|下一节)", l):
                continue
            body.append(l)
        if not body:
            continue
        chapters.append({
            "title": title,
            "section": sec or "原文",
            "paras": [{"text": p, "notes": []} for p in body],
        })
    return chapters


def write_split(chapters, key, name):
    out_dir = os.path.join(OUT, key)
    ch_dir = os.path.join(out_dir, "ch")
    os.makedirs(ch_dir, exist_ok=True)
    index = []
    for i, ch in enumerate(chapters, start=1):
        juan = ""
        m = re.search(r"卷[" + CN + r"]+", ch["title"])
        if m:
            juan = m.group(0)
        index.append({
            "id": i, "title": ch["title"], "juan": juan,
            "juan_num": cn2num(re.sub(r"[^" + CN + r"]", "", juan)) if juan else 0,
            "section": ch["section"],
        })
        with open(os.path.join(ch_dir, "%04d.json" % i), "w", encoding="utf-8") as f:
            json.dump(ch, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(out_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    n_paras = sum(len(c["paras"]) for c in chapters)
    print("%s（%s）：%d 篇，%d 段" % (name, key, len(chapters), n_paras))
    return len(chapters)


if __name__ == "__main__":
    books = []
    for key, (name, author) in BOOK_META.items():
        chs = parse_book(key)
        if not chs:
            print("跳过（无内容）：%s" % key)
            continue
        cnt = write_split(chs, key, name)
        books.append({"key": key, "name": name, "author": author, "notes": "", "style": "plain", "count": cnt})
    # 带注两本一并登记
    for key, name, author, notes in [
        ("shiji", "史记", "[汉] 司马迁 撰", "裴骃《集解》· 司马贞《索隐》· 张守节《正义》"),
        ("zizhitongjian", "资治通鉴", "[宋] 司马光 撰", "胡三省《音注》"),
    ]:
        idx_path = os.path.join(OUT, key, "index.json")
        if os.path.exists(idx_path):
            cnt = len(json.load(open(idx_path, encoding="utf-8")))
            books.append({"key": key, "name": name, "author": author, "notes": notes, "style": "annotated", "count": cnt})
    # 排序：史记、资治通鉴在前，其余按二十四史顺序
    order = ["shiji", "hanshu", "houhanshu", "sanguozhi", "jinshu", "songshu", "nanqishu",
             "liangshu", "chenshu", "weishu", "beiqiishu", "zhoushu", "suishu", "nanshi",
             "beishi", "jiutangshu", "xintangshu", "jiusidai", "xinwudaishi", "songshi",
             "liaoshi", "jinshi", "yuanshi", "mingshi", "zizhitongjian"]
    books.sort(key=lambda b: order.index(b["key"]) if b["key"] in order else 99)
    with open(os.path.join(OUT, "books.json"), "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=1)
    print("\n共 %d 部书写入 books.json" % len(books))
