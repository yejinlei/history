# -*- coding: utf-8 -*-
"""步骤7：实体定稿（添加relations）"""
import json, os, re

ROOT = "/home/user/workspace/17521090448082856013/history-site"
ONT_DIR = os.path.join(ROOT, "data/books/shiji/ontology")
CHAPTER_ID = "shiji-滑稽列傳第六十六"
CHAPTER_TITLE = "滑稽列传第六十六"
TODAY = "2026-11-02"

draft_path = os.path.join(ONT_DIR, "实体-初稿-滑稽列传第六十六.json")
with open(draft_path, encoding="utf-8") as f:
    draft = json.load(f)

# 构建id集合以校验
id_set = set()
for cat in ["persons","places","events","concepts"]:
    for ent in draft["entities"][cat]:
        id_set.add(ent["id"])

# relations: list of dict
R = [
    # 孔子论六艺
    {"from":"p_hj_001","type":"论六艺治道","to":"c_hj_002","evidence":["p1"]},
    {"from":"p_hj_002","type":"标举谈言解纷","to":"c_hj_003","evidence":["p2"]},
    # 淳于髡-齐威王
    {"from":"p_hj_003","type":"以隐语谏威王","to":"p_hj_004","evidence":["p3"]},
    {"from":"p_hj_004","type":"一飞冲天强国","to":"c_hj_007","evidence":["p3"]},
    {"from":"p_hj_003","type":"以大鸟为隐","to":"c_hj_004","evidence":["p3"]},
    {"from":"p_hj_004","type":"朝诸县令长","to":"p_hj_005","evidence":["p3"]},
    {"from":"p_hj_003","type":"仰天大笑请救","to":"p_hj_004","evidence":["p4"]},
    {"from":"p_hj_003","type":"笑禳田者喻礼薄","to":"c_hj_009","evidence":["p4"]},
    {"from":"p_hj_003","type":"所持狭所欲奢","to":"c_hj_010","evidence":["p4"]},
    {"from":"p_hj_006","type":"发精兵十万救齐","to":"pl_hj_001","evidence":["p4"]},
    {"from":"p_hj_002","type":"记楚军夜引去","to":"pl_hj_002","evidence":["p4"]},
    {"from":"p_hj_003","type":"以饮酒讽谏长夜","to":"c_hj_011","evidence":["p5"]},
    {"from":"p_hj_004","type":"罢长夜之饮","to":"c_hj_006","evidence":["p5"]},
    {"from":"p_hj_004","type":"拜髡主客","to":"p_hj_003","evidence":["p5"]},
    # 优孟
    {"from":"p_hj_007","type":"谏贱人贵马","to":"p_hj_008","evidence":["p7"]},
    {"from":"p_hj_007","type":"请六畜葬马","to":"c_hj_014","evidence":["p7"]},
    {"from":"p_hj_008","type":"以马属太官","to":"pl_hj_024","evidence":["p7"]},
    {"from":"p_hj_009","type":"临终嘱子乞封","to":"p_hj_010","evidence":["p8"]},
    {"from":"p_hj_007","type":"着衣冠效孙叔敖","to":"c_hj_015","evidence":["p8"]},
    {"from":"p_hj_008","type":"欲封优孟为相","to":"p_hj_007","evidence":["p8"]},
    {"from":"p_hj_007","type":"歌廉吏不可为","to":"p_hj_008","evidence":["p8"]},
    {"from":"p_hj_008","type":"封寝丘四百户","to":"p_hj_010","evidence":["p8"]},
    {"from":"p_hj_010","type":"奉孙叔敖祀","to":"p_hj_009","evidence":["p8"]},
    # 优旃
    {"from":"p_hj_011","type":"哀陛楯淋雨","to":"p_hj_045","evidence":["p10"]},
    {"from":"p_hj_011","type":"临槛大呼陛楯","to":"p_hj_045","evidence":["p10"]},
    {"from":"p_hj_012","type":"使陛楯半相代","to":"c_hj_016","evidence":["p10"]},
    {"from":"p_hj_011","type":"反语谏扩苑囿","to":"pl_hj_027","evidence":["p11"]},
    {"from":"p_hj_011","type":"谓麋鹿可触寇","to":"p_hj_012","evidence":["p11"]},
    {"from":"p_hj_012","type":"辍止扩苑囿","to":"p_hj_011","evidence":["p11"]},
    {"from":"p_hj_013","type":"欲漆咸阳城","to":"pl_hj_028","evidence":["p12"]},
    {"from":"p_hj_011","type":"反语谏漆城","to":"c_hj_018","evidence":["p12"]},
    {"from":"p_hj_013","type":"笑止漆城之役","to":"p_hj_011","evidence":["p12"]},
    # 太史公总赞
    {"from":"p_hj_002","type":"总赞三俳奇伟","to":"e_hj_016","evidence":["p13"]},
    # 褚少孙补
    {"from":"p_hj_014","type":"补六章滑稽","to":"e_hj_017","evidence":["p14"]},
    {"from":"p_hj_014","type":"以经术为郎","to":"c_hj_019","evidence":["p14"]},
    # 郭舍人
    {"from":"p_hj_015","type":"设计骂乳母","to":"p_hj_016","evidence":["p15"]},
    {"from":"p_hj_016","type":"得马游卿赐帛","to":"p_hj_017","evidence":["p15"]},
    {"from":"p_hj_028","type":"怜乳母止迁徙","to":"p_hj_016","evidence":["p15"]},
    {"from":"p_hj_028","type":"罚谪谮乳母者","to":"p_hj_015","evidence":["p15"]},
    # 东方朔
    {"from":"p_hj_018","type":"公车上书三千牍","to":"c_hj_020","evidence":["p16"]},
    {"from":"p_hj_018","type":"拜为郎官侍中","to":"p_hj_028","evidence":["p16"]},
    {"from":"p_hj_018","type":"怀肉污衣","to":"c_hj_022","evidence":["p16"]},
    {"from":"p_hj_018","type":"岁更娶妇号狂","to":"c_hj_022","evidence":["p16"]},
    {"from":"p_hj_018","type":"避世金马门","to":"c_hj_023","evidence":["p16"]},
    {"from":"p_hj_018","type":"倡陆沈于俗","to":"c_hj_040","evidence":["p16"]},
    {"from":"p_hj_047","type":"诘难东方朔","to":"p_hj_018","evidence":["p17"]},
    {"from":"p_hj_018","type":"答彼一时此一时","to":"c_hj_024","evidence":["p17"]},
    {"from":"p_hj_018","type":"引鼓钟鹤鸣论修身","to":"c_hj_028","evidence":["p17"]},
    {"from":"p_hj_018","type":"识驺牙预言归义","to":"c_hj_029","evidence":["p18"]},
    {"from":"p_hj_027","type":"率十万众降汉","to":"p_hj_028","evidence":["p18"]},
    {"from":"p_hj_028","type":"厚赐东方朔钱财","to":"p_hj_018","evidence":["p18"]},
    {"from":"p_hj_018","type":"临终谏远巧佞","to":"c_hj_030","evidence":["p19"]},
    {"from":"p_hj_018","type":"引青蝇诗谏","to":"p_hj_028","evidence":["p19"]},
    {"from":"p_hj_028","type":"怪东方朔善言","to":"p_hj_018","evidence":["p19"]},
    # 东郭先生/卫青
    {"from":"p_hj_029","type":"出击匈奴至余吾","to":"pl_hj_022","evidence":["p20"]},
    {"from":"p_hj_031","type":"当道遮卫青车","to":"p_hj_029","evidence":["p20"]},
    {"from":"p_hj_031","type":"教献金王夫人亲","to":"p_hj_029","evidence":["p20"]},
    {"from":"p_hj_029","type":"以五百金为王夫人寿","to":"p_hj_032","evidence":["p20"]},
    {"from":"p_hj_028","type":"召见东郭拜都尉","to":"p_hj_031","evidence":["p20"]},
    {"from":"p_hj_031","type":"久贫困衣褐怀宝","to":"c_hj_031","evidence":["p20"]},
    {"from":"p_hj_031","type":"显名证相士失贫","to":"c_hj_032","evidence":["p20"]},
    # 王夫人
    {"from":"p_hj_032","type":"病请子王洛阳","to":"pl_hj_013","evidence":["p21"]},
    {"from":"p_hj_028","type":"拒洛阳因武库敖仓","to":"pl_hj_014","evidence":["p21"]},
    {"from":"p_hj_028","type":"封子为齐王","to":"p_hj_033","evidence":["p21"]},
    # 献鹄
    {"from":"p_hj_003","type":"献鹄道飞空笼","to":"p_hj_034","evidence":["p22"]},
    {"from":"p_hj_003","type":"以空笼造诈成辞","to":"p_hj_034","evidence":["p22"]},
    {"from":"p_hj_034","type":"厚赐淳于髡信士","to":"p_hj_003","evidence":["p22"]},
    # 王先生
    {"from":"p_hj_028","type":"征北海太守诣行在","to":"p_hj_035","evidence":["p23"]},
    {"from":"p_hj_036","type":"教对陛下神武威","to":"p_hj_035","evidence":["p23"]},
    {"from":"p_hj_035","type":"以神武威对武帝","to":"p_hj_028","evidence":["p23"]},
    {"from":"p_hj_028","type":"拜王先生水衡丞","to":"p_hj_036","evidence":["p23"]},
    {"from":"p_hj_028","type":"拜北海守水衡都尉","to":"p_hj_035","evidence":["p23"]},
    {"from":"p_hj_036","type":"引美言市尊行加人","to":"c_hj_033","evidence":["p23"]},
    # 西门豹
    {"from":"p_hj_038","type":"任西门豹为邺令","to":"p_hj_037","evidence":["p24"]},
    {"from":"p_hj_037","type":"至邺问民疾苦","to":"pl_hj_017","evidence":["p24"]},
    {"from":"p_hj_048","type":"告河伯娶妇苦","to":"c_hj_034","evidence":["p24"]},
    {"from":"p_hj_039","type":"借河伯娶妇敛财","to":"p_hj_041","evidence":["p24"]},
    {"from":"p_hj_037","type":"约期送河伯妇","to":"p_hj_041","evidence":["p24"]},
    {"from":"p_hj_037","type":"投巫妪于河","to":"p_hj_041","evidence":["p25"]},
    {"from":"p_hj_037","type":"投巫弟子三人","to":"p_hj_042","evidence":["p25"]},
    {"from":"p_hj_037","type":"投三老于河","to":"p_hj_039","evidence":["p25"]},
    {"from":"p_hj_037","type":"簪笔磬折待河伯","to":"c_hj_036","evidence":["p25"]},
    {"from":"p_hj_040","type":"叩头流血求饶","to":"p_hj_037","evidence":["p25"]},
    {"from":"p_hj_037","type":"止河伯娶妇恶俗","to":"c_hj_034","evidence":["p25"]},
    {"from":"p_hj_037","type":"发民凿十二渠","to":"pl_hj_018","evidence":["p26"]},
    {"from":"p_hj_037","type":"引漳水灌民田","to":"pl_hj_018","evidence":["p26"]},
    {"from":"p_hj_037","type":"论民可乐成难虑始","to":"c_hj_037","evidence":["p26"]},
    {"from":"p_hj_037","type":"泽流后世名闻天下","to":"c_hj_039","evidence":["p26"]},
    # 三不欺
    {"from":"p_hj_043","type":"治郑民不能欺","to":"pl_hj_021","evidence":["p27"]},
    {"from":"p_hj_044","type":"治单父民不忍欺","to":"pl_hj_020","evidence":["p27"]},
    {"from":"p_hj_037","type":"治邺民不敢欺","to":"pl_hj_017","evidence":["p27"]},
]

# 校验
bad = []
for r in R:
    if r["from"] not in id_set:
        bad.append(("from",r))
    if r["to"] not in id_set:
        bad.append(("to",r))
    if not (2 <= len(r["type"]) <= 8):
        bad.append(("len",r))
    for pid in r["evidence"]:
        m = re.match(r"p\d+$",pid)
        if not m:
            bad.append(("pid",r)); break
        n=int(pid[1:])
        if n>28:
            bad.append(("pidoob",r)); break

import re
print("relations数:", len(R))
print("bad:", bad[:5])

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
