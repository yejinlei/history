# -*- coding: utf-8 -*-
"""Re-run annotation with expanded aliases."""
import json, os, re
ROOT="/home/user/workspace/17521090448082856013/history-site"
ONTO=os.path.join(ROOT,"data/books/shiji/ontology")
SRC=os.path.join(ROOT,"data/books/shiji/text/shiji-太史公自序第七十.json")
with open(SRC,encoding='utf-8') as f: paras=json.load(f)['paragraphs']
paras=[p['text'] for p in paras]
with open(os.path.join(ONTO,"实体-定稿-太史公自序第七十.json"),encoding='utf-8') as f: ent=json.load(f)
# Build alias map
A={}
def add_alias(name, eid):
    if name and len(name)>=1:
        A[name]=eid
for grp in ['persons','places','events','concepts']:
    for x in ent['entities'][grp]:
        add_alias(x['name'],x['id'])
        for a in x.get('aliases',[]): add_alias(a,x['id'])

# Add extra aliases to improve mentions (non-ambig)
extra = {
    "遷":"p_zx_012","迁":"p_zx_012",
    "談":"p_zx_011",
    "太史公":"p_zx_012",  # 默认司马迁
    "董生":"p_zx_017",
    "子羽":"p_zx_041","項羽":"p_zx_041","項籍":"p_zx_041",
    "始皇":"p_zx_042",
    "高祖":"p_zx_037",
    "呂太后":"p_zx_038","諸呂":"p_zx_038",
    "孝文":"p_zx_039","太宗":"p_zx_039",
    "孝景":"p_zx_040",
    "今上":"p_zx_036","明天子":"p_zx_036","天子":"p_zx_036",
    "西伯":"p_zx_020","文王":"p_zx_020",
    "武王":"p_zx_021",
    "堯":"p_zx_024","舜":"p_zx_025",
    "湯":"p_zx_026",
    "屈原":"p_zx_027",
    "左丘":"p_zx_028",
    "不韋":"p_zx_030",
    "韓非":"p_zx_031",
    "李陵":"p_zx_032",
    "張儀":"p_zx_033","张仪":"p_zx_033",
    "白起":"p_zx_034","武安君":"p_zx_034",
    "仲尼":"p_zx_018","孔氏":"p_zx_018",
    "旦":"p_zx_019",
    "李耳":"p_zx_022","老子":"p_zx_022",
    "龍門":"pl_zx_001",
    "會稽":"pl_zx_003",
    "禹穴":"pl_zx_004",
    "九疑":"pl_zx_005",
    "周南":"pl_zx_014",
    "河洛":"pl_zx_016",
    "羑里":"pl_zx_018",
    "石室金匱":"pl_zx_019",
    "名山":"pl_zx_020",
    "巴、蜀":"pl_zx_012","巴蜀":"pl_zx_012",
    "卭":"pl_zx_013","笮":"pl_zx_013","昆明":"pl_zx_013",
    "春秋":"c_zx_005",
    "易":"c_zx_004","詩":"c_zx_004","書":"c_zx_004","禮":"c_zx_004","樂":"c_zx_004",
    "六家":"c_zx_003","六家要指":"c_zx_003","六蓺":"c_zx_004","六藝":"c_zx_004",
    "發憤":"c_zx_008","發憤著書":"c_zx_008","一家之言":"c_zx_007",
    "五體":"c_zx_009","本紀":"c_zx_009","表":"c_zx_009","世家":"c_zx_009","列傳":"c_zx_009",
    "太史公書":"c_zx_006","史記":"c_zx_006",
    "五帝本紀":"e_zx_032","夏本紀":"e_zx_032","殷本紀":"e_zx_032","周本紀":"e_zx_032","秦本紀":"e_zx_032","始皇本紀":"e_zx_032","項羽本紀":"e_zx_032","高祖本紀":"e_zx_032","呂太后本紀":"e_zx_032","孝文本紀":"e_zx_032","孝景本紀":"e_zx_032","今上本紀":"e_zx_032",
}
for k,v in extra.items(): add_alias(k,v)
# Remove too-short ambiguous single chars if any (skip to be safe: don't include 重/黎 as single)
for bad in ["重","黎","法","道","德","名","阳","阴","秦","楚","齐","赵","魏","韩","燕","梁","吴"]:
    if bad in A and len(bad)==1: A.pop(bad,None)

sorted_aliases = sorted(A.keys(), key=lambda x:(-len(x),x))
# Add entity_id validity check
all_ids = set()
for grp in ['persons','places','events','concepts']:
    for x in ent['entities'][grp]: all_ids.add(x['id'])
for r in ent.get('relations',[]): all_ids.add(r['source']); all_ids.add(r['target'])

annotations=[]; total=0
for i,text in enumerate(paras):
    matches=[]; used=set()
    for a in sorted_aliases:
        if not a: continue
        start=0
        while True:
            idx=text.find(a,start)
            if idx<0: break
            # Check word-boundary for single char: avoid matching inside other words (simplified: allow anywhere for CJK)
            overlap=False
            for ms,me in used:
                if not(idx+len(a)<=ms or idx>=me): overlap=True; break
            if not overlap:
                eid=A[a]
                if eid in all_ids:
                    matches.append({"start":idx,"end":idx+len(a),"text":a,"entity_id":eid})
                    used.add((idx,idx+len(a)))
                    total+=1
            start=idx+1
    matches.sort(key=lambda x:x['start'])
    annotations.append({"paragraph_id":f"p{i}","text":text,"mentions":matches})

# Validate no mention references a nonexistent id
ref_ids=set(m['entity_id'] for a in annotations for m in a['mentions'])
print("total mentions:",total,"unique ids referenced:",len(ref_ids))
print("Dangling ids:",ref_ids-all_ids)

obj={"book_id":"shiji","chapter_id":"shiji-太史公自序第七十","chapter_title":"太史公自序第七十","version":"1.0","generated_at":"2026-11-02","annotations":annotations}
with open(os.path.join(ONTO,"实体标注-太史公自序第七十.json"),"w",encoding='utf-8') as f:
    json.dump(obj,f,ensure_ascii=False,indent=2)
print("Re-saved annotation.")
