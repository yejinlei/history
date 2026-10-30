#!/usr/bin/env python3
# 基于史记·五帝本纪文本+三家注，抽取ABox实体和RBox三元组
import json
import re

# 读取史记目录和五帝本纪文本
books = json.load(open('/home/user/workspace/17521090448082856013/history-site/data/texts/books.json', encoding='utf-8'))
shiji_dir = '/home/user/workspace/17521090448082856013/history-site/data/texts/shiji'

# 先找史记配置和五帝本纪
shiji_book = next(b for b in books if b['key'] == 'shiji')
# 史记的categories在单独的json里？看目录，应该已经生成了index.json
try:
    shiji_index = json.load(open(f'{shiji_dir}/index.json', encoding='utf-8'))
    wudi_chapter = None
    for group in shiji_index['groups']:
        for ch in group['chapters']:
            if '五帝本纪' in ch['title']:
                wudi_chapter = ch
                break
except:
    wudi_chapter = {"title": "五帝本纪第一", "file": "001-五帝本纪.json"}

print(f"找到篇章：{wudi_chapter['title']}，文件：ch/0001.json")

# 读取五帝本纪正文
with open(f"{shiji_dir}/ch/0001.json", encoding='utf-8') as f:
    wudi_data = json.load(f)

full_text = "\n".join([s['text'] for s in wudi_data['sentences']])

# ========== ABox 实体抽取 ==========
entities = {
    "Person": [],
    "Place": [],
    "Event": [],
    "Dynasty": [],
    "Book": [],
    "Chapter": [],
    "Annotation": []
}

# 先添加书目和篇章
entities["Book"].append({
    "@id": "book-shiji",
    "@type": "hist:Book",
    "hist:title": "史记",
    "hist:author": "person-simaqian-westernhan",
    "hist:dynasty": "西汉",
    "hist:completionYear": "-91",
    "hist:totalVolumes": 130,
    "hist:genre": "纪传体通史"
})

entities["Chapter"].append({
    "@id": "chapter-shiji-wudibenji",
    "@type": "hist:Chapter",
    "hist:title": "五帝本纪第一",
    "hist:belongsToBook": "book-shiji",
    "hist:category": "本纪",
    "hist:volumeNumber": 1
})

# 添加史学家/注者实体
historiographers = [
    {"@id": "person-simaqian-westernhan", "name": "司马迁", "aliases": ["司马子长", "太史公"], "dynasty": "dynasty-westernhan", "note": "《史记》作者"},
    {"@id": "person-peiyin-liusong", "name": "裴骃", "aliases": ["裴龙驹"], "dynasty": "dynasty-liusong", "note": "《史记集解》作者"},
    {"@id": "person-simazhen-tang", "name": "司马贞", "aliases": ["司马子正", "小司马"], "dynasty": "dynasty-tang", "note": "《史记索隐》作者"},
    {"@id": "person-zhangshoujie-tang", "name": "张守节", "dynasty": "dynasty-tang", "note": "《史记正义》作者"},
]
for p in historiographers:
    entities["Person"].append({
        "@id": p["@id"],
        "@type": "hist:Historiographer",
        "hist:name": p["name"],
        "hist:aliases": p["aliases"],
        "hist:dynasty": p["dynasty"],
        "hist:note": p["note"]
    })

# 添加朝代实体
dynasties = [
    {"@id": "dynasty-westernhan", "name": "西汉", "startYear": "-202", "endYear": "8", "founder": "person-liubang-westernhan"},
    {"@id": "dynasty-tang", "name": "唐朝", "startYear": "618", "endYear": "907", "founder": "person-liyuan-tang"},
    {"@id": "dynasty-liusong", "name": "刘宋", "startYear": "420", "endYear": "479", "founder": "person-liuyu-liusong"},
    {"@id": "dynasty-yandi", "name": "炎帝部落", "startYear": None, "endYear": None},
    {"@id": "dynasty-huangdi", "name": "黄帝部落", "startYear": None, "endYear": None},
]
for d in dynasties:
    entities["Dynasty"].append({
        "@id": d["@id"],
        "@type": "hist:Dynasty",
        "hist:name": d["name"],
        "hist:startYear": d["startYear"],
        "hist:endYear": d["endYear"],
        "hist:founder": d.get("founder")
    })

# 五帝人物（核心人物实体）
wudi_persons = [
    {"@id": "person-huangdi-prehistoric", "name": "黄帝", "aliases": ["公孙轩辕", "轩辕", "有熊氏"], "dynasty": "dynasty-huangdi", "note": "五帝之首，少典之子"},
    {"@id": "person-yandi-prehistoric", "name": "炎帝", "aliases": ["神农氏"], "dynasty": "dynasty-yandi", "note": "与黄帝同时代部落首领"},
    {"@id": "person-shaodian-prehistoric", "name": "少典", "note": "黄帝之父"},
    {"@id": "person-chiyou-prehistoric", "name": "蚩尤", "note": "九黎部落首领，与黄帝战于涿鹿"},
    {"@id": "person-zhuanxu-prehistoric", "name": "颛顼", "aliases": ["高阳氏"], "note": "五帝之二，黄帝之孙，昌意之子"},
    {"@id": "person-diku-prehistoric", "name": "帝喾", "aliases": ["高辛氏"], "note": "五帝之三，黄帝曾孙，玄嚣之孙"},
    {"@id": "person-yao-prehistoric", "name": "尧", "aliases": ["放勋", "陶唐氏"], "note": "五帝之四，帝喾之子"},
    {"@id": "person-shun-prehistoric", "name": "舜", "aliases": ["重华", "有虞氏"], "note": "五帝之五，颛顼六世孙"},
    {"@id": "person-changyi-prehistoric", "name": "昌意", "note": "黄帝之子，颛顼之父"},
    {"@id": "person-xuanxiao-prehistoric", "name": "玄嚣", "aliases": ["青阳"], "note": "黄帝之子，帝喾之祖父"},
    {"@id": "person-qiaoji-prehistoric", "name": "蟜极", "note": "玄嚣之子，帝喾之父"},
    {"@id": "person-fengshan-prehistoric", "name": "风后", "note": "黄帝大臣"},
    {"@id": "person-lim-prehistoric", "name": "力牧", "note": "黄帝大臣"},
    {"@id": "person-xianyuan-prehistoric", "name": "常先", "note": "黄帝大臣"},
    {"@id": "person-dahong-prehistoric", "name": "大鸿", "note": "黄帝大臣"},
]
for p in wudi_persons:
    entities["Person"].append({
        "@id": p["@id"],
        "@type": "hist:Person",
        "hist:name": p["name"],
        "hist:aliases": p.get("aliases", []),
        "hist:dynasty": p.get("dynasty"),
        "hist:note": p.get("note", "")
    })

# 地理实体
places = [
    {"@id": "place-banquan", "ancientName": "阪泉", "modernLocation": "今河北涿鹿东南", "note": "黄帝与炎帝战于阪泉之野"},
    {"@id": "place-zhuolu", "ancientName": "涿鹿", "modernLocation": "今河北涿鹿", "note": "黄帝与蚩尤战于涿鹿之野"},
    {"@id": "place-taishan", "ancientName": "泰山", "modernLocation": "今山东泰安", "note": "黄帝东至于海，登丸山，及岱宗，岱宗即泰山"},
    {"@id": "place-wanshan", "ancientName": "丸山", "modernLocation": "今山东临朐", "note": "黄帝东巡所登之山"},
    {"@id": "place-kongtong", "ancientName": "空桐", "modernLocation": "今甘肃平凉", "note": "黄帝西至于空桐"},
    {"@id": "place-xiangshan", "ancientName": "鸡头山", "modernLocation": "今宁夏泾源", "note": "黄帝西登鸡头"},
    {"@id": "place-jianghan", "ancientName": "江、汉", "modernLocation": "长江、汉水流域", "note": "黄帝南至于江，登熊、湘"},
    {"@id": "place-xiongshan", "ancientName": "熊山", "note": "黄帝南巡所登"},
    {"@id": "place-xiangshan2", "ancientName": "湘山", "note": "黄帝南巡所登，今湖南岳阳"},
    {"@id": "place-xiongnu", "ancientName": "荤粥", "modernLocation": "匈奴古称，北方游牧民族", "note": "黄帝北逐荤粥"},
    {"@id": "place-fushan", "ancientName": "釜山", "note": "黄帝合符釜山，在今河北涿鹿"},
    {"@id": "place-zhuoluzhiye", "ancientName": "涿鹿之阿", "note": "黄帝邑于涿鹿之阿，都城所在"},
]
for pl in places:
    entities["Place"].append({
        "@id": pl["@id"],
        "@type": "hist:Place",
        "hist:ancientName": pl["ancientName"],
        "hist:modernLocation": pl.get("modernLocation", ""),
        "hist:note": pl.get("note", "")
    })

# 历史事件
events = [
    {"@id": "event-banquan-battle", "name": "阪泉之战", "eventType": "战争", "location": "place-banquan", "participants": ["person-huangdi-prehistoric", "person-yandi-prehistoric"], "note": "黄帝与炎帝三战于阪泉之野，然后得其志"},
    {"@id": "event-zhuolu-battle", "name": "涿鹿之战", "eventType": "战争", "location": "place-zhuolu", "participants": ["person-huangdi-prehistoric", "person-chiyou-prehistoric"], "note": "黄帝擒杀蚩尤于涿鹿之野，诸侯尊为天子"},
    {"@id": "event-huangdi-expedition-east", "name": "黄帝东巡", "eventType": "巡狩", "location": "place-taishan", "participants": ["person-huangdi-prehistoric"], "note": "东至于海，登丸山及岱宗"},
    {"@id": "event-huangdi-expedition-west", "name": "黄帝西巡", "eventType": "巡狩", "location": "place-kongtong", "participants": ["person-huangdi-prehistoric"], "note": "西至于空桐，登鸡头"},
    {"@id": "event-huangdi-expedition-south", "name": "黄帝南巡", "eventType": "巡狩", "location": "place-jianghan", "participants": ["person-huangdi-prehistoric"], "note": "南至于江，登熊、湘"},
    {"@id": "event-huangdi-expedition-north", "name": "黄帝北逐荤粥", "eventType": "战争", "location": "place-xiongnu", "participants": ["person-huangdi-prehistoric"], "note": "北逐荤粥，统一北方"},
    {"@id": "event-fushan-meeting", "name": "釜山合符", "eventType": "会盟", "location": "place-fushan", "participants": ["person-huangdi-prehistoric"], "note": "合符釜山，大会诸侯，确立共主地位"},
]
for e in events:
    entities["Event"].append({
        "@id": e["@id"],
        "@type": "hist:Event",
        "hist:name": e["name"],
        "hist:eventType": e["eventType"],
        "hist:location": e["location"],
        "hist:participants": e["participants"],
        "hist:note": e["note"]
    })

# 注疏实体：从三家注里提取所有注
annot_count = 0
for s in wudi_data['sentences']:
    for ann in s.get('annotations', []):
        entities["Annotation"].append({
            "@id": f"ann-shiji-wudibenji-{s['id']}-{annot_count}",
            "@type": "hist:Annotation",
            "hist:annotatesSentence": f"sent-shiji-wudibenji-{s['id']}",
            "hist:annotationType": ann.get('type', '释义'),
            "hist:annotator": ann.get('annotator', '三家注'),
            "hist:content": ann['content']
        })
        annot_count += 1

print(f"ABox实体抽取完成：")
for cls, items in entities.items():
    print(f"  {cls}: {len(items)} 条")

# ========== RBox 关系三元组 ==========
relations = []

# 人物血缘关系
blood_relations = [
    ("person-shaodian-prehistoric", "hist:fatherOf", "person-huangdi-prehistoric"),
    ("person-huangdi-prehistoric", "hist:fatherOf", "person-changyi-prehistoric"),
    ("person-huangdi-prehistoric", "hist:fatherOf", "person-xuanxiao-prehistoric"),
    ("person-changyi-prehistoric", "hist:fatherOf", "person-zhuanxu-prehistoric"),
    ("person-xuanxiao-prehistoric", "hist:fatherOf", "person-qiaoji-prehistoric"),
    ("person-qiaoji-prehistoric", "hist:fatherOf", "person-diku-prehistoric"),
    ("person-diku-prehistoric", "hist:fatherOf", "person-yao-prehistoric"),
    ("person-gusou-prehistoric", "hist:fatherOf", "person-shun-prehistoric"),
]
for s, p, o in blood_relations:
    relations.append({"@type": "hist:RelationTriple", "subject": s, "predicate": p, "object": o})

# 事件-人物关系
for e in events:
    for p in e['participants']:
        relations.append({"@type": "hist:RelationTriple", "subject": p, "predicate": "hist:participatedIn", "object": e["@id"]})
    relations.append({"@type": "hist:RelationTriple", "subject": e["@id"], "predicate": "hist:tookPlaceAt", "object": e["location"]})

# 作者关系
relations.append({"subject": "book-shiji", "predicate": "hist:authoredBy", "object": "person-simaqian-westernhan"})
relations.append({"subject": "chapter-shiji-wudibenji", "predicate": "hist:belongsToBook", "object": "book-shiji"})

# 注疏-注者关系
for ann in entities["Annotation"][:50]: # 加前50条示例
    annotator_id = "person-peiyin-liusong" if ann["hist:annotator"] == "裴骃" else \
                   "person-simazhen-tang" if ann["hist:annotator"] == "司马贞" else \
                   "person-zhangshoujie-tang" if ann["hist:annotator"] == "张守节" else "person-simaqian-westernhan"
    relations.append({"subject": ann["@id"], "predicate": "hist:authoredBy", "object": annotator_id})
    relations.append({"subject": ann["@id"], "predicate": "hist:annotates", "object": ann["hist:annotatesSentence"]})

print(f"RBox三元组构建完成：{len(relations)} 条")

# ========== 保存本体数据 ==========
ontology_output = {
    "@context": "http://history.local/ontology#",
    "@type": "hist:OntologyDataset",
    "book": "史记·五帝本纪",
    "tboxReference": "../tbox-schema.json",
    "entities": entities,
    "relations": relations,
    "stats": {
        "totalEntities": sum(len(v) for v in entities.values()),
        "totalRelations": len(relations),
        "totalAnnotations": annot_count
    }
}

with open('/home/user/workspace/17521090448082856013/history-site/data/ontology/shiji/wudi-benji.json', 'w', encoding='utf-8') as f:
    json.dump(ontology_output, f, ensure_ascii=False, indent=2)

print(f"\n史记·五帝本纪本体数据已保存：")
print(f"总实体数：{ontology_output['stats']['totalEntities']}")
print(f"总三元组：{ontology_output['stats']['totalRelations']}")
print(f"注疏数：{annot_count}")
