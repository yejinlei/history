# -*- coding: utf-8 -*-
"""步骤7：基于现有实体初稿补齐遗漏实体后生成定稿（含relations）"""
import json, os, re

ROOT = "/home/user/workspace/17521090448082856013/history-site"
ONT_DIR = os.path.join(ROOT, "data/books/shiji/ontology")
CHAPTER_ID = "shiji-滑稽列傳第六十六"
CHAPTER_TITLE = "滑稽列传第六十六"
TODAY = "2026-11-02"

draft_path = os.path.join(ONT_DIR, "实体-初稿-滑稽列传第六十六.json")
with open(draft_path, encoding="utf-8") as f:
    draft = json.load(f)

# 补充缺失实体
extra_persons = [
    {"id":"person_039","name":"孔丘（孔子）","alias":["孔子"],
     "note":"儒家创始人，此篇引其言「六艺于治一也」开宗明义。","evidence":["p1"]},
    {"id":"person_040","name":"司马迁（太史公）","alias":["太史公"],
     "note":"《史记》作者，本篇序论及太史公论赞作者。","evidence":["p2","p13"]},
    {"id":"person_041","name":"姬昌（周文王）","alias":["文王"],
     "note":"周文王姬昌，遇姜太公，开创周朝基业。","evidence":["p17"]},
    {"id":"person_042","name":"楚王（献鹄事）","alias":["楚王"],
     "note":"褚补献鹄章中的楚王，厚赐献空笼的淳于髡。","evidence":["p22"]},
    {"id":"person_043","name":"巫弟子","alias":["弟子","弟子女"],
     "note":"大巫妪的女弟子，共十人所，西门豹投三人于河。","evidence":["p25"]},
    {"id":"person_044","name":"博士诸先生","alias":["博士","諸先生","諸先生","郎"],
     "note":"汉武帝时朝廷博士、郎官，诘难东方朔，被答得默然无以应。","evidence":["p16","p17","p18"]},
]
extra_places = [
    {"id":"place_020","name":"武库","alias":["武庫"],
     "note":"洛阳国家兵器大仓库。","evidence":["p21"]},
    {"id":"place_021","name":"敖仓","alias":["敖倉"],
     "note":"荥阳敖山大粮仓，天下粮储重地。","evidence":["p21"]},
    {"id":"place_022","name":"漳河（邺）","alias":["河水"],
     "note":"即漳水，西门豹引河水灌田。","evidence":["p26"]},
    {"id":"place_023","name":"驰道","alias":["馳道"],
     "note":"皇帝专用御道，西门豹十二渠横跨之。","evidence":["p15","p26"]},
]
extra_concepts = [
    {"id":"concept_031","name":"讽谏","alias":["諷諫"],
     "note":"不直言过失而以委婉言辞劝谏，滑稽家主要手法。","evidence":["p5","p7"]},
    {"id":"concept_032","name":"覆盂之安","alias":["安於覆盂"],
     "note":"像倒扣的盂一样安稳，喻天下一统太平。","evidence":["p17"]},
    {"id":"concept_033","name":"营营青蝇","alias":["營營青蠅"],
     "note":"出自《诗·青蝇》，以苍蝇喻谗人。","evidence":["p19"]},
    {"id":"concept_034","name":"巧佞谗言","alias":["巧佞","讒言"],
     "note":"巧言谄媚与谗言，东方朔临终所谏。","evidence":["p19"]},
    {"id":"concept_035","name":"以其人之道还治","alias":[],"note":"西门豹投巫妪于河，以其道还治其身。","evidence":["p25"]},
]

draft["entities"]["persons"].extend(extra_persons)
draft["entities"]["places"].extend(extra_places)
draft["entities"]["concepts"].extend(extra_concepts)

# 构建id_set
id_set = set()
for cat in ["persons","places","events","concepts"]:
    for ent in draft["entities"][cat]:
        id_set.add(ent["id"])

# relations - 使用现有id
R = [
    {"from":"person_039","type":"论六艺治道","to":"concept_001","evidence":["p1"]},
    {"from":"person_040","type":"标举谈言解纷","to":"concept_002","evidence":["p2"]},
    {"from":"person_000","type":"以隐语谏威王","to":"person_001","evidence":["p3"]},
    {"from":"person_001","type":"一飞冲天强国","to":"concept_005","evidence":["p3"]},
    {"from":"person_000","type":"仰天大笑请救","to":"person_001","evidence":["p4"]},
    {"from":"person_000","type":"笑禳田喻礼薄","to":"person_001","evidence":["p4"]},
    {"from":"person_026","type":"发精兵十万救齐","to":"place_000","evidence":["p4"]},
    {"from":"person_000","type":"以饮酒讽谏长夜","to":"concept_027","evidence":["p5"]},
    {"from":"person_001","type":"罢长夜之饮","to":"person_000","evidence":["p5"]},
    {"from":"person_001","type":"拜髡主客","to":"concept_020","evidence":["p5"]},
    {"from":"person_002","type":"谏贱人贵马","to":"person_003","evidence":["p7"]},
    {"from":"person_002","type":"请六畜葬马","to":"concept_024","evidence":["p7"]},
    {"from":"person_003","type":"以马属太官","to":"concept_022","evidence":["p7"]},
    {"from":"person_004","type":"临终嘱子乞封","to":"person_036","evidence":["p8"]},
    {"from":"person_002","type":"着衣冠效孙叔敖","to":"concept_008","evidence":["p8"]},
    {"from":"person_003","type":"欲封优孟为相","to":"person_002","evidence":["p8"]},
    {"from":"person_002","type":"歌廉吏不可为","to":"person_003","evidence":["p8"]},
    {"from":"person_003","type":"封寝丘四百户","to":"person_036","evidence":["p8"]},
    {"from":"person_036","type":"奉孙叔敖祀","to":"person_004","evidence":["p8"]},
    {"from":"person_005","type":"哀陛楯淋雨","to":"person_037","evidence":["p10"]},
    {"from":"person_005","type":"临槛大呼陛楯","to":"person_037","evidence":["p10"]},
    {"from":"person_006","type":"使陛楯半相代","to":"person_037","evidence":["p10"]},
    {"from":"person_005","type":"反语谏扩苑囿","to":"person_006","evidence":["p11"]},
    {"from":"person_006","type":"辍止扩苑囿","to":"person_005","evidence":["p11"]},
    {"from":"person_007","type":"欲漆咸阳城","to":"person_005","evidence":["p12"]},
    {"from":"person_005","type":"反语谏漆城","to":"concept_010","evidence":["p12"]},
    {"from":"person_007","type":"笑止漆城之役","to":"person_005","evidence":["p12"]},
    {"from":"person_040","type":"总赞三俳奇伟","to":"event_010","evidence":["p13"]},
    {"from":"person_008","type":"补六章滑稽","to":"event_011","evidence":["p14"]},
    {"from":"person_009","type":"设计骂乳母","to":"person_011","evidence":["p15"]},
    {"from":"person_011","type":"得马游卿赐帛","to":"person_012","evidence":["p15"]},
    {"from":"person_010","type":"怜乳母止迁徙","to":"person_011","evidence":["p15"]},
    {"from":"person_013","type":"公车上书三千牍","to":"concept_030","evidence":["p16"]},
    {"from":"person_013","type":"拜为郎官侍中","to":"person_010","evidence":["p16"]},
    {"from":"person_013","type":"岁更娶妇号狂","to":"person_010","evidence":["p16"]},
    {"from":"person_013","type":"避世金马门","to":"concept_011","evidence":["p16"]},
    {"from":"person_044","type":"诘难东方朔","to":"person_013","evidence":["p17"]},
    {"from":"person_013","type":"答彼一时此一时","to":"concept_012","evidence":["p17"]},
    {"from":"person_020","type":"七十二年逢文王","to":"person_041","evidence":["p17"]},
    {"from":"person_013","type":"识驺牙预言归义","to":"concept_025","evidence":["p18"]},
    {"from":"person_021","type":"率十万众降汉","to":"person_010","evidence":["p18"]},
    {"from":"person_010","type":"厚赐东方朔钱财","to":"person_013","evidence":["p18"]},
    {"from":"person_013","type":"临终谏远巧佞","to":"concept_034","evidence":["p19"]},
    {"from":"person_013","type":"引青蝇诗谏","to":"concept_033","evidence":["p19"]},
    {"from":"person_022","type":"出击匈奴至余吾","to":"place_014","evidence":["p20"]},
    {"from":"person_024","type":"教献金王夫人亲","to":"person_022","evidence":["p20"]},
    {"from":"person_022","type":"以五百金为寿","to":"person_025","evidence":["p20"]},
    {"from":"person_010","type":"召见东郭拜都尉","to":"person_024","evidence":["p20"]},
    {"from":"person_024","type":"久贫困衣褐怀宝","to":"concept_014","evidence":["p20"]},
    {"from":"person_025","type":"病请子王洛阳","to":"place_015","evidence":["p21"]},
    {"from":"person_010","type":"拒洛阳因武库敖仓","to":"place_020","evidence":["p21"]},
    {"from":"person_010","type":"封子为齐王","to":"place_016","evidence":["p21"]},
    {"from":"person_000","type":"献鹄道飞空笼","to":"person_042","evidence":["p22"]},
    {"from":"person_042","type":"厚赐淳于髡信士","to":"person_000","evidence":["p22"]},
    {"from":"person_010","type":"征北海太守诣行在","to":"person_028","evidence":["p23"]},
    {"from":"person_027","type":"教对陛下神武威","to":"person_028","evidence":["p23"]},
    {"from":"person_010","type":"拜王先生水衡丞","to":"person_027","evidence":["p23"]},
    {"from":"person_010","type":"拜北海守水衡都尉","to":"concept_023","evidence":["p23"]},
    {"from":"person_027","type":"引美言市尊行加人","to":"concept_019","evidence":["p23"]},
    {"from":"person_029","type":"任西门豹为邺令","to":"person_030","evidence":["p24"]},
    {"from":"person_030","type":"至邺问民疾苦","to":"place_012","evidence":["p24"]},
    {"from":"person_030","type":"投巫妪于河","to":"person_035","evidence":["p25"]},
    {"from":"person_030","type":"投巫弟子三人","to":"person_043","evidence":["p25"]},
    {"from":"person_030","type":"投三老于河","to":"person_033","evidence":["p25"]},
    {"from":"person_030","type":"簪笔磬折待河","to":"concept_029","evidence":["p25"]},
    {"from":"person_034","type":"叩头流血求饶","to":"person_030","evidence":["p25"]},
    {"from":"person_030","type":"止河伯娶妇恶俗","to":"concept_016","evidence":["p25"]},
    {"from":"person_030","type":"发民凿十二渠","to":"place_017","evidence":["p26"]},
    {"from":"person_030","type":"引漳水灌民田","to":"place_022","evidence":["p26"]},
    {"from":"person_030","type":"论民可乐成难虑始","to":"concept_017","evidence":["p26"]},
    {"from":"person_030","type":"泽流后世名闻天下","to":"place_012","evidence":["p26"]},
    {"from":"person_031","type":"治郑民不能欺","to":"person_030","evidence":["p27"]},
    {"from":"person_032","type":"治单父民不忍欺","to":"person_030","evidence":["p27"]},
    {"from":"person_030","type":"治邺民不敢欺","to":"concept_018","evidence":["p27"]},
]

bad = []
for r in R:
    if r["from"] not in id_set:
        bad.append(("from",r))
    if r["to"] not in id_set:
        bad.append(("to",r))
    if not (2 <= len(r["type"]) <= 8):
        bad.append(("len",r))
    for pid in r["evidence"]:
        if not re.match(r"p\d+$", pid):
            bad.append(("pid",r)); break
        n=int(pid[1:])
        if n>28:
            bad.append(("pidoob",r)); break

print("bad:", bad[:5] if bad else "none")
print("relations数:", len(R))

final = {
    "book_id": "shiji",
    "chapter_id": CHAPTER_ID,
    "chapter_title": CHAPTER_TITLE,
    "version": "1.0",
    "generated_at": TODAY,
    "entities": draft["entities"],
    "relations": R,
}

final_path = os.path.join(ONT_DIR, "实体-定稿-滑稽列传第六十六.json")
with open(final_path, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)
print("实体定稿 written:", final_path)
print("p/pl/e/c:", len(draft["entities"]["persons"]), len(draft["entities"]["places"]), len(draft["entities"]["events"]), len(draft["entities"]["concepts"]))
