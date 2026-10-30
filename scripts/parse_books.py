#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, json
RAW_DIR = "data/raw"
OUT_DIR = "data/texts"
os.makedirs(OUT_DIR, exist_ok=True)

# 章节名映射
SHIJI_SECTIONS = [
    ("十二本纪", [
        "五帝本纪","夏本纪","殷本纪","周本纪","秦本纪","秦始皇本纪","项羽本纪","高祖本纪","吕太后本纪","孝文本纪","孝景本纪","孝武本纪"
    ]),
    ("十表", [
        "三代世表","十二诸侯年表","六国年表","秦楚之际月表","汉兴以来诸侯王年表","高祖功臣侯者年表","惠景间侯者年表","建元以来侯者年表","建元以来王子侯者年表","汉兴以来将相名臣年表"
    ]),
    ("八书", [
        "礼书","乐书","律书","历书","天官书","封禅书","河渠书","平准书"
    ]),
    ("三十世家", [
        "吴太伯世家","齐太公世家","鲁周公世家","燕召公世家","管蔡世家","陈杞世家","卫康叔世家","宋微子世家","晋世家","楚世家","越王勾践世家","郑世家","赵世家","魏世家","韩世家","田敬仲完世家","孔子世家","陈涉世家","外戚世家","楚元王世家","荆燕世家","齐悼惠王世家","萧相国世家","曹相国世家","留侯世家","陈丞相世家","绛侯周勃世家","梁孝王世家","五宗世家","三王世家"
    ]),
    ("七十列传", [
        "伯夷列传","管晏列传","老子韩非列传","司马穰苴列传","孙子吴起列传","伍子胥列传","仲尼弟子列传","商君列传","苏秦列传","张仪列传","樗里子甘茂列传","穰侯列传","白起王翦列传","孟子荀卿列传","孟尝君列传","平原君虞卿列传","魏公子列传","春申君列传","范雎蔡泽列传","乐毅列传","廉颇蔺相如列传","田单列传","鲁仲连邹阳列传","屈原贾生列传","吕不韦列传","刺客列传","李斯列传","蒙恬列传","张耳陈馀列传","魏豹彭越列传","黥布列传","淮阴侯列传","韩信卢绾列传","田儋列传","樊郦滕灌列传","张丞相列传","郦生陆贾列传","傅靳蒯成列传","刘敬叔孙通列传","季布栾布列传","袁盎晁错列传","张释之冯唐列传","万石张叔列传","田叔列传","扁鹊仓公列传","吴王濞列传","魏其武安侯列传","韩长孺列传","李将军列传","匈奴列传","卫将军骠骑列传","平津侯主父列传","南越列传","东越列传","朝鲜列传","西南夷列传","司马相如列传","淮南衡山列传","循吏列传","汲郑列传","儒林列传","酷吏列传","大宛列传","游侠列传","佞幸列传","滑稽列传","日者列传","龟策列传","货殖列传","太史公自序"
    ]),
]

def parse_shiji():
    path = os.path.join(RAW_DIR, "shiji.txt")
    if not os.path.exists(path) or os.path.getsize(path) < 500000:
        print("shiji.txt 不完整，跳过解析")
        return []
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 按 ===== （原文） ===== 分段
    blocks = re.split(r"=====\s*（原文）\s*=====", text)
    chapters = []
    for blk in blocks:
        blk = blk.strip()
        if not blk:
            continue
        # 匹配 "第X章-XXX 原文"
        m = re.search(r"第[一二三四五六七八九十百零]+章[-－](.+?)\s*原文", blk)
        if not m:
            continue
        title = m.group(1).strip()
        # 去掉上一节/下一节
        body = re.sub(r"上一节[：:]?\s*", "", blk)
        body = re.sub(r"下一节[：:]?\s*", "", body)
        body = re.sub(r"第[一二三四五六七八九十百零]+章[-－].+?原文\s*", "", body)
        body = re.sub(r"史记-[^\n]+\n?", "", body)
        body = body.strip()
        if not body:
            continue
        
        # 确定所属部分
        section = None
        idx = 0
        for sec_name, chap_list in SHIJI_SECTIONS:
            for i, cn in enumerate(chap_list):
                if cn in title or title in cn:
                    section = sec_name
                    idx = i
                    break
            if section:
                break
        if not section:
            section = "其他"
        
        # 提取注：【...】形式的夹注
        annotations = []
        def collect_anno(match):
            full = match.group(0)
            note = match.group(1)
            annotations.append({"pos": match.start(), "note": note, "id": len(annotations)+1})
            return full
        # 先找 【xxx：xxx。】 或 【xxx】形式
        body2 = re.sub(r"【([^】]+)】", collect_anno, body)
        
        # 再处理括号注音/简单译注 (xxx)
        paren_notes = []
        def collect_paren(match):
            note = match.group(1)
            # 短的注音（含拼音或解释）
            if re.search(r"[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]", note) or "通" in note or "同" in note or "即" in note or len(note) < 20:
                paren_notes.append({"pos": match.start(), "note": note, "id": len(annotations)+len(paren_notes)+1})
            return match.group(0)
        body3 = re.sub(r"（([^）]+)）", collect_paren, body2)
        
        # 生成文件名 slug
        slug = "shiji-" + re.sub(r"[^\u4e00-\u9fa5]", "", title)
        chapters.append({
            "title": title,
            "section": section,
            "slug": slug,
            "body": body3,
            "annotations": annotations,
            "paren_notes": paren_notes,
        })
        print(f"解析：{section} - {title} -> {slug}, 注{len(annotations)+len(paren_notes)}条")
    
    # 写入json
    os.makedirs(os.path.join(OUT_DIR, "shiji"), exist_ok=True)
    with open(os.path.join(OUT_DIR, "shiji", "chapters.json"), "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)
    print(f"\n史记共解析出 {len(chapters)} 章")
    return chapters

if __name__ == "__main__":
    parse_shiji()
