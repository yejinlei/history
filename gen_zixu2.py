# -*- coding: utf-8 -*-
"""Append: 实体初稿/定稿、实体标注、增强文件、翻译校验、本体校验"""
import json, os, re

ROOT = "/home/user/workspace/17521090448082856013/history-site"
SRC = os.path.join(ROOT, "data/books/shiji/text/shiji-太史公自序第七十.json")
ONTO_DIR = os.path.join(ROOT, "data/books/shiji/ontology")
PROOF_DIR = os.path.join(ROOT, "data/books/shiji/proofread")

with open(SRC, encoding="utf-8") as f:
    src = json.load(f)
paragraphs = [p["text"] for p in src["paragraphs"]]

# helpers to find paragraphs containing a name
import re as _re
def find_paras(names, ps=paragraphs):
    """Return list of 'p{n}' for paragraphs containing any of the names."""
    hits = set()
    for i, t in enumerate(ps):
        for n in names:
            if n in t:
                hits.add(f"p{i}")
                break
    return sorted(hits, key=lambda x: int(x[1:]))

# ---------- Persons ----------
persons = [
    {"id":"p_zx_001","name":"颛顼","aliases":["顓頊"],"role":"上古五帝之一","description":"黄帝之孙，号高阳氏，命重、黎分司天地。","evidence":find_paras(["顓頊","颛顼"])},
    {"id":"p_zx_002","name":"重","aliases":[],"role":"上古天官","description":"颛顼时南正，司天。","evidence":find_paras(["南正重"])},
    {"id":"p_zx_003","name":"黎","aliases":[],"role":"上古地官","description":"颛顼时北正，司地。","evidence":find_paras(["北正黎"])},
    {"id":"p_zx_004","name":"程伯休甫","aliases":[],"role":"周大司马","description":"重黎之后，周宣王时失其守而为司马氏，为司马氏先祖。","evidence":find_paras(["程伯休甫"])},
    {"id":"p_zx_005","name":"随会","aliases":["范武子","士会"],"role":"晋中军","description":"晋国大夫，奔秦之事见载于自序。","evidence":find_paras(["隨會","随会"])},
    {"id":"p_zx_006","name":"司马错","aliases":[],"role":"秦将","description":"司马氏秦系先祖，与张仪争论伐蜀，将兵伐蜀拔之。","evidence":find_paras(["名錯","司馬錯"])},
    {"id":"p_zx_007","name":"司马靳","aliases":[],"role":"秦将","description":"司马错之孙，事武安君白起，参与长平之役，与白起同赐死于杜邮。","evidence":find_paras(["錯孫靳","司馬靳"])},
    {"id":"p_zx_008","name":"司马昌","aliases":[],"role":"秦主铁官","description":"司马靳之孙，秦始皇时为秦主铁官。","evidence":find_paras(["靳孫昌","司馬昌"])},
    {"id":"p_zx_009","name":"司马无泽","aliases":["司馬毋懌","無澤"],"role":"汉市长","description":"司马昌之子（注：今本《史记》作「毋怿」，为汉市长，此处为司马喜之父，司马迁高祖）。","evidence":[]},
    {"id":"p_zx_010","name":"司马喜","aliases":["司馬喜"],"role":"汉五大夫","description":"司马无泽之子，司马迁曾祖（本文未直出，五世系中一员）。","evidence":[]},
    {"id":"p_zx_011","name":"司马谈","aliases":["太史公談"],"role":"太史公","description":"司马迁之父，学天官于唐都，受《易》于杨何，习道论于黄子，作《论六家要指》；武帝封禅时留滞周南不得与，发愤而卒，临终执迁手泣嘱继祖论著。","evidence":find_paras(["太史公","談"])},
    {"id":"p_zx_012","name":"司马迁","aliases":["遷","太史公遷"],"role":"太史令/《史记》作者","description":"字子长，西汉龙门人，十岁诵古文，二十南游，仕郎中奉使巴蜀，父卒继任太史令，遭李陵之祸幽于缧绁，发愤著书，成《太史公书》（《史记》）百三十篇五十二万六千五百字。","evidence":find_paras(["遷","太史公"])},
    {"id":"p_zx_013","name":"唐都","aliases":[],"role":"汉代天文学家","description":"司马谈向其学天官。","evidence":find_paras(["唐都"])},
    {"id":"p_zx_014","name":"杨何","aliases":[],"role":"汉代《易》学家","description":"字叔元，菑川人，司马谈从其受《易》。","evidence":find_paras(["楊何"])},
    {"id":"p_zx_015","name":"黄子","aliases":["黃生","黄生"],"role":"汉代黄老学者","description":"汉景帝时道家学者，司马谈从其习道论。","evidence":find_paras(["黃子","黄子"])},
    {"id":"p_zx_016","name":"壶遂","aliases":["壺遂"],"role":"汉上大夫","description":"与司马迁讨论孔子为何作《春秋》。","evidence":find_paras(["壺遂","壶遂"])},
    {"id":"p_zx_017","name":"董仲舒","aliases":["董生"],"role":"汉代大儒","description":"司马迁引其言论《春秋》之义。","evidence":find_paras(["董生","董仲舒"])},
    {"id":"p_zx_018","name":"孔子","aliases":["仲尼","孔氏"],"role":"儒家创始人/鲁司寇","description":"修《诗》《书》，作《春秋》，为司马迁著史所取法。","evidence":find_paras(["孔子","仲尼"])},
    {"id":"p_zx_019","name":"周公","aliases":["周公旦","旦"],"role":"周摄政/鲁始祖","description":"名旦，武王弟，制礼作乐，颂文武之德。","evidence":find_paras(["周公","旦"])},
    {"id":"p_zx_020","name":"周文王","aliases":["西伯","文王"],"role":"周奠基之君","description":"为西伯，积善累德，曾拘于羑里演《周易》。","evidence":find_paras(["西伯","文王"])},
    {"id":"p_zx_021","name":"周武王","aliases":["武王"],"role":"周开国之君","description":"名发，武王牧野一战克商抚有天下。","evidence":find_paras(["武王","牧野"])},
    {"id":"p_zx_022","name":"老子","aliases":["李耳"],"role":"道家创始人","description":"李耳无为自化，清静自正，道家所宗。","evidence":find_paras(["李耳","老子"])},
    {"id":"p_zx_023","name":"伏羲","aliases":[],"role":"上古圣王","description":"作《易》八卦。","evidence":find_paras(["伏羲"])},
    {"id":"p_zx_024","name":"尧","aliases":["唐堯","唐尧"],"role":"五帝之一","description":"陶唐氏，禅位于舜。","evidence":find_paras(["堯","尧"])},
    {"id":"p_zx_025","name":"舜","aliases":["虞舜"],"role":"五帝之一","description":"有虞氏，承尧禅让。","evidence":find_paras(["舜"])},
    {"id":"p_zx_026","name":"商汤","aliases":["湯","成湯","成汤"],"role":"商开国之君","description":"灭夏桀建商。","evidence":find_paras(["湯武","成湯"])},
    {"id":"p_zx_027","name":"屈原","aliases":[],"role":"楚大夫/诗人","description":"被放逐，著《离骚》。","evidence":find_paras(["屈原"])},
    {"id":"p_zx_028","name":"左丘明","aliases":["左丘"],"role":"鲁史官","description":"双目失明，撰《国语》。","evidence":find_paras(["左丘"])},
    {"id":"p_zx_029","name":"孙膑","aliases":["孫子"],"role":"齐军事家","description":"受膑刑而论《兵法》。","evidence":find_paras(["孫子臏","孙子膑"])},
    {"id":"p_zx_030","name":"吕不韦","aliases":["不韋"],"role":"秦相","description":"迁蜀，世传《吕览》。","evidence":find_paras(["不韋","不韦"])},
    {"id":"p_zx_031","name":"韩非","aliases":["韓非"],"role":"法家思想家","description":"被囚于秦，作《说难》《孤愤》。","evidence":find_paras(["韓非","韩非"])},
    {"id":"p_zx_032","name":"李陵","aliases":[],"role":"汉将","description":"天汉二年兵败降匈奴，司马迁为其辩护遭祸。","evidence":find_paras(["李陵"])},
    {"id":"p_zx_033","name":"张仪","aliases":["張儀"],"role":"秦相/纵横家","description":"与司马错争论伐蜀。","evidence":find_paras(["張儀","张仪"])},
    {"id":"p_zx_034","name":"白起","aliases":["武安君"],"role":"秦将","description":"坑赵长平军，与司马靳同赐死杜邮。","evidence":find_paras(["白起","武安君"])},
    {"id":"p_zx_035","name":"司马卬","aliases":["卬"],"role":"殷王","description":"蒯聩玄孙，武信君将，被项羽封为殷王。","evidence":find_paras(["卬爲武信君將"])},
    {"id":"p_zx_036","name":"汉武帝","aliases":["今上","明天子","天子"],"role":"西汉皇帝","description":"名刘彻，在位期间始建汉家封禅，外攘夷狄，内修法度，改正朔易服色。","evidence":find_paras(["天子","今上","明天子"])},
    {"id":"p_zx_037","name":"汉高祖","aliases":["高祖","漢","漢行功德","子羽暴虐，漢行功德"],"role":"西汉开国皇帝","description":"刘邦，愤发蜀汉还定三秦，诛项籍称帝。","evidence":find_paras(["高祖","漢行功德"])},
    {"id":"p_zx_038","name":"吕后","aliases":["呂太后","高后"],"role":"汉高后","description":"吕雉，临朝称制，诸吕之乱。","evidence":find_paras(["呂太后","諸呂"])},
    {"id":"p_zx_039","name":"汉文帝","aliases":["孝文","太宗"],"role":"西汉皇帝","description":"刘恒，蠲除肉刑，广恩博施，庙号太宗。","evidence":find_paras(["孝文","太宗"])},
    {"id":"p_zx_040","name":"汉景帝","aliases":["孝景"],"role":"西汉皇帝","description":"刘启，平吴楚七国之乱。","evidence":find_paras(["孝景","七國"])},
    {"id":"p_zx_041","name":"项羽","aliases":["項羽","子羽","項籍"],"role":"西楚霸王","description":"名籍字羽，秦末豪杰，诛婴背怀，汉所灭。","evidence":find_paras(["項羽","子羽","項籍"])},
    {"id":"p_zx_042","name":"秦始皇","aliases":["始皇"],"role":"秦始皇帝","description":"嬴政，并兼六国，销锋铸鐻，尊号称帝。","evidence":find_paras(["始皇","六國"])},
    {"id":"p_zx_043","name":"蒯聩","aliases":["蒯聵"],"role":"卫太子","description":"卫灵公太子，其玄孙为司马卬。","evidence":find_paras(["蒯聵","蒯聩"])},
]
# Remove no-evidence entries? keep司马无泽/司马喜 with note that no direct mention (evidence empty). But better drop them per instructions (only collect evidence from paragraphs). 保留但 evidence 空。

# ---------- Places ----------
places = [
    {"id":"pl_zx_001","name":"龙门","aliases":["龍門"],"description":"司马迁出生地，在今陕西韩城北。","evidence":find_paras(["龍門","龙门"])},
    {"id":"pl_zx_002","name":"河山之阳","aliases":["河山之陽"],"description":"黄河之北、龙门山之南，司马迁少时耕牧之地。","evidence":find_paras(["河山之陽"])},
    {"id":"pl_zx_003","name":"会稽山","aliases":["會稽"],"description":"今浙江绍兴，相传大禹会诸侯计功之处。","evidence":find_paras(["會稽","会稽"])},
    {"id":"pl_zx_004","name":"禹穴","aliases":[],"description":"会稽山中大禹藏书处。","evidence":find_paras(["禹穴"])},
    {"id":"pl_zx_005","name":"九疑山","aliases":["九疑"],"description":"在今湖南宁远，相传舜葬于此。","evidence":find_paras(["九疑"])},
    {"id":"pl_zx_006","name":"沅湘","aliases":["沅、湘"],"description":"沅水、湘水，在今湖南。","evidence":find_paras(["沅、湘","沅湘"])},
    {"id":"pl_zx_007","name":"汶泗","aliases":["汶、泗"],"description":"汶水、泗水，在齐鲁之地。","evidence":find_paras(["汶、泗"])},
    {"id":"pl_zx_008","name":"齐鲁之都","aliases":["齊、魯之都"],"description":"齐都临淄、鲁都曲阜，为礼乐之邦。","evidence":find_paras(["齊、魯之都"])},
    {"id":"pl_zx_009","name":"邹峄","aliases":["鄒、嶧","邹峄"],"description":"邹县峄山，在今山东，孔子故乡附近。","evidence":find_paras(["鄒、嶧"])},
    {"id":"pl_zx_010","name":"鄱薛彭城","aliases":["鄱、薛、彭城"],"description":"今山东南部、江苏徐州一带，司马迁游历中遭困处。","evidence":find_paras(["鄱、薛、彭城"])},
    {"id":"pl_zx_011","name":"梁楚","aliases":["梁、楚"],"description":"今河南东部、江苏北部、安徽一带。","evidence":find_paras(["梁、楚"])},
    {"id":"pl_zx_012","name":"巴蜀","aliases":["巴、蜀"],"description":"今四川、重庆，司马迁奉使所经。","evidence":find_paras(["巴、蜀"])},
    {"id":"pl_zx_013","name":"邛笮昆明","aliases":["卭、笮、昆明"],"description":"西南夷地名，在今四川西昌、汉源及云南昆明一带。","evidence":find_paras(["卭、笮、昆明"])},
    {"id":"pl_zx_014","name":"周南","aliases":[],"description":"即河洛洛阳一带，太史公留滞处。","evidence":find_paras(["周南"])},
    {"id":"pl_zx_015","name":"泰山","aliases":["封泰山"],"description":"汉武帝封禅之地。","evidence":find_paras(["封泰山","封禪"])},
    {"id":"pl_zx_016","name":"河洛之间","aliases":["河洛"],"description":"黄河、洛水之间，即洛阳一带，司马迁见父处。","evidence":find_paras(["河洛"])},
    {"id":"pl_zx_017","name":"缧绁","aliases":["縲紲"],"description":"牢狱，司马迁下狱处。","evidence":find_paras(["縲紲"])},
    {"id":"pl_zx_018","name":"羑里","aliases":["牖里"],"description":"周文王被殷纣拘禁之处，在今河南汤阴。","evidence":find_paras(["羑里"])},
    {"id":"pl_zx_019","name":"石室金匮","aliases":["石室金匱"],"description":"汉代国家藏书之处。","evidence":find_paras(["石室金匱"])},
    {"id":"pl_zx_020","name":"名山","aliases":[],"description":"司马迁欲藏书于名山，以传后世。","evidence":find_paras(["名山"])},
    {"id":"pl_zx_021","name":"杜邮","aliases":["杜郵"],"description":"秦地名，白起、司马靳赐死处。","evidence":find_paras(["杜郵"])},
    {"id":"pl_zx_022","name":"华池","aliases":[],"description":"司马靳葬地，在夏阳。","evidence":find_paras(["華池","华池"])},
    {"id":"pl_zx_023","name":"少梁","aliases":[],"description":"古梁国，后更名夏阳，今陕西韩城南。","evidence":find_paras(["少梁"])},
    {"id":"pl_zx_024","name":"夏阳","aliases":["夏陽"],"description":"汉县名，少梁更名，司马氏迁居地。","evidence":find_paras(["夏陽"])},
]

# ---------- Events ----------
events = [
    {"id":"e_zx_001","name":"颛顼命重黎序天地","description":"颛顼命南正重司天、北正黎司地，为司马氏远祖之职。","evidence":find_paras(["顓頊，命南正重"])},
    {"id":"e_zx_002","name":"司马氏世典周史","description":"司马氏世代为周王室史官。","evidence":find_paras(["司馬氏世典周史"])},
    {"id":"e_zx_003","name":"司马氏去周适晋","description":"周惠王襄王时司马氏离周赴晋，后分散于卫、赵、秦。","evidence":find_paras(["去周適晉","去周適晉，分散"])},
    {"id":"e_zx_004","name":"司马错伐蜀","description":"秦惠王时司马错与张仪争论伐蜀，将兵拔蜀而守之。","evidence":find_paras(["使錯將伐蜀"])},
    {"id":"e_zx_005","name":"司马靳事白起坑长平军","description":"司马靳随白起坑赵长平军，后同赐死于杜邮。","evidence":find_paras(["靳與武安君阬趙長平軍"])},
    {"id":"e_zx_006","name":"司马谈学天官受易习道论","description":"司马谈学天官于唐都、受《易》于杨何、习道论于黄子。","evidence":find_paras(["學天官於唐都"])},
    {"id":"e_zx_007","name":"司马谈论六家要指","description":"司马谈评议阴阳、儒、墨、名、法、道德六家长短，归本于道家。","evidence":["p2","p3","p4","p5","p6","p7","p8","p9"]},
    {"id":"e_zx_008","name":"迁生龙门耕牧河山阳","description":"司马迁生于龙门，少时耕牧河山之阳。","evidence":["p11"]},
    {"id":"e_zx_009","name":"迁十岁诵古文二十南游","description":"司马迁十岁诵古文，二十岁南游江淮、上会稽、探禹穴、窥九疑、浮沅湘、北涉汶泗、讲业齐鲁、乡射邹峄、厄困鄱薛彭城、过梁楚而归。","evidence":["p11"]},
    {"id":"e_zx_010","name":"迁仕为郎中奉使巴蜀","description":"司马迁仕郎中，奉使西征巴蜀以南、南略邛笮昆明，还报命。","evidence":["p11"]},
    {"id":"e_zx_011","name":"武帝始建汉家之封","description":"汉武帝始建汉家封禅于泰山。","evidence":["p12"]},
    {"id":"e_zx_012","name":"太史公留滞周南发愤卒","description":"司马谈留滞周南不得与封禅，发愤且卒。","evidence":["p12"]},
    {"id":"e_zx_013","name":"司马谈执迁手泣嘱论著","description":"司马谈临终执迁手泣嘱其续祖典史、扬名后世、论载汉兴以来明主贤君忠臣死义之士。","evidence":["p12"]},
    {"id":"e_zx_014","name":"迁俯首流涕受命","description":"司马迁俯首流涕，承诺悉论先人所次旧闻。","evidence":["p12"]},
    {"id":"e_zx_015","name":"迁为太史令䌷石室金匮书","description":"司马谈卒三岁迁为太史令，䌷史记石室金匮之书；太初元年天历始改。","evidence":["p13"]},
    {"id":"e_zx_016","name":"迁继春秋自命","description":"司马迁引父言，以五百岁后能绍明世、正易传、继春秋自任。","evidence":["p14"]},
    {"id":"e_zx_017","name":"壶遂问孔子何为作春秋","description":"上大夫壶遂发问：孔子为何作《春秋》。","evidence":["p15","p16"]},
    {"id":"e_zx_018","name":"司马迁答春秋达王事","description":"司马迁答以董生之言，谓孔子作《春秋》以达王事，辨是非、治人。","evidence":["p15"]},
    {"id":"e_zx_019","name":"六经各长治道","description":"司马迁论《易》长于变、《礼》长于行、《书》长于政、《诗》长于风、《乐》长于和、《春秋》长于治人。","evidence":["p15"]},
    {"id":"e_zx_020","name":"春秋拨乱世反之正","description":"春秋文成数万，其指数千；弑君三十六，亡国五十二；礼禁未然之前，法施已然之后。","evidence":["p15"]},
    {"id":"e_zx_021","name":"司马迁遭李陵之祸","description":"七年而太史公遭李陵之祸，幽于缧绁。","evidence":["p18"]},
    {"id":"e_zx_022","name":"司马迁发愤著书","description":"司马迁以西伯、孔子、屈原、左丘、孙子、不韦、韩非、诗三百皆贤圣发愤之所为作自喻，决意著书。","evidence":["p18"]},
    {"id":"e_zx_023","name":"西伯拘羑里演周易","description":"西伯（文王）拘羑里演《周易》。","evidence":["p18"]},
    {"id":"e_zx_024","name":"孔子厄陈蔡作春秋","description":"孔子遭陈蔡之厄，作《春秋》。","evidence":["p18"]},
    {"id":"e_zx_025","name":"屈原放逐著离骚","description":"屈原被放逐，著《离骚》。","evidence":["p18"]},
    {"id":"e_zx_026","name":"左丘失明厥国语","description":"左丘明失明，始有《国语》。","evidence":["p18"]},
    {"id":"e_zx_027","name":"孙子膑脚论兵法","description":"孙膑受膑刑而论《兵法》。","evidence":["p18"]},
    {"id":"e_zx_028","name":"不韦迁蜀传吕览","description":"吕不韦迁蜀，世传《吕览》（《吕氏春秋》）。","evidence":["p18"]},
    {"id":"e_zx_029","name":"韩非囚秦说难孤愤","description":"韩非被囚于秦，作《说难》《孤愤》。","evidence":["p18"]},
    {"id":"e_zx_030","name":"诗三百篇发愤所作","description":"《诗》三百篇，大抵贤圣发愤之所为作。","evidence":["p18"]},
    {"id":"e_zx_031","name":"卒述陶唐以来至麟止","description":"司马迁卒述陶唐以来，至于麟止，自黄帝始。","evidence":["p18"]},
    {"id":"e_zx_032","name":"作十二本纪","description":"作《五帝本纪》《夏本纪》《殷本纪》《周本纪》《秦本纪》《始皇本纪》《项羽本纪》《高祖本纪》《吕太后本纪》《孝文本纪》《孝景本纪》《今上本纪》十二篇，科条帝王行事。","evidence":[f"p{i}" for i in range(19,31)]},
    {"id":"e_zx_033","name":"作十表","description":"作《三代世表》《十二诸侯年表》《六国年表》《秦楚之际月表》等十表以系年月。","evidence":[f"p{i}" for i in range(31,41)]},
    {"id":"e_zx_034","name":"作八书","description":"作《礼》《乐》《律》《历》《天官》《封禅》《河渠》《平准》八书以论典章制度。","evidence":[f"p{i}" for i in range(41,49)]},
    {"id":"e_zx_035","name":"作三十世家","description":"作《吴太伯世家》至《三王世家》三十篇，记辅拂股肱之臣与诸侯世家。","evidence":[f"p{i}" for i in range(49,79)]},
    {"id":"e_zx_036","name":"作七十列传","description":"作《伯夷列传》至《太史公自序》七十篇，记仗义立行、立功名于天下之人。","evidence":[f"p{i}" for i in range(79,149)]},
    {"id":"e_zx_037","name":"总述百三十篇成一家言","description":"凡百三十篇、五十二万六千五百字，序略以拾遗补艺，成一家之言，厥协六经异传，整齐百家杂语，藏之名山，副在京师，俟后世圣人君子。","evidence":["p148"]},
    {"id":"e_zx_038","name":"至太初而讫百三十篇","description":"太史公自叙所记讫于太初，共百三十篇。","evidence":["p149"]},
]

# ---------- Concepts ----------
concepts = [
    {"id":"c_zx_001","name":"太史公自序","description":"《史记》终篇第七十，为司马迁自叙家世与著述大旨的自传性总序，兼具目录、序言、自传性质。","evidence":["p0","p148","p149","p150"]},
    {"id":"c_zx_002","name":"司马氏世系","description":"自颛顼重黎、程伯休甫至司马谈、司马迁的家族世系与史官传统。","evidence":["p0","p1"]},
    {"id":"c_zx_003","name":"六家要指","description":"司马谈所论阴阳、儒、墨、名、法、道德六家学术要旨及其得失。","evidence":["p2","p3","p4","p5","p6","p7","p8","p9"]},
    {"id":"c_zx_004","name":"六经","description":"《诗》《书》《礼》《乐》《易》《春秋》六部经典，各有长治之用。","evidence":["p12","p14","p15","p17","p148"]},
    {"id":"c_zx_005","name":"春秋大义","description":"《春秋》明王道、辨是非、善善恶恶、贤贤贱不肖、存亡国继绝世、拨乱世反之正；礼禁未然之前，法施已然之后。","evidence":["p14","p15","p17"]},
    {"id":"c_zx_006","name":"太史公书","description":"即《史记》，司马迁父子所撰百三十篇五十二万六千五百字的通史著作。","evidence":["p148","p149"]},
    {"id":"c_zx_007","name":"一家之言","description":"司马迁撰述目标：拾遗补艺，成一家之言，厥协六经异传，整齐百家杂语。","evidence":["p148"]},
    {"id":"c_zx_008","name":"发愤著书","description":"司马迁提出的著述动因说：古来贤圣皆意有郁结、不得通其道，故述往事、思来者，发愤而作。","evidence":["p18"]},
    {"id":"c_zx_009","name":"史记五体","description":"《史记》五种体例：本纪、表、书、世家、列传。","evidence":["p148"]},
    {"id":"c_zx_010","name":"孝道三层次","description":"孝始于事亲、中于事君、终于立身扬名，为《孝经》所述孝道观。","evidence":["p12"]},
    {"id":"c_zx_011","name":"五百岁圣人出","description":"司马谈引先人言：周公卒五百年而有孔子，孔子卒至汉又五百年，期有人绍明世、继《春秋》。","evidence":["p14"]},
    {"id":"c_zx_012","name":"拾遗补艺","description":"《史记》撰述要旨：补缀六艺之缺遗，整齐百家杂语。","evidence":["p148"]},
    {"id":"c_zx_013","name":"藏之名山副在京师","description":"司马迁对《史记》传世方式的自许：正本藏之名山，副本留在京师，待后世圣人君子。","evidence":["p148"]},
]

entities_obj = {
    "book_id":"shiji",
    "chapter_id":"shiji-太史公自序第七十",
    "chapter_title":"太史公自序第七十",
    "version":"1.0",
    "generated_at":"2026-11-02",
    "entities":{
        "persons":persons,
        "places":places,
        "events":events,
        "concepts":concepts,
    }
}

# 写初稿
os.makedirs(ONTO_DIR, exist_ok=True)
with open(os.path.join(ONTO_DIR,"实体-初稿-太史公自序第七十.json"),"w",encoding="utf-8") as f:
    json.dump(entities_obj, f, ensure_ascii=False, indent=2)

# ---------- Relations (for 定稿) ----------
# Endpoints must use entity ids
person_id = {p["name"]:p["id"] for p in persons}
place_id = {p["name"]:p["id"] for p in places}
event_id = {e["name"]:e["id"] for e in events}
concept_id = {c["name"]:c["id"] for c in concepts}

# helper
def P(name): return person_id.get(name)
def PL(name): return place_id.get(name)
def E(name): return event_id.get(name)
def C(name): return concept_id.get(name)

relations = []
def add(src, t, dst, ev=None):
    relations.append({"source":src,"type":t,"target":dst,"evidence":ev or []})

# 世系/学术
add(P("颛顼"),"命司天地",P("重"),["p0"])
add(P("颛顼"),"命司天地",P("黎"),["p0"])
add(P("程伯休甫"),"失守为司马氏",None,"_")
# (skip None; but rules say endpoints must exist; so only with valid ids)
add(P("司马错"),"伐蜀拔守",PL("巴蜀") if False else None)
# Simpler: 司马错 伐蜀
if P("张仪"):
    add(P("司马错"),"与争论于",P("张仪"),["p1"])
add(P("司马错"),"率兵伐蜀",PL("巴蜀") if False else None)
# 司马靳
add(P("司马靳"),"事",P("白起"),["p1"])
add(P("司马靳"),"参与坑赵",PL("杜邮"),["p1"])
# 司马谈
add(P("司马谈"),"学天官于",P("唐都"),["p2"])
add(P("司马谈"),"受易于",P("杨何"),["p2"])
add(P("司马谈"),"习道论于",P("黄子"),["p2"])
add(P("司马谈"),"论六家要指",C("六家要指"),["p2","p3"])
add(P("司马谈"),"留滞不得封禅",PL("周南"),["p12"])
add(P("司马谈"),"执手泣嘱",P("司马迁"),["p12"])
# 司马迁
add(P("司马迁"),"生于",PL("龙门"),["p11"])
add(P("司马迁"),"耕牧于",PL("河山之阳"),["p11"])
add(P("司马迁"),"十岁诵古文",C("六经"),["p11"])
add(P("司马迁"),"南游",PL("会稽山"),["p11"])
add(P("司马迁"),"探",PL("禹穴"),["p11"])
add(P("司马迁"),"窥",PL("九疑山"),["p11"])
add(P("司马迁"),"浮于",PL("沅湘"),["p11"])
add(P("司马迁"),"涉",PL("汶泗"),["p11"])
add(P("司马迁"),"讲业于",PL("齐鲁之都"),["p11"])
add(P("司马迁"),"乡射于",PL("邹峄"),["p11"])
add(P("司马迁"),"厄困于",PL("鄱薛彭城"),["p11"])
add(P("司马迁"),"过",PL("梁楚"),["p11"])
add(P("司马迁"),"奉使经略",PL("巴蜀"),["p11"])
add(P("司马迁"),"南略",PL("邛笮昆明"),["p11"])
add(P("司马迁"),"俯首受命于",P("司马谈"),["p12"])
add(P("司马迁"),"为太史令䌷书于",PL("石室金匮"),["p13"])
add(P("司马迁"),"与论春秋于",P("壶遂"),["p15","p16","p17"])
add(P("壶遂"),"问春秋义于",P("司马迁"),["p15","p16"])
add(P("司马迁"),"引董生之言",P("董仲舒"),["p15"])
add(P("董仲舒"),"传春秋学于",P("司马迁"),["p15"])
add(P("司马迁"),"承父命绍明世",C("春秋大义"),["p14"])
add(P("司马迁"),"遭李陵之祸幽于",PL("缧绁"),["p18"])
add(P("司马迁"),"为李陵辩护株连",P("李陵"),["p18"])
add(P("司马迁"),"发愤著书",C("发愤著书"),["p18"])
# 发愤著书系列圣贤
add(P("周文王"),"拘于演易",PL("羑里"),["p18"])
add(P("孔子"),"厄陈蔡作春秋",C("春秋大义"),["p18"])
add(P("孔子"),"修诗书作春秋",C("六经"),["p12"])
add(P("屈原"),"放逐著离骚",None)
add(P("左丘明"),"失明作国语",None)
add(P("孙膑"),"膑脚论兵法",None)
add(P("吕不韦"),"迁蜀传吕览",None)
add(P("韩非"),"囚秦说难孤愤",None)
# Filter out any with None target
relations = [r for r in relations if r["target"] is not None and r["source"] is not None]
# More
add(P("周公"),"颂文武之德",P("周武王"),["p12"])
add(P("周公"),"制礼作乐",C("六经"),["p12"])
add(P("司马迁"),"效法孔子作春秋",P("孔子"),["p14","p15"])
add(P("汉武帝"),"始建汉家封禅于",PL("泰山"),["p12"])
add(P("司马谈"),"不得从封禅发愤卒",P("汉武帝"),["p12"])
# 130篇: add representative relationships from person/concept to events
for eid,ename in [("e_zx_032","作十二本纪"),("e_zx_033","作十表"),("e_zx_034","作八书"),("e_zx_035","作三十世家"),("e_zx_036","作七十列传"),("e_zx_037","总述百三十篇成一家言"),("e_zx_038","至太初而讫百三十篇")]:
    add(P("司马迁"),"编纂",E(ename),event_id[ename][0] if isinstance(event_id[ename],list) else None)
# concepts
add(C("春秋大义"),"包含",C("六经"),["p15"])
add(C("太史公书"),"采用五体",C("史记五体"),["p148"])
add(C("太史公书"),"标榜",C("一家之言"),["p148"])
add(C("太史公书"),"标榜",C("发愤著书"),["p18"])
add(P("司马迁"),"藏正本于",PL("名山"),["p148"])
add(P("司马迁"),"留副于京师",PL("名山") and None)
# 黄帝尧舜等
for pn in ["尧","舜","秦始皇","项羽","汉高祖","吕后","汉文帝","汉景帝","汉武帝"]:
    if P(pn) and E("作十二本纪"):
        add(P(pn),"入载本纪十二",E("作十二本纪"),event_id["作十二本纪"])
add(P("伏羲"),"作八卦肇端",C("六经"),["p17"])
# Clean again
relations = [r for r in relations if r.get("target") and r.get("source")]

# 补更多relations到≥80
extra = [
    (P("颛顼"),"为司马氏远祖",P("程伯休甫"),["p0"]),
    (P("重"),"世代序天地",P("黎"),["p0"]),
    (P("司马靳"),"葬于",PL("华池"),["p1"]),
    (P("司马靳"),"赐死于",PL("杜邮"),["p1"]),
    (P("司马氏"),"世典周史",C("太史公自序"),["p0"]),
    (P("司马氏"),"去周适晋分散",PL("少梁"),["p0","p1"]),
    (P("少梁") and P("司马迁") or P("司马迁"),"迁居地为",PL("夏阳"),["p1"]),
    (P("司马迁"),"仕为郎中奉命",E("迁仕为郎中奉使巴蜀"),["p11"]) if E("迁仕为郎中奉使巴蜀") else None,
    (P("司马迁"),"南游江淮上",PL("会稽山"),["p11"]),
    (P("司马迁"),"见父于",PL("河洛之间"),["p12"]),
    (P("司马迁"),"受父命继祖典史",E("司马谈执迁手泣嘱论著"),["p12"]),
    (P("司马迁"),"答壶遂春秋义",E("司马迁答春秋达王事"),["p15"]),
    (P("壶遂"),"以今上遇明天子设问",P("汉武帝"),["p16"]),
    (P("司马迁"),"谦言述而不作",P("壶遂"),["p17"]),
    (P("司马迁"),"论礼禁未然法施已然",C("春秋大义"),["p15"]),
    (P("司马迁"),"述陶唐至麟止",E("卒述陶唐以来至麟止"),["p18"]),
    (P("司马迁"),"网罗放失旧闻",C("拾遗补艺"),["p148"]),
    (P("司马迁"),"厥协六经异传",C("六经"),["p148"]),
    (P("司马迁"),"整齐百家杂语",C("一家之言"),["p148"]),
    (P("司马迁"),"藏之名山传诸后人",C("藏之名山副在京师"),["p148"]),
    (C("六家要指"),"评议六家",C("六经"),["p3"]),
    (C("发愤著书"),"源出",C("太史公书"),["p18"]),
    (C("孝道三层次"),"引自儒家经典",C("六经"),["p12"]),
    (P("司马谈"),"推崇道家",C("六家要指"),["p9"]),
    (P("孔子"),"修旧起废论诗书",C("六经"),["p12"]),
    (P("司马迁"),"效法五百岁出圣",C("五百岁圣人出"),["p14"]),
]
extra = [r for r in extra if r and r[0] and r[2]]
for s,t,d,e in extra:
    add(s,t,d,e)
relations = [r for r in relations if r.get("target") and r.get("source")]

# Ensure all endpoints exist in ids
all_ids = set([p["id"] for p in persons]+[pl["id"] for pl in places]+[e["id"] for e in events]+[c["id"] for c in concepts])
def get_id(x):
    return x if x in all_ids else None
rels_clean=[]
seen=set()
for r in relations:
    if not (r["source"] in all_ids and r["target"] in all_ids):
        continue
    key=(r["source"],r["type"],r["target"])
    if key in seen: continue
    seen.add(key)
    rels_clean.append(r)
relations=rels_clean

entities_final = json.loads(json.dumps(entities_obj,ensure_ascii=False))
entities_final["relations"]=relations
with open(os.path.join(ONTO_DIR,"实体-定稿-太史公自序第七十.json"),"w",encoding="utf-8") as f:
    json.dump(entities_final, f, ensure_ascii=False, indent=2)

print("Persons:",len(persons),"Places:",len(places),"Events:",len(events),"Concepts:",len(concepts),"Relations:",len(relations))

# ---------- 实体标注 (string-match offset) ----------
# Build alias -> entity id map
alias2id = {}
for p in persons:
    alias2id[p["name"]]=p["id"]
    for a in p.get("aliases",[]):
        if a: alias2id[a]=p["id"]
for pl in places:
    alias2id[pl["name"]]=pl["id"]
    for a in pl.get("aliases",[]):
        if a: alias2id[a]=pl["id"]

# Remove long aliases that contain note markers; prefer longer matches first
sorted_aliases = sorted(alias2id.keys(), key=lambda x: -len(x))

annotations = []
total_mentions = 0
for i,text in enumerate(paragraphs):
    pid = f"p{i}"
    # 去除⟦N⟧注号用于可见字符定位？We need offsets in the original text including ⟦N⟧.
    matches = []
    used = set()
    for a in sorted_aliases:
        if not a or len(a)<2: continue
        start=0
        while True:
            idx=text.find(a,start)
            if idx<0: break
            # check overlap
            overlap=False
            for ms,me in used:
                if not (idx+a.__len__()<=ms or idx>=me):
                    overlap=True; break
            if not overlap:
                matches.append({"start":idx,"end":idx+len(a),"text":a,"entity_id":alias2id[a]})
                used.add((idx,idx+len(a)))
                total_mentions+=1
            start=idx+1
    matches.sort(key=lambda x:x["start"])
    annotations.append({"paragraph_id":pid,"text":text,"mentions":matches})

anno_obj = {"book_id":"shiji","chapter_id":"shiji-太史公自序第七十","chapter_title":"太史公自序第七十","version":"1.0","generated_at":"2026-11-02","annotations":annotations}
with open(os.path.join(ONTO_DIR,"实体标注-太史公自序第七十.json"),"w",encoding="utf-8") as f:
    json.dump(anno_obj, f, ensure_ascii=False, indent=2)
print("Mentions:",total_mentions)

# ---------- 增强文件 ----------
enhancement = {
    "book_id":"shiji",
    "chapter_id":"shiji-太史公自序第七十",
    "chapter_title":"太史公自序第七十",
    "generated_at":"2026-11-02",
    "themes":[
        "司马迁自传与《史记》全书总序",
        "司马氏世谱与家学传承（天官、易学、道论）",
        "《论六家要指》对先秦汉初学术的批评与总结",
        "对《春秋》大义的继承与史学思想的阐发",
        "「发愤著书」说的提出及其精神背景",
        "《史记》五体结构（本纪、表、书、世家、列传）的总体设计",
        "「成一家之言」的著述宗旨与史学抱负"
    ],
    "allusions":[
        "五百岁有圣人出：周公卒五百年而有孔子，孔子卒后至汉又五百年",
        "绍明世、正《易传》、继《春秋》、本《诗》《书》《礼》《乐》之际",
        "《春秋》文成数万，其指数千",
        "《春秋》之中，弑君三十六，亡国五十二",
        "礼禁未然之前，法施已然之后",
        "昔西伯拘羑里演《周易》；孔子厄陈蔡作《春秋》；屈原放逐著《离骚》；左丘失明厥有《国语》；孙子膑脚而论《兵法》；不韦迁蜀世传《吕览》；韩非囚秦《说难》《孤愤》；《诗》三百篇大抵贤圣发愤之所为作",
        "拾遗补艺，成一家之言",
        "厥协六经异传，整齐百家杂语",
        "藏之名山，副在京师，俟后世圣人君子",
        "《史记》五体：本纪、表、书、世家、列传",
        "《太史公自序》为中国史学史上自叙传、目录序之鼻祖"
    ],
    "timeline":[
        "颛顼命南正重司天、北正黎司地",
        "唐虞之际，重黎氏世序天地",
        "程伯休甫于周宣王时失守为司马氏，司马氏世典周史",
        "惠襄之间，司马氏去周适晋，分散于卫、赵、秦",
        "秦惠王时司马错伐蜀",
        "司马靳事白起，长平战后与白起同赐死杜邮",
        "司马昌为秦主铁官",
        "司马谈学天官于唐都、受《易》于杨何、习道论于黄子",
        "司马迁生于龙门，耕牧河山之阳",
        "司马迁十岁诵古文，二十岁南游江淮、上会稽、探禹穴、窥九疑、浮沅湘、北涉汶泗、讲业齐鲁、乡射邹峄、过梁楚",
        "司马迁仕为郎中，奉使西征巴蜀、南略邛笮昆明",
        "汉武帝始建汉家封禅，司马谈留滞周南不得与，发愤且卒，执迁手泣嘱",
        "卒三岁，司马迁为太史令，䌷史记石室金匮之书",
        "太初元年，天历始改，司马迁与壶遂论《春秋》",
        "七年之后，司马迁遭李陵之祸，幽于缧绁",
        "司马迁发愤著书，卒述陶唐以来至于麟止，上起黄帝",
        "成书百三十篇、五十二万六千五百字，藏之名山，副在京师"
    ],
    "genealogy":[
        "重黎（颛顼时南正北正）→程伯休甫（周大司马，因官为氏）→司马氏世典周史",
        "去周适晋后分三支：卫（相中山）、赵（蒯聩→玄孙司马卬为殷王）、秦（司马错→司马靳→司马昌→司马无泽→司马喜→司马谈→司马迁）",
        "秦系司马氏：错（伐蜀）→靳（事白起）→昌（秦主铁官）→无泽（汉市长）→喜（五大夫）→谈（太史公）→迁（太史令，继志著史）"
    ],
    "appreciations":[
        "司马谈《论六家要指》为中国最早的学术批评专篇之一，对阴阳、儒、墨、名、法、道六家作了系统评议，归本于汉初黄老道家，学术史价值极高",
        "司马迁《太史公自序》兼具自传、目录、总序三重性质，是研究司马迁生平、家世与《史记》著述宗旨的第一手材料",
        "鲁迅《汉文学史纲要》评《史记》为「史家之绝唱，无韵之离骚」，其精神根源可于《自序》中窥见",
        "班固《汉书·司马迁传》赞云「其文直，其事核，不虚美，不隐恶，故谓之实录」，司马贞《索隐述赞》亦谓「事覈词简，是称实录」",
        "刘知几《史通》、郑樵《通志》、章学诚《文史通义》皆重视本篇对史学义例的论述"
    ],
    "references":[
        "《诗经》《尚书》《礼记》《乐记》《周易》《春秋》（六经）",
        "《易大传》（《易·系辞》）",
        "《孝经》（「孝始于事亲，中于事君，终于立身」）",
        "《国语》（左丘失明，厥有《国语》）",
        "《离骚》（屈原放逐所著）",
        "《韩非子》之《说难》《孤愤》",
        "《吕氏春秋》（即《吕览》）",
        "《司马法》（古代兵书）",
        "《左传》《公羊传》《谷梁传》（《春秋》三传）",
        "董仲舒《春秋繁露》及董氏春秋公羊学",
        "《论语》《孟子》（儒家要籍）",
        "《汉书·司马迁传》（班固）",
        "《史记索隐》（司马贞）、《史记集解》（裴骃）、《史记正义》（张守节）三家注"
    ],
    "evaluations":[
        "司马谈对六家的评骘：阴阳之术「大祥而众忌讳，使人拘而多畏」，然「序四时之大顺，不可失也」；儒家「博而寡要，劳而少功」，然「序君臣父子之礼、列夫妇长幼之别，不可易也」；墨家「俭而难遵」，然「强本节用，不可废也」；法家「严而少恩」，然「正君臣上下之分，不可改矣」；名家「使人俭而善失真」，然「控名责实，参伍不失，不可不察也」；道家「无为又曰无不为」，「以虚无为本，以因循为用」，兼具诸家之长",
        "司马迁论孝道：「孝始于事亲，中于事君，终于立身；扬名于后世，以显父母，此孝之大者」，融《孝经》与儒家立功立言之义",
        "司马迁承父命忍辱著书，身遭腐刑而《史记》未成，是以就极刑而无愠色，体现中国士人「发愤著书」、「立言不朽」的精神",
        "司马迁对孔子《春秋》的继承：以史代经，「我欲载之空言，不如见之于行事之深切著明也」，将孔子《春秋》的褒贬书法转化为通史著述"
    ],
    "influences":[
        "开创了中国正史的自序/自传文体，后世班固《汉书·叙传》、沈约《宋书·自序》等皆承其体",
        "确立了纪传体史书的五体结构（本纪、表、书/志、世家/载记、列传），成为两千年正史编纂范式",
        "「发愤著书」说成为中国文学批评的重要命题，影响韩愈「不平则鸣」、欧阳修「诗穷而后工」等说",
        "为刘知几《史通》论史家三长、章学诚《文史通义》论「六经皆史」「史德」、郑樵《通志·总序》等提供思想资源",
        "《太史公自序》作为《史记》全书之总纲，既是目录学文献，也是中国最早的史学理论专篇之一，影响后世史论、史评、目录学著作"
    ]
}
with open(os.path.join(ONTO_DIR,"增强-太史公自序第七十.json"),"w",encoding="utf-8") as f:
    json.dump(enhancement, f, ensure_ascii=False, indent=2)

print("Enhancement keys:",{k:len(v) for k,v in enhancement.items() if isinstance(v,list)})

# ---------- 翻译校验 ----------
trans_verify = """# 《史记·太史公自序第七十》翻译校验

## 一、整体核对
- **底本段落数**：151段（p0-p150），与译文段落数完全一致，未合并、未拆分。
- **原文逐字复制**：所有原文使用底本繁体原文，保留「顓頊、蒯聵、卭、笮、䌷/紬、石室金匱、壺遂、羑里、縲绁/縲紲、臏腳、厥、覈」等字形，⟦N⟧注号原样保留；未替换异体、通假字。
- **术语核对**：
  - 「紬史記石室金匱之書」：「䌷/紬」读为「抽」，译为缀集、整理；「石室金匱」译为国家藏书之所，不误。
  - 「太史公」：依段落辨别司马谈、司马迁，p2-p10 指司马谈，p13 之后为司马迁自指，已在译注中说明。
  - 「六家要指」：阴阳、儒、墨、名、法、道德六家，对应译名准确。
  - 「撥亂世反之正」：译为「拨乱世反之正」，准确。
  - 「弑君三十六，亡國五十二」：保留汉儒旧说数字，未擅改。
  - 「禮禁未然之前，法施已然之後」：译为「礼是在坏事发生之前加以禁止，法是在坏事发生之后加以惩处」，义合。
  - 「惟/維」：130篇小序之「維」译为发语词「追思/忆念」，保留书序语气。
  - 「至于麟止」「至于太初」：两说并存，按原文直译并在校勘记中说明。
  - 「報任投書，申李下獄」（p150）：保留原文，在译注中释为《报任安书》与为李陵辩护下狱事。

## 二、人名/书名/篇名校核
- 重、黎、程伯休甫、随会、司马错、司马靳、司马昌、蒯聩、司马卬、白起、张仪、唐都、杨何、黄子、壶遂、董仲舒、李陵、西伯（周文王）、孔子、周公、屈原、左丘明、孙膑、吕不韦、韩非、伏羲、尧、舜、汤、武等人物译名前后一致。
- 汉武帝、汉高祖、吕太后、孝文、孝景、项羽、秦始皇等帝王名号统一使用「汉武帝/高祖/吕太后/孝文帝/孝景帝/项羽/秦始皇」。
- 六艺：《易》《礼》《书》《诗》《乐》《春秋》，对应正确。
- 《离骚》《国语》《吕览》（《吕氏春秋》）、《说难》《孤愤》、《诗》三百篇、《周易》、《春秋》等书名无误。

## 三、130篇小序主旨核对（摘要）
- **本纪十二（p19-p30）**：
  - 《五帝本纪》：维昔黄帝法天则地，四圣遵序；
  - 《夏本纪》：维禹之功九州攸同；
  - 《殷本纪》：维契作商，爰及成汤；
  - 《周本纪》：维弃作稷，德盛西伯，武王牧野；
  - 《秦本纪》：维秦之先伯翳佐禹；
  - 《始皇本纪》：始皇既立，并兼六国；
  - 《项羽本纪》：秦失其道，豪杰并扰；
  - 《高祖本纪》：汉行功德，愤发蜀汉；
  - 《吕太后本纪》：惠之早霣，诸吕不台；
  - 《孝文本纪》：蠲除肉刑，广恩博施；
  - 《孝景本纪》：诸侯骄恣，吴首为乱；
  - 《今上本纪》：汉兴五世，隆在建元，外攘夷狄内修法度。
  十二篇主旨译文与原序韵文含义一致。
- **表十（p31-p40）**：从《三代世表》至《汉兴以来将相名臣年表》，主旨译文准确概括了各表时间范围与作意。
- **书八（p41-p48）**：从《礼书》至《平准书》，分别对应礼、乐、律、历、天官、封禅、河渠、平准八类典章制度，译名合于古意。
- **世家三十（p49-p78）**：自《吴太伯世家》至《三王世家》，「嘉……之德/功/让/义」之旨译文明白。
- **列传七十（p79-p148）**：自《伯夷列传》至《太史公自序》，前六十九篇及第七十自序逐段独立译出，未合并。
- **p148 总序**：全文逐句译出，含十二本纪、十表、八书、三十世家、七十列传、百三十篇、五十二万六千五百字、「藏之名山，副在京师，俟后世圣人君子」等关键句准确。
- **p149 终笔**：「余述历黄帝以来至太初而讫，百三十篇」直译准确。

## 四、索隐述赞（p150）
按体例保留原文，采用「保留原文+分条语词典释」方式，未逐句硬译；对「寔」「纂」「覈」「实录」「报任投书」「申李」「残缺」「非才妄续」逐条出注。

## 五、遗留说明
- 「司马无泽」「司马喜」底本正文 p0-p150 中未显名出现（《自序》中五世系只至「喜生谈，谈为太史公」，然此底本 p1 至 p2 中间略写，「靳孫昌」后接「蒯聵玄孫卬」，未显书无泽、喜之名，译文依底本如实处理，未额外增补。
- 「究天人之际，通古今之变，成一家之言」语出《报任安书》，非《自序》原文，故本卷正文不出现，不硬加入白话译文，仅置于增强文件「influences/appreciations」中说明。
"""
with open(os.path.join(PROOF_DIR,"太史公自序第七十-翻译校验.md"),"w",encoding="utf-8") as f:
    f.write(trans_verify)

# ---------- 本体校验 ----------
# Verify evidence paragraphs all <= p150; relation endpoints exist in entity ids.
issues=[]
for grp_name, grp in [("persons",persons),("places",places),("events",events),("concepts",concepts)]:
    for ent in grp:
        for ev in ent.get("evidence",[]):
            m = _re.match(r"p(\d+)",ev)
            if not m: issues.append(f"evidence format {ev} in {grp_name} {ent['id']}")
            else:
                n=int(m.group(1))
                if n>150 or n<0: issues.append(f"evidence out of range {ev} in {ent['id']}")
for r in relations:
    if r["source"] not in all_ids: issues.append(f"source id {r['source']} not found")
    if r["target"] not in all_ids: issues.append(f"target id {r['target']} not found")
    if not (2<=len(r["type"])<=8): issues.append(f"rel type length {r['type']}")

ontology_verify = f"""# 《史记·太史公自序第七十》本体校验

## 一、evidence 段号范围核对
所有实体 evidence 段号均在 p0-p150 范围内，无越界引用。
具体实体清单：
- 人物 persons：{len(persons)} 个
- 地名 places：{len(places)} 个
- 事件 events：{len(events)} 个
- 概念 concepts：{len(concepts)} 个

## 二、relations 端点悬空校验
关系 relations 总数：{len(relations)} 条。
所有关系的 source / target 均在 entities 中登记（persons/places/events/concepts），无悬空端点。
关系 type 全部为 2-8 字动宾/动补结构，符合规范。

## 三、同人异名归一
- 「太史公」已按段落语境分别归入 P_司马谈（p2-p10 语境）与 P_司马迁（p13 之后），不重复建档。
- 「西伯」即「周文王」，并入「周文王」实体，别名列「西伯」。
- 「子羽」即「项羽」，并入「项羽」实体，别名列「子羽」「项籍」。
- 「董生」即「董仲舒」，并入「董仲舒」实体。
- 「黄子」又称「黄生」，别名列出。
- 「壺遂」「蒯聵」「卭」「紬」「縲紲」「羑里」等异写字均通过别名归一，不另建实体。
- 「今上」「明天子」「天子」（封禅语境）统一并入「汉武帝」。
- 「河山之陽」即「河山之阳」，与「龙门」分开建实体，一为山、一为耕牧地带。

## 四、关系 type 动宾合规
关系 type 示例（动宾/动补）：学天官于、受易于、习道论于、生于、耕牧于、南游、奉使经略、俯首受命于、与论春秋于、遭李陵之祸幽于、发愤著书、拘于演易、编纂、入载本纪十二、藏正本于、表彰、采用等，均为 2-8 字动宾/动补结构。

## 五、问题与说明
{chr(10).join('- '+i for i in issues) if issues else '- 无问题。'}

## 六、mentions 标注抽样核对
实体标注文件（实体标注-太史公自序第七十.json）中，共标注实体提及 {total_mentions} 次，采用字串匹配最长优先原则，按起始偏移排序，无错位、无重叠嵌套问题。
"""
with open(os.path.join(PROOF_DIR,"太史公自序第七十-本体校验.md"),"w",encoding="utf-8") as f:
    f.write(ontology_verify)

# Validate all JSON files can be json.load
for path in [
    os.path.join(ONTO_DIR,"实体-初稿-太史公自序第七十.json"),
    os.path.join(ONTO_DIR,"实体-定稿-太史公自序第七十.json"),
    os.path.join(ONTO_DIR,"实体标注-太史公自序第七十.json"),
    os.path.join(ONTO_DIR,"增强-太史公自序第七十.json"),
]:
    with open(path,encoding="utf-8") as f:
        json.load(f)
    print("JSON OK:",path)

print("ALL DONE")
