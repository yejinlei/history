import json
import re

# 加载实体定稿
with open('data/books/shiji/ontology/实体-定稿-西南夷列传第五十六.json', 'r', encoding='utf-8') as f:
    ent_data = json.load(f)

# 加载底本
with open('data/books/shiji/text/shiji-西南夷列傳第五十六.json', 'r', encoding='utf-8') as f:
    text_data = json.load(f)

# 直接用繁体原名匹配：直接从底本提取实体繁体原名
all_mentions = []
# 核心实体繁简对应列表
name_pairs = [
    # persons
    ("莊蹻", "庄蹻", "persons"),
    ("楚莊王", "楚庄王", "persons"),
    ("常頞", "常頞", "persons"),
    ("王恢", "王恢", "persons"),
    ("唐蒙", "唐蒙", "persons"),
    ("郢", "东越王郢", "persons"),
    ("多同", "多同（夜郎侯）", "persons"),
    ("夜郎侯", "多同（夜郎侯）", "persons"),
    ("司馬相如", "司马相如", "persons"),
    ("公孫弘", "公孙弘", "persons"),
    ("張騫", "张骞（博望侯）", "persons"),
    ("博望侯", "张骞（博望侯）", "persons"),
    ("王然于", "王然于", "persons"),
    ("柏始昌", "柏始昌", "persons"),
    ("呂越人", "吕越人", "persons"),
    ("嘗羌", "尝羌（滇王）", "persons"),
    ("滇王", "尝羌（滇王）", "persons"),
    ("馳義侯", "驰义侯", "persons"),
    ("且蘭君", "且兰君", "persons"),
    ("邛君", "邛君", "persons"),
    ("筰侯", "筰侯", "persons"),
    ("上", "刘彻（汉武帝）", "persons"),
    ("天子", "刘彻（汉武帝）", "persons"),
    # places
    ("西南夷", "西南夷", "places"),
    ("夜郎", "夜郎", "places"),
    ("靡莫", "靡莫", "places"),
    ("滇", "滇", "places"),
    ("卭都", "邛都", "places"),
    ("邛都", "邛都", "places"),
    ("同師", "同师", "places"),
    ("楪榆", "楪榆", "places"),
    ("嶲", "嶲", "places"),
    ("昆明", "昆明（夷）", "places"),
    ("徙", "徙", "places"),
    ("筰都", "筰都", "places"),
    ("冉駹", "冉駹", "places"),
    ("白馬", "白马", "places"),
    ("巴蜀", "巴蜀", "places"),
    ("黔中", "黔中郡", "places"),
    ("滇池", "滇池", "places"),
    ("五尺道", "五尺道", "places"),
    ("蜀故徼", "蜀故徼", "places"),
    ("東越", "东越", "places"),
    ("番陽", "番阳", "places"),
    ("南越", "南越", "places"),
    ("䍧柯江", "牂柯江", "places"),
    ("番禺", "番禺", "places"),
    ("長安", "长安", "places"),
    ("長沙", "长沙（国）", "places"),
    ("豫章", "豫章郡", "places"),
    ("筰關", "筰关", "places"),
    ("犍爲", "犍为郡", "places"),
    ("僰道", "僰道", "places"),
    ("廣漢", "广汉郡", "places"),
    ("朔方", "朔方郡", "places"),
    ("大夏", "大夏", "places"),
    ("身毒國", "身毒国", "places"),
    ("且蘭", "且兰", "places"),
    ("䍧柯郡", "牂柯郡", "places"),
    ("越嶲郡", "越嶲郡", "places"),
    ("沈犂郡", "沈犁郡", "places"),
    ("汶山郡", "汶山郡", "places"),
    ("武都郡", "武都郡", "places"),
    ("勞𣹰", "劳𣹰", "places"),
    ("益州郡", "益州郡", "places"),
    ("匈奴", "匈奴", "places"),
    # events
    ("莊蹻王滇", "庄蹻王滇", "events"),
    ("五尺道", "秦开五尺道", "events"),
    ("夜郎自大", "滇王夜郎问汉孰大", "events"),
    # concepts
    ("魋結", "魋结（椎髻）", "concepts"),
    ("編髮", "编发", "concepts"),
    ("枸醬", "枸酱", "concepts"),
    ("黃屋左纛", "黄屋左纛", "concepts"),
    ("夜郎自大", "夜郎自大", "concepts"),
    ("七郡", "西南夷七郡", "concepts")
]

for trad, can, cat in name_pairs:
    all_mentions.append((trad, can, cat))

# 去重
all_mentions = list(set(all_mentions))
# 按长度降序匹配，优先匹配长名称
all_mentions.sort(key=lambda x: -len(x[0]))

paragraphs = []
for p in text_data['paragraphs']:
    pid = p['id'].split(':')[-1]
    text = p['text']
    # 移除注号标记用于匹配（⟦数字⟧）
    clean_text = re.sub(r'⟦\d+⟧', '', text)
    
    mentions = []
    matched_spans = set()
    
    for name, canonical, cat in all_mentions:
        if not name or len(name) < 1:
            continue
        # 找所有出现位置
        start = 0
        while True:
            idx = clean_text.find(name, start)
            if idx == -1:
                break
            # 检查是否与已有span重叠
            overlap = False
            for s, e in matched_spans:
                if not (idx + len(name) <= s or idx >= e):
                    overlap = True
                    break
            if not overlap:
                mentions.append({
                    "start": idx,
                    "end": idx + len(name),
                    "name": canonical,
                    "category": cat
                })
                matched_spans.add((idx, idx + len(name)))
            start = idx + 1
    
    # 按start排序
    mentions.sort(key=lambda x: x['start'])
    
    paragraphs.append({
        "para_id": pid,
        "text": text,
        "mentions": mentions
    })

# 构建标注文件
annotation = {
    "book_id": "shiji",
    "chapter_id": "56",
    "chapter_title": "西南夷列传第五十六",
    "version": "final",
    "generated_at": "2026-11-02T05:53:27.726863+08:00",
    "paragraphs": paragraphs
}

# 统计
total_mentions = sum(len(p['mentions']) for p in paragraphs)
print(f"标注完成，共{len(paragraphs)}段，{total_mentions}处提及")

with open('data/books/shiji/ontology/实体标注-西南夷列传第五十六.json', 'w', encoding='utf-8') as f:
    json.dump(annotation, f, ensure_ascii=False, indent=2)

print("实体标注-西南夷列传第五十六.json 已生成")
