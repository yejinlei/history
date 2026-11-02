import json, re
from datetime import datetime

with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/text/shiji-酷吏列傳第六十二.json','r',encoding='utf-8') as f:
    src = json.load(f)
with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/ontology/实体-定稿-酷吏列传第六十二.json','r',encoding='utf-8') as f:
    ent = json.load(f)

# 建立name->id/type索引
name2id = {}
name2type = {}
for typ in ['persons','places','events','concepts']:
    tname = typ[:-1] if typ.endswith('s') else typ
    if typ == 'persons': tname='person'
    elif typ == 'places': tname='place'
    elif typ == 'events': tname='event'
    elif typ == 'concepts': tname='concept'
    for e in ent['entities'][typ]:
        name2id[e['name']] = e['id']
        name2type[e['name']] = tname
        for a in e.get('alias',[]):
            if a and len(a)>=1:
                name2id[a] = e['id']
                name2type[a] = tname

# 增补关键词映射（简繁、异体、简称）
extra = {
    "孔子":"孔子","孔":"孔子",
    "老氏":"老子（老聃）","老子":"老子（老聃）",
    "太史公":"司马迁（太史公）","信哉是言":"司马迁（太史公）",
    "高后":"吕雉（高后）","呂氏":"吕雉（高后）",
    "侯封":"侯封",
    "鼂錯":"晁错","錯":"晁错",
    "孝景":"刘启（汉景帝）","景帝":"刘启（汉景帝）",
    "郅都":"郅都","都":"郅都","蒼鷹":"苍鹰",
    "寗成":"宁成","寧成":"宁成","成":None, # 成多义，处理时谨慎
    "孝文":"刘恒（汉文帝）","文帝":"刘恒（汉文帝）",
    "賈姬":"贾姬",
    "野彘":None,
    "竇太后":"窦太后","太后":"窦太后", # p2-p6指窦太后；p25+指王太后，按段区分
    "濟南":"济南郡","瞷氏":None,"瞷氏":"豪强",
    "條侯":"周亚夫（条侯）","亞夫":"周亚夫（条侯）",
    "臨江王":"刘荣（临江王）",
    "魏其侯":"窦婴（魏其侯）",
    "鴈門":"雁门郡",
    "匈奴":"匈奴",
    "穰":"穰县","關":"函谷关",
    "周陽由":"周阳由","由":None,
    "趙兼":"赵兼","淮南王":"刘安（淮南王）",
    "汲黯":"汲黯","黯":"汲黯",
    "司馬安":"司马安",
    "勝屠公":"胜屠公",
    "趙禹":"赵禹","禹":"赵禹",
    "斄":"斄县","亞夫":"周亚夫（条侯）",
    "張湯":"张汤","湯":"张汤",
    "杜":"杜县",
    "周陽侯":"田胜（周阳侯）",
    "武安侯":"田蚡（武安侯）",
    "陳皇后":"陈皇后（阿娇）",
    "田甲":"田甲","魚翁叔":"鱼翁叔",
    "今上":"刘彻（汉武帝）","上":None,"陛下":"刘彻（汉武帝）","天子":"刘彻（汉武帝）","皇帝":"刘彻（汉武帝）",
    "公孫弘":"公孙弘","弘":"公孙弘",
    "淮南":"刘安（淮南王）","衡山":"刘赐（衡山王）","江都":"刘建（江都王）",
    "嚴助":"严助","伍被":"伍被",
    "渾邪":"浑邪王",
    "狄山":"狄山",
    "李文":"李文",
    "魯謁居":"鲁谒居","謁居":"鲁谒居",
    "趙王":"刘彭祖（赵王）","趙":"刘彭祖（赵王）",
    "減宣":"减宣","宣":None,
    "孝文園":None,"瘞錢":None,
    "青翟":"庄青翟","丞相青翟":"庄青翟",
    "朱買臣":"朱买臣","王朝":"王朝","邊通":"边通",
    "田信":"田信",
    "安世":"张安世","張安世":"张安世",
    "湯母":"张汤母",
    "義縱":"义纵","縱":None,
    "張次公":"张次公",
    "義姁":"义姁","姁":"义姁",
    "王太后":"王太后（武帝母）",
    "脩成君子仲":"修成子仲","仲":"修成子仲",
    "穰氏":"豪强",
    "南陽":"南阳郡","河內":"河内郡","定襄":"定襄郡",
    "杜周":"杜周","周":None,
    "王溫舒":"王温舒","溫舒":None,
    "閻奉":"阎奉","楊可":"杨可","杜式":"杜式",
    "楊皆":"杨皆","麻戊":"麻戊","楊贛":"杨赣","成信":"成信",
    "尹齊":"尹齐",
    "楊僕":"杨仆","荀彘":"荀彘",
    "華成":"华成",
    "徐自爲":"徐自为","光祿":"徐自为",
    "梅免":"梅免","白政":"白政","殷中":"殷中","杜少":"杜少","徐勃":"徐勃","堅盧":"坚卢","范生":"范生",
    "范昆":"范昆","張德":"张德",
    "衞將軍青":"卫青","衛青":"卫青",
    "主父偃":"主父偃",
    "桑弘羊":"桑弘羊",
    "衞皇后":"卫皇后（卫子夫）",
    "馮當":"冯当","李貞":"李贞","彌僕":"弥仆","駱璧":"骆璧","褚廣":"褚广","無忌":"无忌","殷周":"殷周",
    "索隱":"司马贞",
    "河東":"河东郡","長安":"长安","上林":"上林苑",
    "見知":"见知法",
    "族滅":"族灭","族":"族灭",
    "舞文巧詆":"舞文巧诋",
    "不寒而慄":"不寒而栗","栗":"慄",
    "蒼鷹":"苍鹰",
    "鷹擊毛摯":"鹰击毛挚",
    "沈命法":"沈命法",
    "三尺法":"三尺法",
    "詔獄":"诏狱",
    "五銖錢":"五铢钱","白 金":"白金三品","告緡":"告缗令","鹽鐵":"盐铁官营",
    "道不拾遺":"道不拾遗",
    "虎而冠":"虎而冠",
    "束溼薪":"束湿薪",
    "問遺無所受":"问遗无所受",
    "廢格沮事":"废格沮事",
    "一意孤行":"孤立行一意而已",
}

# 段级别名规则（王太后/窦太后/「上」所属帝）
para_texts = [p['text'] for p in src['paragraphs']]
paragraphs = []
type_singleton = set()
for pi, ptxt in enumerate(para_texts):
    pid = f"p{pi}"
    ms = []
    sp = 0
    # 对每个关键词匹配
    keys = sorted(extra.keys(), key=lambda x:-len(x))
    taken = set()
    # 特别处理「上」：p1-p7 指景帝，p8+指武帝
    for m in re.finditer(r'上', ptxt):
        i=m.start()
        if i in taken: continue
        tgt = "刘启（汉景帝）" if pi<=7 else "刘彻（汉武帝）"
        if tgt in name2id:
            ms.append({"entity_id":name2id[tgt],"entity_name":tgt,"entity_type":name2type[tgt],"start":i,"end":i+1,"surface":"上"})
            taken.add(i)
    for kw in keys:
        if not kw: continue
        if kw=='上': continue
        tgt = extra[kw]
        if tgt is None: continue
        if tgt not in name2id: continue
        # 太后分野：p2-p6指窦太后，p25指王太后
        if kw=='太后':
            tgt = "窦太后" if pi<=6 else "王太后（武帝母）"
            if tgt not in name2id: continue
        for m in re.finditer(re.escape(kw), ptxt):
            i=m.start(); j=m.end()
            if any( pos in taken for pos in range(i,j) ): continue
            # 简体重字避免短字误匹配（如「都」「成」「宣」「湯」「周」等需在明确上下文）
            if len(kw)==1 and kw in "都成由宣縱溫舒周禹湯弘黯":
                # 单字简称，要求上下文是指代该人的语境（粗略：前面有姓）
                # 简单跳过单字，避免大量误匹配，只匹配长词
                continue
            ms.append({"entity_id":name2id[tgt],"entity_name":tgt,"entity_type":name2type[tgt],"start":i,"end":j,"surface":ptxt[i:j]})
            for pos in range(i,j): taken.add(pos)
    paragraphs.append({"para_id":pid,"text":ptxt,"mentions":ms})

annotation = {
    "book_id":"shiji",
    "chapter_id":"酷吏列传第六十二",
    "chapter_title":"酷吏列传第六十二",
    "version":"final",
    "generated_at": datetime.now().isoformat(),
    "paragraphs": paragraphs
}

with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/ontology/实体标注-酷吏列传第六十二.json','w',encoding='utf-8') as f:
    json.dump(annotation, f, ensure_ascii=False, indent=2)
print("annotation done, paragraphs:", len(paragraphs))
# 统计mentions
total = sum(len(p['mentions']) for p in paragraphs)
print("total mentions:", total)
import json as _j
_j.load(open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/ontology/实体标注-酷吏列传第六十二.json','r',encoding='utf-8'))
print("json valid")
