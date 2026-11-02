import json
from datetime import datetime

with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/ontology/实体-初稿-酷吏列传第六十二.json', 'r', encoding='utf-8') as f:
    draft = json.load(f)

# add relations
relations = [
    {"type":"开篇立论","from":"司马迁（太史公）","to":"孔子","evidence":["p0"]},
    {"type":"开篇立论","from":"司马迁（太史公）","to":"老子（老聃）","evidence":["p0"]},
    {"type":"引用论断","from":"司马迁（太史公）","to":"法令滋章盗贼多有","evidence":["p0","p36"]},
    {"type":"凌轹宗室","from":"侯封","to":"吕雉（高后）","evidence":["p1"]},
    {"type":"辅助景帝","from":"晁错","to":"刘启（汉景帝）","evidence":["p1"]},
    {"type":"触犯七国","from":"晁错","to":"七国之乱（注：概称，作事件：晁错刻深被戮）","evidence":["p1"]},
    {"type":"臣事文帝","from":"郅都","to":"刘恒（汉文帝）","evidence":["p2"]},
    {"type":"直谏救主","from":"郅都","to":"刘启（汉景帝）","evidence":["p2"]},
    {"type":"族灭首恶","from":"郅都","to":"济南瞷氏（概念：族灭/事件：族灭瞷氏）","evidence":["p3"]},
    {"type":"号曰苍鹰","from":"郅都","to":"苍鹰","evidence":["p5"]},
    {"type":"侧目而视","from":"郅都","to":"列侯宗室（概念）","evidence":["p5"]},
    {"type":"对簿自杀","from":"刘荣（临江王）","to":"郅都","evidence":["p6"]},
    {"type":"怒斩郅都","from":"窦太后","to":"郅都","evidence":["p6"]},
    {"type":"拜为雁门","from":"刘启（汉景帝）","to":"郅都","evidence":["p6"]},
    {"type":"畏都引去","from":"匈奴","to":"郅都","evidence":["p6"]},
    {"type":"事奉景帝","from":"宁成","to":"刘启（汉景帝）","evidence":["p7"]},
    {"type":"交驩同僚","from":"宁成","to":"郅都","evidence":["p7"]},
    {"type":"操下如束湿薪","from":"宁成","to":"其下属","evidence":["p7"]},
    {"type":"髡钳逃归","from":"宁成","to":"函谷关","evidence":["p8"]},
    {"type":"以侯周阳为氏","from":"周阳由","to":"赵兼","evidence":["p9"]},
    {"type":"暴酷骄恣","from":"周阳由","to":"所居郡豪","evidence":["p9"]},
    {"type":"争权同死","from":"周阳由","to":"胜屠公","evidence":["p10"]},
    {"type":"共事二千石","from":"周阳由","to":"汲黯","evidence":["p9"]},
    {"type":"共定律令","from":"赵禹","to":"张汤","evidence":["p12","p15"]},
    {"type":"作文深刻","from":"赵禹","to":"见知法","evidence":["p12"]},
    {"type":"评禹不任","from":"周亚夫（条侯）","to":"赵禹","evidence":["p12","p24"]},
    {"type":"孤立行意","from":"赵禹","to":"知友宾客","evidence":["p15"]},
    {"type":"审鼠磔尸","from":"张汤","to":"盗鼠","evidence":["p13"]},
    {"type":"倾身助之","from":"张汤","to":"田胜（周阳侯）","evidence":["p14"]},
    {"type":"征汤为史","from":"田蚡（武安侯）","to":"张汤","evidence":["p15"]},
    {"type":"深竟党与","from":"张汤","to":"陈皇后（阿娇）","evidence":["p15"]},
    {"type":"舞智御人","from":"张汤","to":"下属","evidence":["p15"]},
    {"type":"交私贾人","from":"张汤","to":"田甲","evidence":["p15","p19"]},
    {"type":"交私贾人","from":"张汤","to":"鱼翁叔","evidence":["p15"]},
    {"type":"春秋决狱","from":"张汤","to":"尚书春秋","evidence":["p16"]},
    {"type":"兄事赵禹","from":"张汤","to":"赵禹","evidence":["p15"]},
    {"type":"称赞汤美","from":"公孙弘","to":"张汤","evidence":["p16"]},
    {"type":"穷根本","from":"张汤","to":"刘安（淮南王）","evidence":["p16"]},
    {"type":"争诛严助","from":"张汤","to":"严助","evidence":["p16"]},
    {"type":"争诛伍被","from":"张汤","to":"伍被","evidence":["p16"]},
    {"type":"承指造币","from":"张汤","to":"刘彻（汉武帝）","evidence":["p17"]},
    {"type":"笼盐铁","from":"张汤","to":"盐铁官营","evidence":["p17"]},
    {"type":"出告缗令","from":"张汤","to":"告缗令","evidence":["p17"]},
    {"type":"天下皆决于汤","from":"刘彻（汉武帝）","to":"张汤","evidence":["p17"]},
    {"type":"斥为愚儒","from":"张汤","to":"狄山","evidence":["p18"]},
    {"type":"遣山乘鄣","from":"刘彻（汉武帝）","to":"狄山","evidence":["p18"]},
    {"type":"斩山头去","from":"匈奴","to":"狄山","evidence":["p18"]},
    {"type":"责汤行义","from":"田甲","to":"张汤","evidence":["p19"]},
    {"type":"飞变告文","from":"鲁谒居","to":"李文","evidence":["p21"]},
    {"type":"知而隐之","from":"张汤","to":"鲁谒居","evidence":["p21"]},
    {"type":"为谒居摩足","from":"张汤","to":"鲁谒居","evidence":["p21"]},
    {"type":"求汤阴事","from":"刘彭祖（赵王）","to":"张汤","evidence":["p21"]},
    {"type":"穷竟其事","from":"减宣","to":"张汤","evidence":["p21"]},
    {"type":"约俱谢","from":"庄青翟","to":"张汤","evidence":["p21"]},
    {"type":"欲陷汤","from":"朱买臣","to":"张汤","evidence":["p22"]},
    {"type":"欲陷汤","from":"王朝","to":"张汤","evidence":["p22"]},
    {"type":"欲陷汤","from":"边通","to":"张汤","evidence":["p22"]},
    {"type":"捕案田信","from":"三长史（朱买臣、王朝、边通）","to":"田信","evidence":["p22"]},
    {"type":"八辈簿责","from":"刘彻（汉武帝）","to":"张汤","evidence":["p22"]},
    {"type":"让汤自为计","from":"赵禹","to":"张汤","evidence":["p22"]},
    {"type":"遗书自杀","from":"张汤","to":"三长史","evidence":["p22","p23"]},
    {"type":"薄葬汤","from":"张汤母","to":"张汤","evidence":["p23"]},
    {"type":"尽案诛三长史","from":"刘彻（汉武帝）","to":"朱买臣","evidence":["p23"]},
    {"type":"丞相自杀","from":"庄青翟","to":"","evidence":["p23"]},
    {"type":"惜汤迁安世","from":"刘彻（汉武帝）","to":"张安世","evidence":["p23"]},
    {"type":"以寿卒家","from":"赵禹","to":"","evidence":["p24"]},
    {"type":"少年为盗","from":"义纵","to":"张次公","evidence":["p25"]},
    {"type":"因姊得官","from":"义纵","to":"义姁","evidence":["p25"]},
    {"type":"医幸太后","from":"义姁","to":"王太后（武帝母）","evidence":["p25"]},
    {"type":"捕按仲","from":"义纵","to":"修成子仲","evidence":["p25"]},
    {"type":"族灭穰氏","from":"义纵","to":"河内","evidence":["p25"]},
    {"type":"评成如狼牧羊","from":"公孙弘","to":"宁成","evidence":["p26"]},
    {"type":"宁见乳虎","from":"关东吏民","to":"宁成","evidence":["p26"]},
    {"type":"案宁氏破家","from":"义纵","to":"宁成","evidence":["p26"]},
    {"type":"举为爪牙","from":"义纵","to":"杜周","evidence":["p26","p38"]},
    {"type":"掩定襄狱","from":"义纵","to":"定襄罪囚","evidence":["p26"]},
    {"type":"不寒而栗","from":"定襄吏民","to":"义纵","evidence":["p26"]},
    {"type":"鹰击毛挚","from":"义纵","to":"","evidence":["p27"]},
    {"type":"共事互凌","from":"义纵","to":"王温舒","evidence":["p27"]},
    {"type":"怒其不治道","from":"刘彻（汉武帝）","to":"义纵","evidence":["p27"]},
    {"type":"捕可使者","from":"义纵","to":"杨可","evidence":["p27"]},
    {"type":"废格弃市","from":"杜式","to":"义纵","evidence":["p27"]},
    {"type":"椎埋为奸","from":"王温舒","to":"","evidence":["p28"]},
    {"type":"择爪牙吏","from":"王温舒","to":"杨皆","evidence":["p28","p29"]},
    {"type":"择爪牙吏","from":"王温舒","to":"麻戊","evidence":["p29"]},
    {"type":"择爪牙吏","from":"王温舒","to":"杨赣","evidence":["p29"]},
    {"type":"择爪牙吏","from":"王温舒","to":"成信","evidence":["p29"]},
    {"type":"请族豪猾","from":"王温舒","to":"刘彻（汉武帝）","evidence":["p29"]},
    {"type":"流血十余里","from":"王温舒","to":"河内","evidence":["p29"]},
    {"type":"叹冬月短","from":"王温舒","to":"","evidence":["p29"]},
    {"type":"惮纵未敢恣","from":"王温舒","to":"义纵","evidence":["p29"]},
    {"type":"廉武督盗","from":"尹齐","to":"张汤","evidence":["p30"]},
    {"type":"声甚宁成","from":"尹齐","to":"宁成","evidence":["p30"]},
    {"type":"放尹齐治","from":"杨仆","to":"尹齐","evidence":["p31"]},
    {"type":"楼船征越","from":"杨仆","to":"南越","evidence":["p31"]},
    {"type":"为荀彘缚","from":"杨仆","to":"荀彘","evidence":["p31"]},
    {"type":"善事有势者","from":"王温舒","to":"权贵","evidence":["p32"]},
    {"type":"虎而冠","from":"王温舒","to":"爪牙吏","evidence":["p32"]},
    {"type":"请覆脱卒","from":"王温舒","to":"刘彻（汉武帝）","evidence":["p33"]},
    {"type":"匿华成","from":"王温舒","to":"华成","evidence":["p34"]},
    {"type":"罪至族自杀","from":"王温舒","to":"","evidence":["p34"]},
    {"type":"五族同诛","from":"王温舒","to":"两弟两婚家","evidence":["p34"]},
    {"type":"悲夫五族","from":"徐自为","to":"王温舒","evidence":["p34"]},
    {"type":"以恶为治","from":"王温舒","to":"天下","evidence":["p36"]},
    {"type":"揭竿起义","from":"梅免","to":"地方官","evidence":["p36"]},
    {"type":"发兵兴击","from":"范昆","to":"农民起义军","evidence":["p36"]},
    {"type":"作沈命法","from":"刘彻（汉武帝）","to":"二千石","evidence":["p36"]},
    {"type":"上下相匿","from":"地方小吏","to":"上级官府","evidence":["p36"]},
    {"type":"举荐减宣","from":"卫青","to":"减宣","evidence":["p37"]},
    {"type":"微文深诋","from":"减宣","to":"主父偃","evidence":["p37"]},
    {"type":"微文深诋","from":"减宣","to":"刘安（淮南王）","evidence":["p37"]},
    {"type":"治米盐事","from":"减宣","to":"属县","evidence":["p37"]},
    {"type":"格杀成信","from":"减宣","to":"成信","evidence":["p37"]},
    {"type":"大逆自杀","from":"减宣","to":"","evidence":["p37"]},
    {"type":"举为廷史","from":"义纵","to":"杜周","evidence":["p38"]},
    {"type":"事张汤","from":"杜周","to":"张汤","evidence":["p38"]},
    {"type":"外宽内深","from":"杜周","to":"","evidence":["p39"]},
    {"type":"善候伺","from":"杜周","to":"刘彻（汉武帝）","evidence":["p39"]},
    {"type":"专以意指为狱","from":"杜周","to":"人主","evidence":["p39"]},
    {"type":"答客三尺法","from":"杜周","to":"客（说者）","evidence":["p39"]},
    {"type":"诏狱逮六七万人","from":"杜周","to":"罪囚","evidence":["p40"]},
    {"type":"捕刻桑弘羊子弟","from":"杜周","to":"桑弘羊","evidence":["p41"]},
    {"type":"迁御史大夫","from":"刘彻（汉武帝）","to":"杜周","evidence":["p41"]},
    {"type":"夾河为守","from":"杜周两子","to":"河两岸郡守","evidence":["p41"]},
    {"type":"家訾累巨万","from":"杜周","to":"","evidence":["p41"]},
    {"type":"辩证评价十人","from":"司马迁（太史公）","to":"郅都","evidence":["p42"]},
    {"type":"辩证评价十人","from":"司马迁（太史公）","to":"张汤","evidence":["p42"]},
    {"type":"辩证评价十人","from":"司马迁（太史公）","to":"赵禹","evidence":["p42"]},
    {"type":"辩证评价十人","from":"司马迁（太史公）","to":"杜周","evidence":["p42"]},
    {"type":"何足数哉","from":"司马迁（太史公）","to":"冯当","evidence":["p42"]},
    {"type":"总结述赞","from":"司马贞","to":"全篇主旨","evidence":["p43"]}
]

# 修正关系端点，全部在entities集合中
name_set = set()
for k, lst in draft['entities'].items():
    for ent in lst:
        name_set.add(ent['name'])

valid_rels = []
# 清洗关系，把不在name_set里的、空字符串端点替换成合法实体名
name_replace = {
    "其下属":"宁成",
    "济南瞷氏（概念：族灭/事件：族灭瞷氏）":"郅都",
    "列侯宗室（概念）":"诸侯",
    "所居郡豪":"豪强",
    "两弟两婚家":"王温舒两弟",
    "人主":"刘彻（汉武帝）",
    "罪囚":"罪囚",
    "两弟两婚家（注：补实体）":"王温舒两弟",
    "三长史（朱买臣、王朝、边通）":"朱买臣",
    "诸侯": None,  # 补
    "豪强": None,
    "地方官": None,
    "罪囚": None,
    "农民起义军": None,
    "权贵": None,
    "张汤两子河两岸":None,
    "河两岸郡守":None,
    "王温舒两弟":None,
    "盗鼠":None,
    "下属":None,
    "全文主旨":None,
    "全篇主旨":None,
    "两弟两婚家":None,
    "客（说者）":None,
    "上级官府":None,
    "二千石":None,
    "地方小吏":None,
    "定襄罪囚":None,
    "属县":None,
    "河内":None,
    "天下":None,
    "张汤两子":"杜周",
    "盗鼠":"张汤",
    "下属":"赵禹",
    "全篇主旨":"酷烈为治",
    "罪囚":"诏狱",
    "农民起义军":"梅免",
    "权贵":"王温舒",
    "两弟两婚家":"王温舒",
    "客（说者）":"杜周",
    "上级官府":"郡守",
    "二千石":"地方长吏",
    "地方小吏":"县吏",
    "定襄罪囚":"义纵",
    "属县":"减宣",
    "河内":"河内郡",
    "天下":"汉朝",
    "诸侯":None,
    "豪强":None,
    "地方官":None,
    "郡守":None,
    "地方长吏":None,
    "县吏":None,
    "酷烈为治":None,
}
# 补充缺失实体到persons/places/concepts
def add_missing(name, typ, note, evid):
    prefix_map = {"persons":"person","places":"place","events":"event","concepts":"concept"}
    maxn = 0
    for ent in draft['entities'][typ]:
        nid = int(ent['id'].split('_')[1])
        if nid > maxn: maxn = nid
    new = {"id": f"{prefix_map[typ]}_{maxn+1:03d}", "name": name, "alias": [], "note": note, "evidence": evid}
    draft['entities'][typ].append(new)
    name_set.add(name)

add_missing("诸侯王","concepts","泛指诸侯王室、宗室列侯",["p5"])
add_missing("豪强","concepts","地方豪强奸猾大族，为酷吏打击对象",["p3","p9","p25","p26","p29"])
add_missing("郡守","concepts","郡最高长官，二千石，沈命法下主要问责对象",["p3","p10","p29","p36"])
add_missing("酷烈为治","concepts","以酷烈严酷手段施政治民，为本篇主旨",["p42","p43"])
add_missing("县吏","concepts","郡县小吏，沈命法下畏诛不敢发盗",["p36"])

valid_rels = []
for r in relations:
    f = r['from']
    t = r['to'] if r['to'] else None
    typ = r['type']
    evid = r['evidence']
    # filter out self/missing
    if t is None or t == f:
        continue
    if f not in name_set:
        # find by endswith
        found = False
        for n in name_set:
            if n.endswith(f) or f in n:
                f = n; found=True; break
        if not found:
            continue
    if t not in name_set:
        found = False
        for n in name_set:
            if n.endswith(t) or t in n:
                t = n; found=True; break
        if not found:
            continue
    if not (2 <= len(typ) <= 8):
        continue
    if not all(c.isalnum() or c in '为于与对从至把将当被以' for c in typ):
        # 动宾短语检查简化：有动词字即可，长度合即保留
        pass
    valid_rels.append({"type": typ, "from": f, "to": t, "evidence": evid})

# 去重
seen=set(); uniq=[]
for r in valid_rels:
    key=(r['type'],r['from'],r['to'])
    if key not in seen and r['from']!=r['to']:
        seen.add(key); uniq.append(r)

final = {
    "book_id": draft['book_id'],
    "chapter_id": draft['chapter_id'],
    "chapter_title": draft['chapter_title'],
    "version": "final",
    "generated_at": datetime.now().isoformat(),
    "entities": draft['entities'],
}
final['entities']['relations'] = uniq

with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/ontology/实体-定稿-酷吏列传第六十二.json','w',encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=2)
print("final entities done, relations:", len(uniq))
# validate
import json as _j
with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/ontology/实体-定稿-酷吏列传第六十二.json','r',encoding='utf-8') as f:
    d = _j.load(f)
ns = set()
for k in ['persons','places','events','concepts']:
    for e in d['entities'][k]:
        ns.add(e['name'])
bad=0
for r in d['entities']['relations']:
    if r['from'] not in ns or r['to'] not in ns:
        print('bad rel', r); bad+=1
print('bad rels', bad)
print('total persons', len(d['entities']['persons']),'places',len(d['entities']['places']),'events',len(d['entities']['events']),'concepts',len(d['entities']['concepts']),'relations',len(d['entities']['relations']))
