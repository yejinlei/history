import json
import os
from datetime import datetime

BASE = "/home/user/workspace/17521090448082856013/history-site"

# 读取原文
with open(os.path.join(BASE, "data/books/shiji/text/shiji-滑稽列傳第六十六.json"), "r", encoding="utf-8") as f:
    source = json.load(f)
# 读取定稿实体
with open(os.path.join(BASE, "data/books/shiji/ontology/实体-定稿-滑稽列传第六十六.json"), "r", encoding="utf-8") as f:
    ont = json.load(f)

# 建名称到entity映射
name_map = {}  # surface -> (eid, ename, etype)
for cat in ["persons", "places", "events", "concepts"]:
    etype = cat[:-1] if cat.endswith("s") else cat
    if cat == "persons": etype = "person"
    elif cat == "places": etype = "place"
    elif cat == "events": etype = "event"
    elif cat == "concepts": etype = "concept"
    for ent in ont["entities"][cat]:
        name_map[ent["name"]] = (ent["id"], ent["name"], etype)
        for a in ent.get("alias", []):
            name_map[a] = (ent["id"], ent["name"], etype)

# 简单关键词匹配
keyword_map = {
    "淳于髡": ("person_000", "淳于髡", "person"),
    "髡": ("person_000", "淳于髡", "person"),
    "齊威王": ("person_001", "齐威王（田因齐）", "person"),
    "威王": ("person_001", "齐威王（田因齐）", "person"),
    "齊王": ("person_001", "齐威王（田因齐）", "person"),
    "優孟": ("person_002", "优孟", "person"),
    "孟": ("person_002", "优孟", "person"),
    "楚莊王": ("person_003", "楚庄王（熊侣）", "person"),
    "莊王": ("person_003", "楚庄王（熊侣）", "person"),
    "楚王": ("person_003", "楚庄王（熊侣）", "person"),
    "孫叔敖": ("person_004", "孙叔敖", "person"),
    "優旃": ("person_005", "优旃", "person"),
    "秦始皇": ("person_006", "秦始皇（嬴政）", "person"),
    "始皇": ("person_006", "秦始皇（嬴政）", "person"),
    "二世": ("person_007", "秦二世（嬴胡亥）", "person"),
    "褚先生": ("person_008", "褚少孙", "person"),
    "郭舍人": ("person_009", "郭舍人", "person"),
    "武帝": ("person_010", "刘彻（汉武帝）", "person"),
    "陛下": ("person_010", "刘彻（汉武帝）", "person"),
    "上": ("person_010", "刘彻（汉武帝）", "person"),
    "人主": ("person_010", "刘彻（汉武帝）", "person"),
    "皇帝": ("person_010", "刘彻（汉武帝）", "person"),
    "大乳母": ("person_011", "汉武帝大乳母（东武侯母）", "person"),
    "東武侯母": ("person_011", "汉武帝大乳母（东武侯母）", "person"),
    "馬游卿": ("person_012", "马游卿", "person"),
    "東方生": ("person_013", "东方朔", "person"),
    "東方朔": ("person_013", "东方朔", "person"),
    "朔": ("person_013", "东方朔", "person"),
    "東方先生": ("person_013", "东方朔", "person"),
    "蘇秦": ("person_014", "苏秦", "person"),
    "張儀": ("person_015", "张仪", "person"),
    "許由": ("person_016", "许由", "person"),
    "接輿": ("person_017", "接舆", "person"),
    "范蠡": ("person_018", "范蠡", "person"),
    "子胥": ("person_019", "伍子胥", "person"),
    "太公": ("person_020", "姜太公（吕望）", "person"),
    "混邪王": ("person_021", "浑邪王", "person"),
    "衞青": ("person_022", "卫青", "person"),
    "衞將軍": ("person_022", "卫青", "person"),
    "大將軍衞青": ("person_022", "卫青", "person"),
    "衞后": ("person_023", "卫皇后（卫子夫）", "person"),
    "東郭先生": ("person_024", "东郭先生", "person"),
    "王夫人": ("person_025", "王夫人", "person"),
    "趙王": ("person_026", "赵王（齐威王时）", "person"),
    "王先生": ("person_027", "王先生（文学卒史）", "person"),
    "北海太守": ("person_028", "北海太守", "person"),
    "魏文侯": ("person_029", "魏文侯", "person"),
    "西門豹": ("person_030", "西门豹", "person"),
    "子產": ("person_031", "子产", "person"),
    "子賤": ("person_032", "宓子贱", "person"),
    "三老": ("person_033", "邺三老", "person"),
    "廷掾": ("person_034", "邺廷掾", "person"),
    "大巫嫗": ("person_035", "大巫妪", "person"),
    "巫嫗": ("person_035", "大巫妪", "person"),
    "孫叔敖子": ("person_036", "孙叔敖之子", "person"),
    "負薪者": ("person_036", "孙叔敖之子", "person"),
    "陛楯者": ("person_037", "陛楯郎", "person"),
    "陛楯郎": ("person_037", "陛楯郎", "person"),
    "索隱": ("person_038", "司马贞", "person"),
    "函谷關": ("place_005", "函谷关", "place"),
    "雍": ("place_006", "雍县", "place"),
    "陳倉": ("place_007", "陈仓", "place"),
    "長安": ("place_008", "长安", "place"),
    "建章宮": ("place_009", "建章宫", "place"),
    "金馬門": ("place_010", "金马门", "place"),
    "北海": ("place_011", "北海郡", "place"),
    "鄴": ("place_012", "邺县", "place"),
    "寢丘": ("place_013", "寝丘", "place"),
    "余吾水": ("place_014", "余吾水", "place"),
    "洛陽": ("place_015", "洛阳", "place"),
    "齊": ("place_016", "齐国（汉封国）", "place"),
    "公車": ("place_019", "公车府", "place"),
    "六蓺": ("concept_001", "六艺（六经）", "concept"),
    "談言微中": ("concept_002", "谈言微中", "concept"),
    "隱": ("concept_003", "隐语", "concept"),
    "贅婿": ("concept_004", "赘婿", "concept"),
    "一飛沖天": ("concept_005", "一飞冲天、一鸣惊人", "concept"),
    "一鳴驚人": ("concept_005", "一飞冲天、一鸣惊人", "concept"),
    "冠纓索絕": ("concept_006", "冠缨索绝", "concept"),
    "樂極則悲": ("concept_007", "乐极生悲", "concept"),
    "酒極則亂": ("concept_007", "乐极生悲", "concept"),
    "優孟衣冠": ("concept_008", "优孟衣冠", "concept"),
    "無立錐之地": ("concept_009", "无立锥之地", "concept"),
    "漆城蕩蕩": ("concept_010", "漆城荡荡", "concept"),
    "避世金馬門": ("concept_011", "朝隐（避世金马门）", "concept"),
    "彼一時也此一時也": ("concept_012", "彼一时此一时", "concept"),
    "人之將死其言也善": ("concept_013", "人之将死，其言也善", "concept"),
    "衣褐懷寶": ("concept_014", "衣褐怀宝", "concept"),
    "相馬失之瘦相士失之貧": ("concept_015", "相马失之瘦，相士失之贫", "concept"),
    "河伯娶婦": ("concept_016", "河伯娶妇", "concept"),
    "民可以樂成不可與慮始": ("concept_017", "民可与乐成，不可与虑始", "concept"),
}

# 按关键词长度从长到短匹配，避免短词覆盖
keywords = sorted(keyword_map.keys(), key=lambda x: -len(x))

annotation = {
    "book_id": "shiji",
    "chapter_id": "66",
    "chapter_title": "滑稽列传第六十六",
    "version": "final",
    "generated_at": datetime.now().isoformat(),
    "paragraphs": []
}

for para in source["paragraphs"]:
    pid = para["id"].split(":")[-1]
    text = para["text"]
    mentions = []
    used = set()
    for kw in keywords:
        start = 0
        while True:
            pos = text.find(kw, start)
            if pos == -1:
                break
            # 检查是否重叠
            overlap = False
            for i in range(pos, pos+len(kw)):
                if i in used:
                    overlap = True
                    break
            if not overlap:
                eid, ename, etype = keyword_map[kw]
                mentions.append({
                    "entity_id": eid,
                    "entity_name": ename,
                    "entity_type": etype,
                    "start": pos,
                    "end": pos + len(kw),
                    "surface": kw
                })
                for i in range(pos, pos+len(kw)):
                    used.add(i)
            start = pos + 1
    annotation["paragraphs"].append({
        "para_id": pid,
        "text": text,
        "mentions": mentions
    })

annot_path = os.path.join(BASE, "data/books/shiji/ontology/实体标注-滑稽列传第六十六.json")
with open(annot_path, "w", encoding="utf-8") as f:
    json.dump(annotation, f, ensure_ascii=False, indent=2)
json.load(open(annot_path, "r", encoding="utf-8"))
total_mentions = sum(len(p["mentions"]) for p in annotation["paragraphs"])
print(f"实体标注已生成：{annot_path}，共{len(annotation['paragraphs'])}段，{total_mentions}处标注")
