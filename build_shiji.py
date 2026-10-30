import json, os, re
from collections import defaultdict, Counter

# 体例映射（繁体→英文键）
tili_map = {"本紀": "benji", "本纪": "benji", "表": "biao", "書": "shu", "书": "shu", "世家": "shijia", "列傳": "liezhuan", "列传": "liezhuan", "其他": "appendix"}
tili_cn = {"benji": "十二本纪", "biao": "十表", "shu": "八书", "shijia": "三十世家", "liezhuan": "七十列传", "appendix": "附录"}

# 1. 读取所有章节
base_dir = "data/texts/shiji/ch/"
chapters = []
for fn in sorted(os.listdir(base_dir)):
    if fn.endswith(".json"):
        with open(base_dir+fn, encoding="utf-8") as f:
            ch = json.load(f)
        m = re.match(r"卷(\d+)", ch["juan"])
        ch["juan_num"] = int(m.group(1)) if m else 0
        ch["id"] = "shiji-" + ch["title"]
        chapters.append(ch)
chapters.sort(key=lambda x: x["juan_num"])
print(f"读取 {len(chapters)} 篇")

# 2. 创建目录
os.makedirs("data/books/shiji/text", exist_ok=True)
os.makedirs("data/books/shiji/annotations", exist_ok=True)
os.makedirs("data/ontology/shiji", exist_ok=True)

# 3. 实体存储
persons = {}
places = {}
events = {}

# 从篇章标题提取核心人物
title_person_map = {
    # 本纪
    "五帝本紀": ["黄帝","颛顼","帝喾","尧","舜"],
    "夏本紀": ["大禹","夏启","桀"],
    "殷本紀": ["成汤","盘庚","武丁","纣王"],
    "周本紀": ["周文王","周武王","周厉王","周幽王"],
    "秦本紀": ["秦穆公","秦孝公","秦昭襄王"],
    "秦始皇本紀": ["秦始皇","秦二世","李斯","赵高"],
    "項羽本紀": ["项羽","范增","项梁","虞姬"],
    "高祖本紀": ["刘邦","萧何","张良","韩信"],
    "呂太后本紀": ["吕雉"],
    "孝文本紀": ["汉文帝"],
    "孝景本紀": ["汉景帝"],
    "孝武本紀": ["汉武帝"],
    # 世家核心人物
    "吳太伯世家": ["太伯","仲雍","季札"],
    "齊太公世家": ["姜子牙","齐桓公","管仲"],
    "魯周公世家": ["周公","鲁隐公"],
    "燕召公世家": ["召公","燕昭王"],
    "管蔡世家": ["管叔","蔡叔"],
    "陳杞世家": ["陈胡公"],
    "衛康叔世家": ["康叔"],
    "宋微子世家": ["微子","宋襄公"],
    "晉世家": ["晋文公","晋献公"],
    "楚世家": ["楚庄王","楚怀王"],
    "越王句踐世家": ["勾践","范蠡","文种"],
    "鄭世家": ["郑庄公"],
    "趙世家": ["赵武灵王","赵盾"],
    "魏世家": ["魏文侯","信陵君"],
    "韓世家": ["韩昭侯"],
    "田敬仲完世家": ["田完","齐威王"],
    "孔子世家": ["孔子"],
    "陳涉世家": ["陈胜","吴广"],
    "蕭相國世家": ["萧何"],
    "曹相國世家": ["曹参"],
    "留侯世家": ["张良"],
    "陳丞相世家": ["陈平"],
    "絳侯周勃世家": ["周勃","周亚夫"],
    # 列传核心人物
    "伯夷列傳": ["伯夷","叔齐"],
    "管晏列傳": ["管仲","晏婴"],
    "老子韓非列傳": ["老子","庄子","韩非子"],
    "司馬穰苴列傳": ["司马穰苴"],
    "孫子吳起列傳": ["孙武","孙膑","吴起"],
    "伍子胥列傳": ["伍子胥"],
    "商君列傳": ["商鞅"],
    "蘇秦列傳": ["苏秦"],
    "張儀列傳": ["张仪"],
    "白起王翦列傳": ["白起","王翦"],
    "孟子荀卿列傳": ["孟子","荀子"],
    "孟嘗君列傳": ["孟尝君"],
    "平原君虞卿列傳": ["平原君"],
    "魏公子列傳": ["信陵君"],
    "春申君列傳": ["春申君"],
    "樂毅列傳": ["乐毅"],
    "廉頗藺相如列傳": ["廉颇","蔺相如"],
    "屈原賈生列傳": ["屈原","贾谊"],
    "呂不韋列傳": ["吕不韦"],
    "刺客列傳": ["荆轲","聂政","专诸","豫让"],
    "李斯列傳": ["李斯"],
    "淮陰侯列傳": ["韩信"],
    "李將軍列傳": ["李广"],
    "衛將軍驃騎列傳": ["卫青","霍去病"],
    "司馬相如列傳": ["司马相如"],
    "太史公自序": ["司马迁"]
}
for title, names in title_person_map.items():
    for name in names:
        pid = f"book:shiji:person:{name}"
        persons[pid] = {
            "id": pid,
            "name": name,
            "type": "核心人物",
            "in_chapter": "shiji-"+title,
            "global_same_as": f"global:person:{name}",
            "aliases": [],
            "evidence": []
        }

# 地名、事件关键词
place_keys = ["涿鹿","阪泉","咸阳","长安","洛阳","邯郸","临淄","彭城","垓下","鸿门","霸上",
              "函谷关","崤山","太行","黄河","长江","东海","南海","长城","阴山","祁连"]
event_keys = ["涿鹿之战","阪泉之战","牧野之战","城濮之战","长平之战","巨鹿之战","鸿门宴",
              "垓下之围","白登之围","文景之治","汉武盛世","焚书坑儒","陈胜吴广起义","商鞅变法",
              "合纵连横","胡服骑射","百家争鸣","独尊儒术","张骞出使西域","封狼居胥"]

# 预存核心地名事件
for p in place_keys:
    places[f"book:shiji:place:{p}"] = {
        "id": f"book:shiji:place:{p}", "name": p, "type": "核心地名",
        "global_same_as": f"global:place:{p}", "evidence": []
    }
for e in event_keys:
    events[f"book:shiji:event:{e}"] = {
        "id": f"book:shiji:event:{e}", "name": e, "type": "核心事件",
        "global_same_as": f"global:event:{e}", "evidence": []
    }

# 4. 逐章处理：分离正文/批注，补充evidence
chapter_list = []
total_paras = 0
total_chars = 0
total_annotations = 0

for ch in chapters:
    ch_id = ch["id"]
    section = ch["section"]
    tili = tili_map[section]

    # 正文输出
    paragraphs = []
    annotations = []
    ann_counter = 0
    para_count = len(ch["paras"])
    char_count = 0

    for p_idx, para in enumerate(ch["paras"]):
        text = para["text"]
        char_count += len(text)
        sent_id = f"text:shiji:{ch_id}:p{p_idx}"
        paragraphs.append({"id": sent_id, "text": text})

        # 为核心人物添加证据
        for name in title_person_map.get(ch["title"], []):
            if name in text:
                pid = f"book:shiji:person:{name}"
                if sent_id not in persons[pid]["evidence"]:
                    persons[pid]["evidence"].append(sent_id)
        # 为核心地名添加证据
        for pl in place_keys:
            if pl in text:
                plid = f"book:shiji:place:{pl}"
                if sent_id not in places[plid]["evidence"]:
                    places[plid]["evidence"].append(sent_id)
        # 为核心事件添加证据
        for ev in event_keys:
            if ev[:2] in text and len(ev)>=4:
                eid = f"book:shiji:event:{ev}"
                if sent_id not in events[eid]["evidence"]:
                    events[eid]["evidence"].append(sent_id)

        # 注疏
        for note in para.get("notes", []):
            ann_id = f"anno:shiji:{ch_id}:a{ann_counter}"
            annotations.append({
                "id": ann_id,
                "book": "shiji",
                "chapter_id": ch_id,
                "target_para_id": sent_id,
                "annotator": note["tag"],  # 集解/索隐/正义
                "text": note["text"]
            })
            ann_counter += 1

    # 保存文件
    with open(f"data/books/shiji/text/{ch_id}.json", "w", encoding="utf-8") as f:
        json.dump({
            "book":"shiji","book_name":"史记","chapter_id":ch_id,"title":ch["title"],
            "juan":ch["juan"],"tili":tili,"author":"司马迁",
            "paragraphs": paragraphs
        }, f, ensure_ascii=False, indent=2)
    with open(f"data/books/shiji/annotations/{ch_id}.json", "w", encoding="utf-8") as f:
        json.dump(annotations, f, ensure_ascii=False, indent=2)

    chapter_list.append({
        "id": ch_id, "title": ch["title"], "juan": ch["juan"], "juan_num": ch["juan_num"],
        "tili": tili, "tili_name": section, "para_count": para_count,
        "char_count": char_count, "annotation_count": len(annotations)
    })
    total_paras += para_count
    total_chars += char_count
    total_annotations += len(annotations)

# 5. 统计体例分布
tili_counter = Counter(c["tili_name"] for c in chapter_list)
structure = {}
for cn_name, count in tili_counter.items():
    tili_key = tili_map[cn_name]
    structure[tili_key] = {"name": tili_cn[tili_key], "count": count}

# 6. 保存完整本体
ontology = {
    "book": "shiji",
    "book_name": "史记",
    "author": "司马迁",
    "dynasty": "西汉",
    "annotation_authors": {"裴骃": "集解", "司马贞": "索隐", "张守节": "正义"},
    "total_chapters": len(chapters),
    "total_paragraphs": total_paras,
    "total_chars": total_chars,
    "total_annotations": total_annotations,
    "structure": structure,
    "chapters": chapter_list,
    "entities": {
        "persons": list(persons.values()),
        "places": list(places.values()),
        "events": list(events.values())
    },
    "build_version": "v1.0",
    "build_time": "2026"
}
with open("data/ontology/shiji/ontology.json", "w", encoding="utf-8") as f:
    json.dump(ontology, f, ensure_ascii=False, indent=2)

# 7. 生成篇章索引（供阅读器使用）
with open("data/books/shiji/chapter_index.json", "w", encoding="utf-8") as f:
    json.dump(chapter_list, f, ensure_ascii=False, indent=2)

# 输出统计
print("="*60)
print("✅ 《史记》本体构建完成")
print(f"总篇章：{len(chapters)} 篇")
print(f"体例分布：{dict(tili_counter)}")
print(f"总段落：{total_paras:,}")
print(f"总字数：{total_chars:,}")
print(f"总注疏：{total_annotations:,} 条（三家注已分离）")
print(f"核心人物：{len(persons)} 位")
print(f"核心地名：{len(places)} 处")
print(f"核心事件：{len(events)} 个")
print(f"正文目录：data/books/shiji/text/ ({len(chapters)} 个文件)")
print(f"注疏目录：data/books/shiji/annotations/ ({len(chapters)} 个文件)")
print(f"本体文件：data/ontology/shiji/ontology.json")
