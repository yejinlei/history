# -*- coding: utf-8 -*-
"""步骤8：实体标注 - 逐段字串匹配计算start/end"""
import json, os, re

ROOT = "/home/user/workspace/17521090448082856013/history-site"
BASE_JSON = os.path.join(ROOT, "data/books/shiji/text/shiji-滑稽列傳第六十六.json")
ONT_DIR = os.path.join(ROOT, "data/books/shiji/ontology")
CHAPTER_ID = "shiji-滑稽列傳第六十六"
CHAPTER_TITLE = "滑稽列传第六十六"
TODAY = "2026-11-02"

with open(BASE_JSON, encoding="utf-8") as f:
    base = json.load(f)
para_map = {}
para_full = {}
for p in base["paragraphs"]:
    pid = p["id"].split(":")[-1]
    para_map[pid] = p["text"]
    para_full[pid] = p

final_path = os.path.join(ONT_DIR, "实体-定稿-滑稽列传第六十六.json")
with open(final_path, encoding="utf-8") as f:
    final = json.load(f)

# 合并所有实体并建立id->(name, alias, category)
all_ents = []
id2cat = {}
id2name = {}
for cat in ["persons","places","events","concepts"]:
    for ent in final["entities"][cat]:
        all_ents.append((cat, ent))
        id2cat[ent["id"]] = cat
        id2name[ent["id"]] = ent["name"]

def get_match_terms(ent):
    """返回要在原文中匹配的字串列表（优先长的）。"""
    names = []
    # alias中的繁体/核心名称
    for a in ent.get("alias", []):
        if a and len(a) >= 1:
            names.append(a)
    # 从name里取括号外的部分
    core = ent["name"]
    if "（" in core:
        core = core.split("（")[0]
    if "(" in core:
        core = core.split("(")[0]
    names.append(core)
    # 去重+按长度降序
    seen=set(); uniq=[]
    for n in names:
        if n not in seen:
            seen.add(n); uniq.append(n)
    uniq.sort(key=lambda x:-len(x))
    return uniq

paragraphs_out = []
total_mentions = 0
for i in range(29):
    pid = f"p{i}"
    text = para_map[pid]
    # 收集所有匹配 (start, end, ent_id, match_text)
    matches = []
    # 记录已占用的字符位置
    occupied = [False]*len(text)
    for cat, ent in all_ents:
        # 是否本实体在本段evidence内
        if pid not in ent.get("evidence", []):
            continue
        terms = get_match_terms(ent)
        for term in terms:
            if not term or len(term) < 1: continue
            pos = 0
            while True:
                idx = text.find(term, pos)
                if idx == -1: break
                # 检查与已有匹配是否重叠
                end = idx+len(term)
                overlap = False
                for k in range(idx, end):
                    if occupied[k]:
                        overlap = True; break
                if not overlap:
                    # 采用此匹配
                    matches.append({"start":idx,"end":end,"id":ent["id"],"text":term})
                    for k in range(idx, end):
                        occupied[k] = True
                pos = idx+1
    # 排序
    matches.sort(key=lambda m:m["start"])
    # 格式化输出
    mentions = []
    for m in matches:
        mentions.append({
            "id": m["id"],
            "start": m["start"],
            "end": m["end"],
            "text": m["text"],
        })
        total_mentions += 1
    paragraphs_out.append({
        "para_id": pid,
        "text": text,
        "mentions": mentions,
    })
    print(pid, "mentions:", len(mentions))

annotation = {
    "book_id": "shiji",
    "chapter_id": CHAPTER_ID,
    "chapter_title": CHAPTER_TITLE,
    "version": "1.0",
    "generated_at": TODAY,
    "paragraphs": paragraphs_out,
}
ann_path = os.path.join(ONT_DIR, "实体标注-滑稽列传第六十六.json")
with open(ann_path, "w", encoding="utf-8") as f:
    json.dump(annotation, f, ensure_ascii=False, indent=2)
print("标注 written:", ann_path)
print("总mentions:", total_mentions)
