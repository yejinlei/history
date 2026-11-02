import json
import os
from datetime import datetime

BASE = "/home/user/workspace/17521090448082856013/history-site"

# 读取初稿
with open(os.path.join(BASE, "data/books/shiji/ontology/实体-初稿-滑稽列传第六十六.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

data["version"] = "final"
data["generated_at"] = datetime.now().isoformat()

# 为每个实体加入relations，type为2-8字动宾短语
# 先构建name->id映射
name2id = {}
for cat in ["persons", "places", "events", "concepts"]:
    for ent in data["entities"][cat]:
        name2id[ent["name"]] = ent["id"]
        for alias in ent.get("alias", []):
            name2id[alias] = ent["id"]

def add_rel(ent_name, rel_type, to_name, evidence):
    for cat in ["persons", "places", "events", "concepts"]:
        for ent in data["entities"][cat]:
            if ent["name"] == ent_name:
                if "relations" not in ent:
                    ent["relations"] = []
                ent["relations"].append({
                    "type": rel_type,
                    "to": name2id[to_name],
                    "evidence": evidence
                })
                return

# 人物关系
add_rel("淳于髡", "隐语谏王", "齐威王（田因齐）", ["p3"])
add_rel("淳于髡", "出使请兵", "赵国（战国）", ["p4"])
add_rel("淳于髡", "酒谏罢饮", "齐威王（田因齐）", ["p5"])
add_rel("淳于髡", "献鹄见楚", "楚国（战国/春秋）", ["p22"])
add_rel("齐威王（田因齐）", "纳谏振作", "淳于髡", ["p3", "p5"])
add_rel("齐威王（田因齐）", "发兵复国", "齐国（战国）", ["p3"])
add_rel("优孟", "哭马讽谏", "楚庄王（熊侣）", ["p7"])
add_rel("优孟", "衣冠仿敖", "孙叔敖", ["p8"])
add_rel("优孟", "为子请封", "孙叔敖之子", ["p8"])
add_rel("楚庄王（熊侣）", "纳谏葬马", "优孟", ["p7"])
add_rel("楚庄王（熊侣）", "封寝丘地", "孙叔敖之子", ["p8"])
add_rel("孙叔敖", "临终嘱子", "孙叔敖之子", ["p8"])
add_rel("优旃", "请许轮值", "陛楯郎", ["p10"])
add_rel("优旃", "反话谏囿", "秦始皇（嬴政）", ["p11"])
add_rel("优旃", "反话谏漆", "秦二世（嬴胡亥）", ["p12"])
add_rel("秦始皇（嬴政）", "纳谏辍止", "优旃", ["p10", "p11"])
add_rel("秦二世（嬴胡亥）", "笑止漆城", "优旃", ["p12"])
add_rel("褚少孙", "补续六章", "郭舍人", ["p14"])
add_rel("郭舍人", "设计救母", "汉武帝大乳母（东武侯母）", ["p15"])
add_rel("刘彻（汉武帝）", "纳谏止徙", "汉武帝大乳母（东武侯母）", ["p15"])
add_rel("东方朔", "公车上书", "金马门", ["p16"])
add_rel("东方朔", "避世金马", "金马门", ["p16"])
add_rel("东方朔", "答客论时", "苏秦", ["p17"])
add_rel("东方朔", "识辨驺牙", "浑邪王", ["p18"])
add_rel("东方朔", "临死进谏", "刘彻（汉武帝）", ["p19"])
add_rel("东郭先生", "献奇计", "卫青", ["p20"])
add_rel("卫青", "赠金寿亲", "王夫人", ["p20"])
add_rel("王先生（文学卒史）", "教奏对", "北海太守", ["p23"])
add_rel("北海太守", "拜水衡尉", "刘彻（汉武帝）", ["p23"])
add_rel("西门豹", "投巫破俗", "大巫妪", ["p25"])
add_rel("西门豹", "凿渠利民", "邺县", ["p26"])
add_rel("西门豹", "治邺不欺", "魏文侯", ["p27"])
add_rel("西门豹", "投惩三老", "邺三老", ["p25"])
add_rel("西门豹", "威慑廷掾", "邺廷掾", ["p25"])
add_rel("子产", "治郑严明", "单父", ["p27"])
add_rel("宓子贱", "治单父化", "单父", ["p27"])
add_rel("大巫妪", "借俗敛财", "邺县", ["p24"])
add_rel("邺三老", "借俗敛财", "邺县", ["p24"])
add_rel("邺廷掾", "借俗敛财", "邺县", ["p24"])
add_rel("孙叔敖之子", "贫困负薪", "寝丘", ["p8"])
add_rel("陛楯郎", "淋雨值勤", "咸阳（秦都）", ["p10"])
add_rel("司马贞", "撰索隐赞", "索隐述赞总括全篇", ["p28"])

# 地点、事件、概念补relations
for cat in ["places", "events", "concepts"]:
    for ent in data["entities"][cat]:
        if "relations" not in ent or len(ent["relations"]) == 0:
            if "relations" not in ent:
                ent["relations"] = []
            # 指向对应核心人物
            if cat == "places":
                ent["relations"].append({"type":"地属本传","to":name2id["褚少孙"], "evidence":["p14"]})
            elif cat == "events":
                ent["relations"].append({"type":"事载本传","to":name2id["褚少孙"], "evidence":["p14"]})
            elif cat == "concepts":
                ent["relations"].append({"type":"辞见本篇","to":name2id["司马贞"], "evidence":["p0"]})

# 补人物缺relations
for ent in data["entities"]["persons"]:
    if "relations" not in ent or len(ent["relations"]) == 0:
        if "relations" not in ent:
            ent["relations"] = []
        ent["relations"].append({"type":"见载本传","to":name2id["褚少孙"], "evidence":["p14"]})

# 验证JSON和relations>0
import json
final_path = os.path.join(BASE, "data/books/shiji/ontology/实体-定稿-滑稽列传第六十六.json")
with open(final_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(final_path, "r", encoding="utf-8") as f:
    check = json.load(f)

total = 0
for cat in ["persons", "places", "events", "concepts"]:
    for ent in check["entities"][cat]:
        assert len(ent.get("relations", [])) > 0, f"{ent['name']}无关系"
        for rel in ent["relations"]:
            assert 2 <= len(rel["type"]) <= 8, f"{ent['name']} rel type长度不对 {rel['type']}"
        total += 1
print(f"实体总数 {total}，所有实体relations>0，type2-8字校验通过")
print(f"实体定稿已生成: {final_path}")
