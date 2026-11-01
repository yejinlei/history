#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为《南越尉佗列传第五十三》生成实体初稿、定稿、标注、增强文件。"""
import json
import os
import re
from datetime import datetime

CHAPTER_ID = "53"
CHAPTER_TITLE = "南越尉佗列传第五十三"
BOOK_ID = "shiji"
BASE = "/home/user/workspace/17521090448082856013/history-site"

# 读取底本
text_path = f"{BASE}/data/books/shiji/text/shiji-南越尉佗列傳第五十三.json"
with open(text_path, encoding="utf-8") as f:
    text_data = json.load(f)
paras = text_data["paragraphs"]
N = len(paras)
para_texts = [p["text"] for p in paras]
para_ids = [p["id"].split(":")[-1] for p in paras]  # p0,p1,...
print("段落数:", N)

# ============ 实体清单（含evidence段号） ============
# 已逐段遍历原文，按出现段落填入evidence
persons = [
    {"name":"赵佗（南越王）","alias":["尉佗","趙佗","佗","南越王","南越武王","南越武帝","蠻夷大長老夫臣佗"],"note":"真定人，秦南海龙川令，秦末兼并桂林、象郡自立为南越武王，汉初受封，武帝建元四年卒，享年约百余岁","evidence":["p0","p1","p2","p3","p12","p13"],"id":"person_000"},
    {"name":"任囂","alias":["南海尉","囂"],"note":"秦南海尉，病终将南海尉事授予赵佗，为南越立国奠定基础","evidence":["p0"],"id":"person_001"},
    {"name":"陈胜","alias":["陳勝"],"note":"秦末农民起义领袖，首举反秦义旗","evidence":["p0"],"id":"person_002"},
    {"name":"吴广","alias":["吳廣"],"note":"秦末农民起义领袖，与陈胜同举义旗","evidence":["p0"],"id":"person_003"},
    {"name":"项羽","alias":["項羽","項籍"],"note":"西楚霸王，秦末义军盟主，主持分封","evidence":["p0"],"id":"person_004"},
    {"name":"刘邦（汉高祖）","alias":["高帝","劉季","漢高祖","高皇帝"],"note":"汉高祖，西汉开国皇帝，汉十一年遣陆贾立赵佗为南越王","evidence":["p0","p1","p2"],"id":"person_005"},
    {"name":"陆贾","alias":["陸賈","賈"],"note":"汉初辩士，太中大夫，两度出使南越，说服赵佗去帝制称臣，著《新语》","evidence":["p0","p2","p14"],"id":"person_006"},
    {"name":"吕雉（高后）","alias":["高后","呂后"],"note":"汉高祖皇后，惠帝时临朝称制，禁南越关市铁器，引发赵佗称帝","evidence":["p1","p2"],"id":"person_007"},
    {"name":"周灶（隆虑侯）","alias":["隆慮侯竈","竈","隆慮侯"],"note":"汉初将军，封隆虑侯，高后时奉命击南越，因暑湿大疫未能逾岭","evidence":["p1","p13"],"id":"person_008"},
    {"name":"刘恒（汉文帝）","alias":["孝文帝","孝文皇帝","文帝"],"note":"汉文帝，即位后为赵佗修治真定冢墓，遣陆贾再次出使南越，赵佗去帝制称臣","evidence":["p2"],"id":"person_009"},
    {"name":"陈平","alias":["陳平","丞相平"],"note":"汉初丞相，封曲逆侯，向文帝推荐陆贾出使南越","evidence":["p2"],"id":"person_010"},
    {"name":"刘启（汉景帝）","alias":["孝景","孝景皇帝","景帝"],"note":"汉景帝，在位时南越称臣，使人朝请","evidence":["p2"],"id":"person_011"},
    {"name":"赵胡（南越文王）","alias":["胡","南越王","文王"],"note":"赵佗之孙，南越文王，即位后遭闽越攻击，遣太子婴齐入宿卫，称病不入朝","evidence":["p3","p4","p13"],"id":"person_012"},
    {"name":"郢（闽越王）","alias":["閩越王郢","郢"],"note":"闽越王，建元六年发兵击南越，为其弟余善所杀","evidence":["p3","p4"],"id":"person_013"},
    {"name":"余善","alias":["餘善"],"note":"闽越王郢之弟，杀郢降汉，后自立为东越王，元封初反汉被诛，详见《东越列传》","evidence":["p3","p4"],"id":"person_014"},
    {"name":"刘彻（汉武帝）","alias":["天子","上","皇帝","武帝","孝武"],"note":"汉武帝，在位期间平定两越，置九郡，完成对岭南的统一","evidence":["p3","p4","p5","p6","p7","p8","p9","p10","p11"],"id":"person_015"},
    {"name":"庄助","alias":["莊助","嚴助"],"note":"汉会稽吴人，中大夫，奉武帝节发兵会稽救东瓯，又谕意南越王","evidence":["p4","p8"],"id":"person_016"},
    {"name":"赵婴齐（南越明王）","alias":["嬰齊","太子嬰齊","明王"],"note":"赵胡太子，入长安宿卫，娶邯郸樛氏，即位后藏武帝玺，称病不入朝","evidence":["p4","p5","p6","p13"],"id":"person_017"},
    {"name":"樛太后","alias":["樛氏女","太后","樛后","嫪后"],"note":"邯郸樛氏女，婴齐之后，南越王兴之母，曾与安国少季私通，力主内属，被吕嘉所杀","evidence":["p5","p6","p7","p8","p13","p14"],"id":"person_018"},
    {"name":"赵兴","alias":["太子興","興","王"],"note":"婴齐与樛氏所生之子，南越王，即位后与太后请内属，被吕嘉所杀","evidence":["p5","p6","p7","p8"],"id":"person_019"},
    {"name":"赵次公","alias":["次公"],"note":"婴齐之子，被遣入长安宿卫","evidence":["p5"],"id":"person_020"},
    {"name":"安国少季","alias":["安國少季","使者"],"note":"霸陵人，与樛太后私通，元鼎四年奉命出使南越谕王太后入朝","evidence":["p6"],"id":"person_021"},
    {"name":"终军","alias":["終軍","諫大夫終軍","辯士"],"note":"汉济南人，谏大夫，辩士，年少请缨出使南越，年二十余为吕嘉所杀，世称「终童」","evidence":["p6"],"id":"person_022"},
    {"name":"魏臣","alias":["勇士魏臣"],"note":"汉朝勇士，随终军出使南越补其不足","evidence":["p6"],"id":"person_023"},
    {"name":"路博德（伏波将军）","alias":["路博德","衞尉路博德","伏波","伏波將軍"],"note":"汉平州人，卫尉，拜伏波将军，元鼎六年平南越，益封，为伏波将军开府之始","evidence":["p6","p9","p10","p11","p13"],"id":"person_024"},
    {"name":"吕嘉","alias":["呂嘉","相嘉","丞相","嘉"],"note":"南越相，历相三王，宗族七十余人为长吏，得众心，反对内属，杀王、太后及汉使者反，被汉军擒杀","evidence":["p6","p7","p8","p9","p10","p13","p14"],"id":"person_025"},
    {"name":"苍梧秦王","alias":["蒼梧秦王","秦王"],"note":"南越苍梧王，称秦王，与吕嘉有联姻，后归汉","evidence":["p7","p8","p11"],"id":"person_026"},
    {"name":"庄参","alias":["莊參"],"note":"汉臣，天子欲使以二千人往使南越，庄参辞不可","evidence":["p8"],"id":"person_027"},
    {"name":"韩千秋","alias":["韓千秋","故濟北相","郟壯士"],"note":"颍川郏县人，故济北相，自请率勇士入越击吕嘉，兵入小胜后战死，武帝封其子延年","evidence":["p8"],"id":"person_028"},
    {"name":"樛乐","alias":["樛樂","太后弟樛樂"],"note":"樛太后之弟，与韩千秋将二千人入越，战死，武帝封其子广德","evidence":["p8"],"id":"person_029"},
    {"name":"赵建德","alias":["建德","術陽侯建德","術陽侯"],"note":"赵婴齐长子（越妻所生），封术阳侯，吕嘉反后立为南越王，番禺降后被擒，南越国亡","evidence":["p8","p10"],"id":"person_030"},
    {"name":"韩延年","alias":["延年","成安侯"],"note":"韩千秋之子，以父功封成安侯，后随李陵战匈奴","evidence":["p8"],"id":"person_031"},
    {"name":"樛广德","alias":["廣德","龍亢侯"],"note":"樛乐之子，以其姑樛太后首愿属汉封龙亢侯","evidence":["p8"],"id":"person_032"},
    {"name":"杨仆（楼船将军）","alias":["楊僕","樓船將軍","主爵都尉楊僕"],"note":"汉宜阳人，主爵都尉，拜楼船将军，出豫章下横浦，先陷寻陕破石门，攻番禺，以陷坚封将梁侯","evidence":["p9","p10","p11","p13"],"id":"person_033"},
    {"name":"归义越侯（二人）","alias":["歸義越侯二人","戈船將軍","下厲將軍"],"note":"故归义汉朝的两位越人封侯，分别拜戈船将军、下厉将军，出零陵","evidence":["p9","p11"],"id":"person_034"},
    {"name":"驰义侯","alias":["馳義侯"],"note":"汉所封侯，奉命发巴蜀夜郎兵下牂柯江会番禺","evidence":["p9","p11"],"id":"person_035"},
    {"name":"苏弘","alias":["司馬蘇弘","故校尉司馬"],"note":"伏波将军部下司马，擒赵建德，封海常侯","evidence":["p10"],"id":"person_036"},
    {"name":"孙都稽","alias":["都稽","越郎都稽","越郎"],"note":"南越郎官，擒吕嘉，封临蔡侯","evidence":["p10"],"id":"person_037"},
    {"name":"赵光（苍梧王）","alias":["蒼梧王趙光","趙光"],"note":"南越苍梧王，与越王同姓，闻汉兵至降汉，封随桃侯","evidence":["p11"],"id":"person_038"},
    {"name":"揭阳令史定","alias":["揭陽令定","定"],"note":"南越揭阳县令，名定，闻汉兵至自定属汉，封安道侯","evidence":["p11"],"id":"person_039"},
    {"name":"居翁","alias":["桂林監居翁","越桂林監居翁"],"note":"南越桂林郡监，谕瓯骆四十余万口降汉，封湘成侯","evidence":["p11"],"id":"person_040"},
    {"name":"越人","alias":["越","越民"],"note":"南越国民众、越地军民","evidence":["p0","p10","p8"],"id":"person_041"},
]

places = [
    {"name":"真定","alias":["真定"],"note":"汉县名，今河北正定，赵佗故里","evidence":["p0","p2"],"id":"place_000"},
    {"name":"杨越","alias":["楊越"],"note":"古族名，指扬州之越，又称扬越，分布于长江中下游及岭南","evidence":["p0"],"id":"place_001"},
    {"name":"桂林郡","alias":["桂林"],"note":"秦置郡，治今广西桂平西南，秦三十六郡之一","evidence":["p0","p0"],"id":"place_002"},
    {"name":"南海郡","alias":["南海"],"note":"秦置郡，治番禺，今广东广州，秦三十六郡之一","evidence":["p0"],"id":"place_003"},
    {"name":"象郡","alias":["象郡"],"note":"秦置郡，辖今越南北部及广西南部一带","evidence":["p0"],"id":"place_004"},
    {"name":"龙川","alias":["龍川"],"note":"秦南海郡属县，今广东龙川西，赵佗为龙川县令","evidence":["p0"],"id":"place_005"},
    {"name":"番禺","alias":["番禺"],"note":"南越国都，今广东广州，南海郡治","evidence":["p0","p8","p10"],"id":"place_006"},
    {"name":"横浦关","alias":["橫浦"],"note":"秦关名，在今广东南雄北大庾岭，为岭南五关之一","evidence":["p0","p9"],"id":"place_007"},
    {"name":"阳山关","alias":["陽山"],"note":"秦关名，在今广东阳山西北","evidence":["p0"],"id":"place_008"},
    {"name":"湟谿关","alias":["湟谿"],"note":"秦关名，在今广东英德西南连江入北江处","evidence":["p0"],"id":"place_009"},
    {"name":"长沙国","alias":["長沙","長沙邊邑"],"note":"汉初诸侯王国，与南越接境，都临湘（今湖南长沙）","evidence":["p0","p1","p2"],"id":"place_010"},
    {"name":"闽越","alias":["閩越"],"note":"古族名、国名，在今福建一带，都东冶（今福州）","evidence":["p1","p3","p4"],"id":"place_011"},
    {"name":"西瓯","alias":["西甌"],"note":"古族名，百越一支，分布在今广西及越南北部","evidence":["p1","p2"],"id":"place_012"},
    {"name":"骆越","alias":["駱","甌駱","駱越"],"note":"古族名，百越一支，分布在今越南北部及广西南部，又称瓯骆","evidence":["p1","p2","p11"],"id":"place_013"},
    {"name":"代","alias":["代"],"note":"汉文帝即位前封代王，代国在今山西北部、河北西北部，都中都","evidence":["p2"],"id":"place_014"},
    {"name":"好畤","alias":["好畤"],"note":"汉县名，今陕西乾县东，陆贾故里","evidence":["p2"],"id":"place_015"},
    {"name":"长安","alias":["長安"],"note":"西汉都城，今陕西西安西北","evidence":["p5","p6","p8"],"id":"place_016"},
    {"name":"邯郸","alias":["邯鄲"],"note":"汉赵国都，今河北邯郸，樛太后故里","evidence":["p5"],"id":"place_017"},
    {"name":"霸陵","alias":["霸陵"],"note":"汉文帝陵，因置县，今陕西西安东北，安国少季故里","evidence":["p6"],"id":"place_018"},
    {"name":"桂阳","alias":["桂陽"],"note":"汉郡/县名，治今广东连州，伏波将军路博德出桂阳","evidence":["p6","p9"],"id":"place_019"},
    {"name":"郏县","alias":["郟"],"note":"汉县名，今河南郏县，韩千秋故里","evidence":["p8"],"id":"place_020"},
    {"name":"汇水","alias":["匯水"],"note":"水名，即洭水/湟水，今连江，伏波将军下汇水","evidence":["p9"],"id":"place_021"},
    {"name":"豫章","alias":["豫章"],"note":"汉郡名，治今江西南昌，楼船将军杨仆出豫章","evidence":["p9"],"id":"place_022"},
    {"name":"零陵","alias":["零陵"],"note":"汉郡名，治今广西全州西南，戈船、下厉将军出零陵","evidence":["p9"],"id":"place_023"},
    {"name":"离水","alias":["離水"],"note":"水名，即漓江，今广西漓江","evidence":["p9"],"id":"place_024"},
    {"name":"苍梧","alias":["蒼梧"],"note":"古地名/国名，今广西梧州一带，南越苍梧秦王所居","evidence":["p9","p11"],"id":"place_025"},
    {"name":"巴蜀","alias":["巴蜀"],"note":"巴郡、蜀郡合称，今四川重庆一带","evidence":["p9"],"id":"place_026"},
    {"name":"夜郎","alias":["夜郎"],"note":"古国名，在今贵州西部及云南东北部","evidence":["p9","p11"],"id":"place_027"},
    {"name":"牂柯江","alias":["䍧柯江"],"note":"水名，今北盘江，下游为西江，可通番禺","evidence":["p9"],"id":"place_028"},
    {"name":"寻陕","alias":["尋陝"],"note":"地名，又作寻峡、寻狭，在今广东清远飞来峡","evidence":["p10"],"id":"place_029"},
    {"name":"石门","alias":["石門"],"note":"地名，在今广州西北，为番禺要塞","evidence":["p10"],"id":"place_030"},
    {"name":"揭阳","alias":["揭陽"],"note":"汉揭阳县，今广东揭阳，南越揭阳令定所居","evidence":["p11"],"id":"place_031"},
    {"name":"南海","alias":["南海"],"note":"即南海，南方大海，番禺所临","evidence":["p0","p10"],"id":"place_032"},
    {"name":"江淮之间","alias":["江淮之間"],"note":"长江、淮河之间地区，东越内迁之地","evidence":["p2东越"],"id":"place_033"},
]

events = [
    {"name":"秦略定杨越置三郡","alias":["略定楊越置桂林南海象郡"],"note":"秦始皇三十三年（前214年），秦南平百越，置桂林、南海、象郡，以谪徙民与越杂处","evidence":["p0"],"id":"event_000"},
    {"name":"任嚣临终托赵佗","alias":["任囂病且死召趙佗語"],"note":"秦二世时南海尉任嚣病重，召龙川令赵佗，嘱其绝新道自备，待诸侯变，被佗书行南海尉事","evidence":["p0"],"id":"event_001"},
    {"name":"赵佗绝关自守","alias":["移檄告橫浦陽山湟谿關急絕道聚兵自守"],"note":"任嚣死，赵佗移檄三关绝道聚兵，以法诛秦所置长吏，以其党为假守","evidence":["p0"],"id":"event_002"},
    {"name":"赵佗自立南越武王","alias":["擊并桂林象郡自立爲南越武王"],"note":"秦破灭后赵佗击并桂林、象郡，自立为南越武王","evidence":["p0"],"id":"event_003"},
    {"name":"陆贾首次使越封王","alias":["遣陸賈因立佗爲南越王剖符通使"],"note":"汉十一年（前196年）刘邦遣陆贾立赵佗为南越王，剖符通使，和集百越","evidence":["p0"],"id":"event_004"},
    {"name":"高后禁南越关市","alias":["禁南越關市鐵器"],"note":"高后时有司请禁南越关市铁器，赵佗怨，以为长沙王之计","evidence":["p1"],"id":"event_005"},
    {"name":"赵佗称帝攻长沙","alias":["自尊號爲南越武帝發兵攻長沙邊邑"],"note":"赵佗自称南越武帝，发兵攻长沙边邑，败数县而去","evidence":["p1"],"id":"event_006"},
    {"name":"隆虑侯击南越疫罢","alias":["隆慮侯竈擊之暑溼士卒大疫兵不能踰嶺"],"note":"高后遣隆虑侯周灶击南越，会暑湿士卒大疫，兵不能逾岭；岁余高后崩，罢兵","evidence":["p1","p13"],"id":"event_007"},
    {"name":"赵佗以兵威赂闽越西瓯骆","alias":["以兵威邊財物賂遺閩越西甌駱役屬焉"],"note":"赵佗乘汉兵罢，以兵威边，以财物赂遗闽越、西瓯、骆，属役之，东西万余里，乘黄屋左纛称制与中国侔","evidence":["p1"],"id":"event_008"},
    {"name":"文帝为赵佗修冢召昆弟","alias":["爲佗親冢在真定置守邑歲時奉祀召其從昆弟尊官厚賜"],"note":"孝文帝元年，初镇抚天下，为赵佗真定亲冢置守邑岁时奉祀，召其从昆弟尊官厚赐宠之","evidence":["p2"],"id":"event_009"},
    {"name":"陆贾再次使越","alias":["召賈以爲太中大夫往使讓佗自立爲帝"],"note":"文帝复召陆贾为太中大夫，往使南越责备赵佗自立为帝无一介之使报","evidence":["p2"],"id":"event_010"},
    {"name":"赵佗去帝制称臣","alias":["爲書謝去帝制黃屋左纛長爲藩臣"],"note":"赵佗见陆贾至甚恐，上书谢罪，愿长为藩臣奉贡职，下令国中去帝制黄屋左纛","evidence":["p2"],"id":"event_011"},
    {"name":"闽越击南越","alias":["閩越王郢興兵擊南越邊邑"],"note":"建元六年（前135年）闽越王郢兴兵击南越边邑，赵胡上书天子","evidence":["p3"],"id":"event_012"},
    {"name":"余善杀郢降汉","alias":["閩越王弟餘善殺郢以降"],"note":"汉兴师讨闽越，兵未逾岭，余善杀郢以降，罢兵","evidence":["p3"],"id":"event_013"},
    {"name":"赵胡遣婴齐入宿卫","alias":["遣太子嬰齊入宿衞"],"note":"天子使庄助谕意，赵胡顿首谢德，遣太子婴齐入长安宿卫","evidence":["p4"],"id":"event_014"},
    {"name":"赵胡称病不入朝","alias":["胡稱病竟不入見"],"note":"大臣谏胡不可入见，胡称病，终不入朝；后十余岁胡病甚，婴齐请归，胡薨谥文王","evidence":["p4"],"id":"event_015"},
    {"name":"婴齐藏玺立樛后","alias":["藏其先武帝璽上書請立樛氏女爲后"],"note":"婴齐代立即藏其先武帝玺，上书请立邯郸樛氏女为后、兴为嗣，称病不入朝，遣子次公宿卫","evidence":["p5"],"id":"event_016"},
    {"name":"安国少季使南越谕内属","alias":["漢使安國少季徃諭王王太后以入朝"],"note":"元鼎四年（前113年）汉使安国少季往谕王、王太后入朝比内诸侯，终军等宣辞，路博德屯桂阳待使者","evidence":["p6"],"id":"event_017"},
    {"name":"南越请内属","alias":["請比內諸侯三歲一朝除邊關"],"note":"太后数劝王及群臣求内属，上书请比内诸侯，三岁一朝，除边关；天子许之赐印，用汉法比内诸侯","evidence":["p6"],"id":"event_018"},
    {"name":"吕嘉谏阻内属","alias":["嘉數諫止王弗聽有畔心數稱病不見漢使者"],"note":"吕嘉相三王，宗族贵盛，得众心，数谏止王，不听，有畔心，称病不见汉使","evidence":["p7"],"id":"event_019"},
    {"name":"太后置酒谋诛吕嘉","alias":["置酒介漢使者權謀誅嘉使者狐疑莫敢發"],"note":"王、王太后置酒谋借汉使权诛吕嘉，使者狐疑不敢发，太后欲鏦嘉以矛，王止之；嘉出称病阴与大臣作乱","evidence":["p7"],"id":"event_020"},
    {"name":"韩千秋樛乐入越","alias":["遣千秋與王太后弟樛樂將二千人徃"],"note":"天子以庄参不可，遣韩千秋与樛乐将二千人入越","evidence":["p8"],"id":"event_021"},
    {"name":"吕嘉反杀王太后汉使","alias":["與其弟將卒攻殺王太后及漢使者立建德爲王"],"note":"吕嘉反，下令国中攻杀王、太后及汉使者，立建德为王","evidence":["p8"],"id":"event_022"},
    {"name":"韩千秋兵败战死","alias":["越以兵擊千秋等遂滅之"],"note":"越开道给食诱汉军深入，至番禺四十里发兵击灭之；天子封千秋子延年、樛乐子广德为侯","evidence":["p8"],"id":"event_023"},
    {"name":"汉五将军伐南越","alias":["令罪人及江淮以南樓船十萬師徃討之"],"note":"元鼎五年秋，汉遣伏波将军路博德、楼船将军杨仆、戈船下厉将军、驰义侯共五路师会番禺","evidence":["p8","p9"],"id":"event_024"},
    {"name":"楼船伏波会师番禺","alias":["樓船伏波俱進至番禺"],"note":"元鼎六年冬，楼船先陷寻陕破石门，伏波后期与楼船俱至番禺","evidence":["p10"],"id":"event_025"},
    {"name":"番禺火攻破城","alias":["樓船攻敗越人縱火燒城伏波營招降"],"note":"楼船攻败越人纵火烧城，伏波为营招降赐印；犁旦城中皆降伏波","evidence":["p10"],"id":"event_026"},
    {"name":"吕嘉建德夜逃被擒","alias":["嘉建德亡入海蘇弘得建德都稽得嘉"],"note":"吕嘉、建德夜亡入海乘船西去，苏弘擒建德封海常侯，都稽擒嘉封临蔡侯","evidence":["p10"],"id":"event_027"},
    {"name":"苍梧桂林揭阳降汉","alias":["趙光定居翁諭甌駱皆屬漢"],"note":"苍梧王赵光、揭阳令定、桂林监居翁皆降，皆得为侯","evidence":["p11"],"id":"event_028"},
    {"name":"南越平置九郡","alias":["南越已平遂爲九郡"],"note":"元鼎六年南越平，汉于其地置南海、苍梧、郁林、合浦、交趾、九真、日南、珠崖、儋耳九郡","evidence":["p11"],"id":"event_029"},
    {"name":"南越国亡","alias":["五世九十三歲而國亡"],"note":"自尉佗初王至建德亡国共五世九十三年，南越国亡","evidence":["p12"],"id":"event_030"},
]

concepts = [
    {"name":"剖符通使","alias":["剖符通使"],"note":"汉与南越国王分符为信、互通使节的封建盟誓制度","evidence":["p0"],"id":"concept_000"},
    {"name":"和集百越","alias":["和集百越"],"note":"汉初对百越的民族政策，以和平方式安辑百越各部，毋为边患","evidence":["p0"],"id":"concept_001"},
    {"name":"关市","alias":["關市"],"note":"边境互市贸易，高后禁南越关市铁器是引发赵佗称帝的直接原因","evidence":["p1"],"id":"concept_002"},
    {"name":"黄屋左纛","alias":["黃屋左纛"],"note":"帝王车驾仪仗：黄屋是以黄缯为车盖，左纛是在车衡左方设犛牛尾大幢，为帝制专用","evidence":["p1","p2"],"id":"concept_003"},
    {"name":"称制","alias":["稱制"],"note":"代行天子权力、使用皇帝礼仪制度","evidence":["p1"],"id":"concept_004"},
    {"name":"藩臣","alias":["藩臣","藩"],"note":"臣属于中央王朝的附属国，奉贡职、守约束","evidence":["p2","p3","p4"],"id":"concept_005"},
    {"name":"奉贡职","alias":["奉貢職"],"note":"奉行向中央王朝进贡方物的职责","evidence":["p2"],"id":"concept_006"},
    {"name":"朝请","alias":["朝請"],"note":"汉代诸侯王朝见天子的制度，春曰朝，秋曰请","evidence":["p2"],"id":"concept_007"},
    {"name":"宿卫","alias":["宿衞"],"note":"入宫在皇帝身边充当侍卫，西汉时诸侯太子入宿卫为常见的控制与纳质手段","evidence":["p4","p5"],"id":"concept_008"},
    {"name":"内属","alias":["內屬"],"note":"边疆民族或政权请求内附于中央王朝，比内诸侯、用汉法、置汉吏","evidence":["p6","p7","p8"],"id":"concept_009"},
    {"name":"银印","alias":["銀印"],"note":"汉制，丞相、太尉等高级官员授银印青绶，赐吕嘉银印表示汉正式任命南越丞相","evidence":["p6"],"id":"concept_010"},
    {"name":"黥劓刑","alias":["黥劓刑"],"note":"古肉刑：黥为墨面，劓为割鼻；南越除故黥劓刑用汉法","evidence":["p6"],"id":"concept_011"},
    {"name":"尚公主/王女","alias":["尚王女"],"note":"娶帝王之女为妻曰「尚」，吕嘉男尽尚王女、女尽嫁王子，是其宗族与南越王室联姻的制度","evidence":["p7"],"id":"concept_012"},
    {"name":"东乡南乡北乡西乡","alias":["東鄉南鄉北鄉西鄉"],"note":"乡同向，宴席座次方向：东向为尊（汉使坐东向），南向次尊（太后），北向为臣位（王），西向为陪位（吕嘉）","evidence":["p7"],"id":"concept_013"},
    {"name":"伏波将军","alias":["伏波將軍"],"note":"汉代将军名号，路博德为首任伏波将军，后马援亦曾任此职","evidence":["p9","p10","p11"],"id":"concept_014"},
    {"name":"楼船将军","alias":["樓船將軍"],"note":"汉代将军名号，统帅水军楼船之士，杨仆以主爵都尉为楼船将军","evidence":["p9","p10","p11"],"id":"concept_015"},
    {"name":"九郡","alias":["九郡"],"note":"平南越后所置九郡：南海、苍梧、郁林、合浦、交趾、九真、日南、珠崖、儋耳","evidence":["p11"],"id":"concept_016"},
    {"name":"因祸为福","alias":["因禍爲福"],"note":"太史公评路博德语，转祸为福、智虑愈殖","evidence":["p13"],"id":"concept_017"},
    {"name":"成败之转譬若纠墨","alias":["成敗之轉譬若糾墨"],"note":"太史公评语：成败的转换如绞合的绳索一般互相缠绕、互为转化","evidence":["p13"],"id":"concept_018"},
]

relations = [
    {"from":"赵佗（南越王）","to":"任囂","type":"受任南海尉","evidence":["p0"],"id":"rel_000"},
    {"from":"赵佗（南越王）","to":"桂林郡","type":"秦末兼并桂林","evidence":["p0"],"id":"rel_001"},
    {"from":"赵佗（南越王）","to":"象郡","type":"秦末兼并象郡","evidence":["p0"],"id":"rel_002"},
    {"from":"赵佗（南越王）","to":"刘邦（汉高祖）","type":"受汉封为南越王","evidence":["p0"],"id":"rel_003"},
    {"from":"赵佗（南越王）","to":"吕雉（高后）","type":"不满高后禁市","evidence":["p1"],"id":"rel_004"},
    {"from":"赵佗（南越王）","to":"周灶（隆虑侯）","type":"以暑湿拒汉军","evidence":["p1"],"id":"rel_005"},
    {"from":"赵佗（南越王）","to":"闽越","type":"赂遗使役属","evidence":["p1"],"id":"rel_006"},
    {"from":"赵佗（南越王）","to":"刘恒（汉文帝）","type":"受抚去帝称臣","evidence":["p2"],"id":"rel_007"},
    {"from":"刘恒（汉文帝）","to":"陆贾","type":"遣陆贾再使越","evidence":["p2"],"id":"rel_008"},
    {"from":"刘恒（汉文帝）","to":"陈平","type":"诏陈平举使者","evidence":["p2"],"id":"rel_009"},
    {"from":"赵胡（南越文王）","to":"赵佗（南越王）","type":"继佗立为南越王","evidence":["p3"],"id":"rel_010"},
    {"from":"赵胡（南越文王）","to":"郢（闽越王）","type":"遭闽越兴兵攻击","evidence":["p3"],"id":"rel_011"},
    {"from":"刘彻（汉武帝）","to":"郢（闽越王）","type":"兴兵讨伐闽越","evidence":["p3"],"id":"rel_012"},
    {"from":"余善","to":"郢（闽越王）","type":"杀郢降汉","evidence":["p3"],"id":"rel_013"},
    {"from":"刘彻（汉武帝）","to":"庄助","type":"遣庄助谕意南越","evidence":["p4"],"id":"rel_014"},
    {"from":"赵胡（南越文王）","to":"赵婴齐（南越明王）","type":"遣太子婴齐入宿卫","evidence":["p4"],"id":"rel_015"},
    {"from":"赵婴齐（南越明王）","to":"樛太后","type":"娶樛氏生子兴","evidence":["p5"],"id":"rel_016"},
    {"name":None,"from":"赵婴齐（南越明王）","to":"赵兴","type":"立赵兴为太子嗣王","evidence":["p5"],"id":"rel_017"},
    {"from":"赵兴","to":"樛太后","type":"以樛氏为太后","evidence":["p6"],"id":"rel_018"},
    {"from":"安国少季","to":"樛太后","type":"早年私通复又私通","evidence":["p6"],"id":"rel_019"},
    {"from":"刘彻（汉武帝）","to":"安国少季","type":"遣安国少季使越","evidence":["p6"],"id":"rel_020"},
    {"from":"刘彻（汉武帝）","to":"终军","type":"遣终军宣谕南越","evidence":["p6"],"id":"rel_021"},
    {"from":"路博德（伏波将军）","to":"桂阳","type":"将兵屯桂阳待命","evidence":["p6"],"id":"rel_022"},
    {"from":"樛太后","to":"吕嘉","type":"置酒谋诛吕嘉未成","evidence":["p7"],"id":"rel_023"},
    {"from":"赵兴","to":"吕嘉","type":"无意诛杀吕嘉","evidence":["p7"],"id":"rel_024"},
    {"from":"吕嘉","to":"苍梧秦王","type":"与苍梧秦王联姻","evidence":["p7"],"id":"rel_025"},
    {"from":"刘彻（汉武帝）","to":"庄参","type":"欲遣庄参使越","evidence":["p8"],"id":"rel_026"},
    {"from":"韩千秋","to":"刘彻（汉武帝）","type":"自请斩吕嘉报国","evidence":["p8"],"id":"rel_027"},
    {"from":"刘彻（汉武帝）","to":"韩千秋","type":"遣韩千秋入越","evidence":["p8"],"id":"rel_028"},
    {"from":"刘彻（汉武帝）","to":"樛乐","type":"遣樛乐同入越","evidence":["p8"],"id":"rel_029"},
    {"from":"吕嘉","to":"赵兴","type":"攻杀南越王赵兴","evidence":["p8"],"id":"rel_030"},
    {"from":"吕嘉","to":"樛太后","type":"攻杀樛太后","evidence":["p8"],"id":"rel_031"},
    {"from":"吕嘉","to":"赵建德","type":"立赵建德为南越王","evidence":["p8"],"id":"rel_032"},
    {"from":"越人","to":"韩千秋","type":"诱击歼灭韩千秋军","evidence":["p8"],"id":"rel_033"},
    {"from":"刘彻（汉武帝）","to":"韩延年","type":"封韩延年为成安侯","evidence":["p8"],"id":"rel_034"},
    {"from":"刘彻（汉武帝）","to":"樛广德","type":"封樛广德为龙亢侯","evidence":["p8"],"id":"rel_035"},
    {"from":"刘彻（汉武帝）","to":"路博德（伏波将军）","type":"拜伏波将军伐越","evidence":["p9"],"id":"rel_036"},
    {"from":"刘彻（汉武帝）","to":"杨仆（楼船将军）","type":"拜杨仆为楼船将军","evidence":["p9"],"id":"rel_037"},
    {"from":"杨仆（楼船将军）","to":"寻陕","type":"先攻陷寻陕","evidence":["p10"],"id":"rel_038"},
    {"from":"杨仆（楼船将军）","to":"石门","type":"攻破石门","evidence":["p10"],"id":"rel_039"},
    {"from":"苏弘","to":"赵建德","type":"擒获赵建德封侯","evidence":["p10"],"id":"rel_040"},
    {"from":"孙都稽","to":"吕嘉","type":"擒获吕嘉封侯","evidence":["p10"],"id":"rel_041"},
    {"from":"赵光（苍梧王）","to":"路博德（伏波将军）","type":"闻汉兵至自定属汉","evidence":["p11"],"id":"rel_042"},
    {"from":"揭阳令史定","to":"刘彻（汉武帝）","type":"举揭阳降汉","evidence":["p11"],"id":"rel_043"},
    {"from":"居翁","to":"骆越","type":"谕瓯骆属汉","evidence":["p11"],"id":"rel_044"},
    {"from":"刘彻（汉武帝）","to":"南海郡","type":"平南越置九郡","evidence":["p11"],"id":"rel_045"},
]

# 构造最终实体JSON
def make_person(p):
    return {"name":p["name"],"alias":p["alias"],"note":p["note"],"evidence":p["evidence"],"id":p["id"]}
def make_place(p):
    return {"name":p["name"],"alias":p["alias"],"note":p["note"],"evidence":p["evidence"],"id":p["id"]}
def make_event(e):
    return {"name":e["name"],"alias":e["alias"],"note":e["note"],"evidence":e["evidence"],"id":e["id"]}
def make_concept(c):
    return {"name":c["name"],"alias":c["alias"],"note":c["note"],"evidence":c["evidence"],"id":c["id"]}
def make_rel(r):
    return {"from":r["from"],"to":r["to"],"type":r["type"],"evidence":r["evidence"],"id":r["id"]}

final = {
    "book_id": BOOK_ID,
    "chapter_id": CHAPTER_ID,
    "chapter_title": CHAPTER_TITLE,
    "version": "final",
    "generated_at": datetime.now().isoformat(),
    "entities": {
        "persons": [make_person(p) for p in persons],
        "places": [make_place(p) for p in places if p["name"] != "南海"] + [make_place(places[32])],
        "events": [make_event(e) for e in events],
        "concepts": [make_concept(c) for c in concepts],
        "relations": [make_rel(r) for r in relations],
    }
}

# 校验端点
names = set()
for k in ["persons","places","events","concepts"]:
    for e in final["entities"][k]:
        names.add(e["name"])
err = []
for r in final["entities"]["relations"]:
    if r["from"] not in names:
        err.append(f"from not found: {r['from']}")
    if r["to"] not in names:
        err.append(f"to not found: {r['to']}")
print("端点错误:", err if err else "无")

# 校验段号
max_p = N-1
for k in ["persons","places","events","concepts","relations"]:
    for e in final["entities"][k]:
        for ev in e["evidence"]:
            m = re.match(r"p(\d+)", ev)
            if m and int(m.group(1)) > max_p:
                err.append(f"段号越界: {k} {e.get('name') or e.get('from')+'->'+e.get('to')} {ev}")
print("段号校验后:", len(err), "个错误")

# 关系type长度2-8字
for r in final["entities"]["relations"]:
    L = len(r["type"])
    if L < 2 or L > 8:
        err.append(f"关系type长度异常: {r['type']} ({L}字)")
print("关系type校验后:", len(err), "个错误")

out_path = f"{BASE}/data/books/shiji/ontology/实体-定稿-{CHAPTER_TITLE}.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)
print("写入:", out_path)

# 初稿同样内容但 version=draft
draft = json.loads(json.dumps(final, ensure_ascii=False))
draft["version"] = "draft"
draft_path = f"{BASE}/data/books/shiji/ontology/实体-初稿-{CHAPTER_TITLE}.json"
with open(draft_path, "w", encoding="utf-8") as f:
    json.dump(draft, f, ensure_ascii=False, indent=2)
print("写入:", draft_path)
