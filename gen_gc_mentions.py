#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
BASE = "/home/user/workspace/17521090448082856013/history-site"

with open(os.path.join(BASE,"data/books/shiji/text/shiji-龜策列傳第六十八.json"),encoding="utf-8") as f:
    src = json.load(f)
paras = [p["text"] for p in src["paragraphs"]]

with open(os.path.join(BASE,"data/books/shiji/ontology/实体-定稿-龟策列传第六十八.json"),encoding="utf-8") as f:
    onto = json.load(f)

# 额外补充常用短名（≤8字），避免泛用单字
extra_alias = {
    "person_gc_021": ["文王"],
    "person_gc_004": ["衞平"],
    "person_gc_006": ["神龜","元龜","玉靈","靈龜"],
    "person_gc_007": ["周公"],
    "person_gc_009": ["紂"],
    "person_gc_020": ["湯"],
    "person_gc_019": ["桀"],
    "person_gc_031": ["禹"],
    "person_gc_008": ["武王"],
    "concept_gc_002": ["太卜"],
    "concept_gc_001": ["龜策","卜筮"],
    "concept_gc_005": ["灼龜","鑽龜"],
    "concept_gc_013": ["橫吉安","橫吉"],
    "place_gc_005": ["宋國"],
    "place_gc_004": ["泉陽"],
}
# 排除的短名（太泛单字）
blocked = {"卜","筮","龜","宋","河","桀","湯","禹","紂","王","者","不","之","而"}

entity_aliases = {}
for cat in ["persons","places","events","concepts"]:
    for e in onto["entities"][cat]:
        names = [e["name"]] + e.get("alias",[]) + extra_alias.get(e["id"],[])
        shorts=[]; seen=set()
        for n in names:
            if n in blocked: continue
            if len(n) < 2 or len(n) > 8: continue
            if n in seen: continue
            seen.add(n); shorts.append(n)
        shorts.sort(key=lambda x:(len(x), -len(x)))  # 短的优先扫描；冲突时按长的覆盖
        if shorts:
            entity_aliases[e["id"]] = {"names":shorts, "name":e["name"], "cat":cat}

paragraphs_out=[]
for i,text in enumerate(paras):
    pid=f"p{i}"
    found=[]
    for eid,info in entity_aliases.items():
        for nm in info["names"]:
            start=0
            while True:
                idx=text.find(nm,start)
                if idx<0: break
                end=idx+len(nm)
                found.append((idx,end,-len(nm),eid,info["name"],nm))
                start=end
    # 先按start升序、长度降序；贪心去重叠：同起点取最长；重叠保留先出现的长者
    found.sort(key=lambda x:(x[0], x[2]))  # x[2]=-len 即长的先
    kept=[]; last_end=-1
    for sp in found:
        s,e,_,eid,ename,txt=sp
        if s>=last_end:
            kept.append((s,e,eid,ename,txt))
            last_end=e
    # 对于相同区间若有更高优先（person>place>event>concept），暂不复杂处理
    mentions=[{"start":s,"end":e,"entity_id":ei,"entity_name":en,"text":t} for s,e,ei,en,t in kept]
    mentions.sort(key=lambda x:x["start"])
    paragraphs_out.append({"para_id":pid,"text":text,"mentions":mentions})

out={
    "book_id":"shiji",
    "chapter_id":"shiji-龜策列傳第六十八",
    "chapter_title":"龟策列传第六十八",
    "version":"1.0",
    "generated_at":"2026-11-02T15:15:00",
    "paragraphs":paragraphs_out
}
with open(os.path.join(BASE,"data/books/shiji/ontology/实体标注-龟策列传第六十八.json"),"w",encoding="utf-8") as f:
    json.dump(out,f,ensure_ascii=False,indent=2)

total=sum(len(p["mentions"]) for p in paragraphs_out)
print("总mentions:",total)
for p in paragraphs_out[:6]:
    print(p["para_id"],"n=",len(p["mentions"]))
    for m in p["mentions"][:10]:
        print(" ",m["start"],m["end"],repr(m["text"]),"->",m["entity_name"])
