#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime

# 读取底本
with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/text/shiji-淮南衡山列傳第五十八.json', 'r', encoding='utf-8') as f:
    text_data = json.load(f)

paragraphs = []
for p in text_data['paragraphs']:
    pid = p['id'].split(':')[-1]
    paragraphs.append({
        'id': pid,
        'text': p['text']
    })

# 初始化实体
persons = []
places = []
events = []
concepts = []

def add_person(name, alias, note, evidence_pid):
    # 检查是否已存在
    for p in persons:
        if p['name'] == name:
            if evidence_pid not in p['evidence']:
                p['evidence'].append(evidence_pid)
            return
    persons.append({
        'name': name,
        'alias': alias,
        'note': note,
        'evidence': [evidence_pid]
    })

def add_place(name, alias, note, evidence_pid):
    for pl in places:
        if pl['name'] == name:
            if evidence_pid not in pl['evidence']:
                pl['evidence'].append(evidence_pid)
            return
    places.append({
        'name': name,
        'alias': alias,
        'note': note,
        'evidence': [evidence_pid]
    })

def add_event(name, note, evidence_pid):
    for e in events:
        if e['name'] == name:
            if evidence_pid not in e['evidence']:
                e['evidence'].append(evidence_pid)
            return
    events.append({
        'name': name,
        'note': note,
        'evidence': [evidence_pid]
    })

def add_concept(name, note, evidence_pid):
    for c in concepts:
        if c['name'] == name:
            if evidence_pid not in c['evidence']:
                c['evidence'].append(evidence_pid)
            return
    concepts.append({
        'name': name,
        'note': note,
        'evidence': [evidence_pid]
    })

# 逐段提取实体
for p in paragraphs:
    pid = p['id']
    t = p['text']
    
    # ---- 人物提取 ----
    # 核心人物
    if '淮南厲王長' in t or '厲王' in t or '長' in t and ('淮南' in t or '王' in t):
        add_person('刘长（淮南厉王）', ['淮南厲王長', '淮南王長', '厲王', '長', '淮南王'], '刘邦第七子，封淮南王，谥厉，骄横谋反，绝食而死', pid)
    if '高祖' in t or '高皇帝' in t or '上' in t and ('高祖' in t or '八年' in t):
        add_person('刘邦（汉高祖）', ['高祖', '高皇帝', '上'], '西汉开国皇帝，汉高祖', pid)
    if '張敖' in t or '趙王敖' in t or '趙王' in t:
        add_person('张敖', ['趙王張敖', '趙王敖', '趙王'], '张耳之子，刘邦女婿，袭封赵王', pid)
    if '趙兼' in t:
        add_person('赵兼', ['趙兼'], '刘长舅父', pid)
    if '辟陽侯' in t or '審食其' in t:
        add_person('审食其（辟阳侯）', ['辟陽侯', '審食其'], '吕后宠臣，封辟阳侯，被刘长锤杀', pid)
    if '呂后' in t:
        add_person('吕雉（吕后）', ['呂后'], '刘邦皇后，汉惠帝时临朝称制', pid)
    if '黥布' in t:
        add_person('英布（黥布）', ['淮南王黥布', '黥布'], '汉初名将，封淮南王，后谋反被击杀', pid)
    if '魏敬' in t:
        add_person('魏敬', ['魏敬'], '刘长随从，击杀审食其', pid)
    if '孝文帝' in t or '上' in t and ('孝文' in t or '文帝' in t):
        add_person('刘恒（汉文帝）', ['孝文帝', '上', '文帝'], '刘邦第四子，初封代王，汉文帝，开创文景之治', pid)
    if '薄太后' in t:
        add_person('薄姬（薄太后）', ['薄太后'], '汉文帝生母', pid)
    if '太子' in t and ('孝景' in t or '啟' not in t and pid < 'p10'):
        add_person('刘启（汉景帝）', ['太子'], '汉文帝太子，后为汉景帝', pid)
    if '但' in t and ('男子但' in t or '大夫但' in t):
        add_person('但（大夫）', ['男子但', '大夫但'], '刘长部下，参与谋反', pid)
    if '柴武' in t or '棘蒲侯' in t or '奇' in t and '太子奇' in t:
        add_person('柴武（棘蒲侯）', ['棘蒲侯柴武', '棘蒲侯'], '汉初大将，封棘蒲侯', pid)
        add_person('柴奇', ['太子奇', '奇'], '柴武太子，参与刘长谋反', pid)
    if '張倉' in t or '丞相臣' in t and '倉' in t:
        add_person('张苍', ['丞相臣張倉', '臣倉'], '汉初丞相，封北平侯', pid)
    if '馮敬' in t:
        add_person('冯敬', ['典客臣馮敬', '臣敬'], '当时任典客', pid)
    if '逸' in t and '宗正臣逸' in t:
        add_person('刘逸（宗正）', ['宗正臣逸', '臣逸'], '当时任宗正，代理御史大夫事', pid)
    if '賀' in t and '廷尉臣賀' in t:
        add_person('贺（廷尉）', ['廷尉臣賀', '臣賀'], '当时任廷尉', pid)
    if '福' in t and '中尉臣福' in t:
        add_person('福（中尉）', ['備盜賊中尉臣福', '臣福'], '当时任中尉，掌京城治安', pid)
    if '春' in t and ('郎中春' in t or '丞相春' in t):
        add_person('春（淮南相）', ['郎中春', '春'], '淮南国郎中，被刘长任为相', pid)
    if '開章' in t:
        add_person('开章（士五）', ['士五開章', '開章'], '刘长谋反同谋，被刘长杀害灭口', pid)
    if '蕳忌' in t or '忌' in t and ('中尉蕳忌' in t or '故中尉' in t):
        add_person('蕳忌', ['故中尉蕳忌', '忌'], '淮南国原中尉，刘长亲信，参与杀开章', pid)
    if '王織' in t:
        add_person('王织', ['南海民王織'], '南海人，上书献璧给皇帝', pid)
    if '奇' in t and '長安尉奇' in t:
        add_person('奇（长安尉）', ['長安尉奇'], '长安县尉，负责逮捕开章', pid)
    if '嬰' in t and '臣嬰' in t:
        add_person('夏侯婴（汝阴侯）', ['臣嬰'], '汉初大臣，汝阴侯，太仆', pid)
    if '袁盎' in t:
        add_person('袁盎', ['袁盎'], '字丝，汉初大臣，以直谏著称', pid)
    if '安' in t and ('淮南王安' in t or '王安' in t or '王' in t and pid >= 'p10'):
        add_person('刘安（淮南王）', ['淮南王安', '淮南王', '安', '王安'], '刘长长子，后袭封淮南王，组织编《淮南子》，因谋反自杀', pid)
    if '勃' in t and ('安陽侯勃' in t or '子勃' in t or '衡山王' in t):
        add_person('刘勃（衡山王/济北贞王）', ['安陽侯勃', '子勃', '衡山王'], '刘长次子，先后封安阳侯、衡山王、济北王，谥贞', pid)
    if '賜' in t and ('周陽侯賜' in t or '子賜' in t or '廬江王' in t or '衡山王賜' in t):
        add_person('刘赐（衡山王）', ['周陽侯賜', '子賜', '廬江王', '衡山王賜'], '刘长第三子，先后封周阳侯、庐江王、衡山王，因谋反自杀', pid)
    if '良' in t and ('東城侯良' in t or '子良' in t):
        add_person('刘良（东城侯）', ['東城侯良', '子良'], '刘长第四子，封东城侯，早死无后', pid)
    if '城陽王' in t or '喜' in t and '城陽王喜' in t:
        add_person('刘喜（城阳王）', ['城陽王喜', '城陽王'], '齐悼惠王刘肥之孙，曾徙封淮南王，后复还城阳', pid)
    if '曲城侯' in t:
        add_person('蛊捷（曲城侯）', ['曲城侯'], '汉初功臣，曲城侯，率兵救淮南', pid)
    if '武安侯' in t:
        add_person('田蚡（武安侯）', ['武安侯'], '汉武帝舅舅，封武安侯，官至太尉、丞相', pid)
    if '劉陵' in t or '女陵' in t or '陵' in t and ('王女陵' in t or '女陵' in t):
        add_person('刘陵', ['女陵', '陵'], '刘安之女，聪慧善辩，在长安为父刺探情报', pid)
    if '荼' in t and ('王后荼' in t or '王后' in t):
        add_person('荼（淮南王后）', ['王后荼', '王后'], '淮南王刘安王后', pid)
    if '遷' in t and ('太子遷' in t or '太子' in t and pid >= 'p15'):
        add_person('刘迁（淮南太子）', ['太子遷', '太子'], '刘安太子，谋反失败自杀', pid)
    if '王皇太后' in t or '脩成君' in t:
        add_person('王娡（王太后）', ['王皇太后'], '汉武帝生母', pid)
        add_person('金俗（修成君）', ['脩成君'], '王太后与前夫金王孙之女，汉武帝同母异父姊', pid)
    if '靁被' in t or '雷被' in t:
        add_person('雷被（郎中）', ['郎中靁被', '靁被'], '淮南国郎中，善击剑，被刘迁迫害逃奔长安', pid)
    if '宏' in t and ('漢中尉宏' in t or '中尉宏' in t):
        add_person('殷宏（汉中尉）', ['漢中尉宏', '中尉宏'], '汉朝中尉，奉命到淮南查案', pid)
    if '伍被' in t:
        add_person('伍被', ['伍被'], '淮南国中郎，刘安主要谋士，先劝谏后参与谋反，事发被杀', pid)
    if '左吴' in t:
        add_person('左吴', ['左吴'], '淮南王刘安亲信，参与谋反', pid)
    if '膠東王' in t:
        add_person('刘寄（胶东王）', ['膠東王'], '汉景帝子，汉武帝异母弟', pid)
    if '常山王' in t:
        add_person('刘舜（常山王）', ['常山王'], '汉景帝子，汉武帝异母弟', pid)
    if '子胥' in t or '伍子胥' in t:
        add_person('伍子胥', ['子胥'], '春秋吴国大夫，谏吴王夫差被杀', pid)
    if '吳王' in t and ('夫差' in t or '姑蘇' in t):
        add_person('夫差（吴王）', ['吳王'], '春秋吴国末代君主，不听伍子胥劝谏被越国灭', pid)
    if '文王' in t:
        add_person('周文王（姬昌）', ['文王'], '周朝奠基者', pid)
    if '蒙恬' in t:
        add_person('蒙恬', ['蒙恬'], '秦朝大将，北筑长城御匈奴', pid)
    if '徐福' in t:
        add_person('徐福', ['徐福'], '秦朝方士，入海求仙药，留居海外称王', pid)
    if '尉佗' in t or '趙佗' in t:
        add_person('赵佗（南越王）', ['尉佗'], '秦朝南海尉，后建立南越国称王', pid)
    if '陳勝' in t:
        add_person('陈胜', ['陳勝'], '秦末农民起义领袖', pid)
    if '吳廣' in t:
        add_person('吴广', ['吳廣'], '秦末农民起义领袖', pid)
    if '高皇帝' in t and '高皇始於豐沛' in t:
        add_person('刘邦（汉高祖）', ['高皇帝', '高皇'], '西汉开国皇帝', pid) # 重复但归一条
    if '吳王' in t and ('劉濞' in t or '吳楚' in t or '丹徒' in t):
        add_person('刘濞（吴王）', ['吳王'], '汉高祖侄，封吴王，吴楚七国之乱主谋', pid)
    if '竇氏' in t:
        add_person('窦婴（魏其侯）', ['竇氏'], '窦太后侄，魏其侯，汉景帝时平定七国之乱', pid)
    if '微子' in t:
        add_person('微子（宋微子）', ['微子'], '商纣王庶兄，宋国始祖，过殷墟作麦秀之歌', pid)
    if '紂' in t or '王子比干' in t:
        add_person('帝辛（商纣王）', ['紂', '紂王'], '商朝末代君主', pid)
        add_person('比干', ['王子比干'], '商纣王叔父，强谏被剖心', pid)
    if '孟子' in t:
        add_person('孟子（孟轲）', ['孟子'], '战国儒家代表人物', pid)
    if '不害' in t and ('孽子不害' in t or '不害' in t and pid >= 'p19'):
        add_person('刘不害', ['孽子不害', '不害'], '刘安庶长子，不受宠，未封侯', pid)
    if '建' in t and ('建' in t and ('王孫建' in t or '子建' in t or pid >= 'p19')):
        add_person('刘建', ['王孫建', '建'], '刘不害之子，告发淮南太子谋反', pid)
    if '莊芷' in t:
        add_person('庄芷', ['壽春莊芷'], '寿春人，代刘建上书朝廷', pid)
    if '審卿' in t:
        add_person('审卿', ['審卿'], '审食其之孙，与公孙弘交好，追查淮南谋反案', pid)
    if '公孫弘' in t:
        add_person('公孙弘（平津侯）', ['公孫弘', '丞相弘'], '汉武帝时丞相，封平津侯', pid)
    if '大將軍' in t or '青' in t and ('大將軍青' in t):
        add_person('卫青（大将军）', ['大將軍', '大將軍青', '青'], '汉武帝时大将军，多次出击匈奴，汉代名将', pid)
    if '黃義' in t:
        add_person('黄义', ['黃義'], '曾跟随卫青击匈奴，向伍被称赞卫青', pid)
    if '曹梁' in t:
        add_person('曹梁（谒者）', ['謁者曹梁', '曹梁'], '汉朝谒者，出使长安归来称赞卫青', pid)
    if '樓緩' in t:
        add_person('楼缓', ['樓緩'], '淮南王部下，奉命守成皋', pid)
    if '周被' in t:
        add_person('周被', ['周被'], '淮南王部下，奉命下颍川塞轘辕伊阙', pid)
    if '陳定' in t:
        add_person('陈定', ['陳定'], '淮南王部下，奉命发南阳兵守武关', pid)
    if '趙賢' in t:
        add_person('赵贤', ['趙賢'], '淮南王亲信，参与谋反', pid)
    if '朱驕如' in t:
        add_person('朱骄如', ['朱驕如'], '淮南王亲信，参与谋反', pid)
    if '章邯' in t:
        add_person('章邯', ['章邯'], '秦朝大将，镇压秦末农民起义', pid)
    if '楊熊' in t:
        add_person('杨熊', ['楊熊'], '秦朝大将', pid)
    if '趙王彭祖' in t or '彭祖' in t and '趙王' in t:
        add_person('刘彭祖（赵王）', ['趙王彭祖'], '汉景帝子，封赵王', pid)
    if '讓' in t and '列侯臣讓' in t:
        add_person('曹让（列侯）', ['列侯臣讓', '讓'], '列侯，参与议淮南王罪', pid)
    if '端' in t and '膠西王臣端' in t:
        add_person('刘端（胶西王）', ['膠西王臣端', '端', '膠西王'], '汉景帝子，封胶西王，参与议淮南王罪', pid)
    if '湯' in t and '廷尉湯' in t:
        add_person('张汤', ['廷尉湯', '湯'], '汉武帝时廷尉、御史大夫，著名酷吏', pid)
    if '宗正' in t and '使宗正' in t and pid == 'p23':
        add_person('（宗正）', ['宗正'], '汉朝派去惩办淮南王的宗正（姓名未载）', pid)
    if '乘舒' in t:
        add_person('乘舒（衡山王后）', ['王后乘舒'], '衡山王刘赐王后，生刘爽、刘孝、刘无采', pid)
    if '爽' in t and ('太子爽' in t or '長男爽' in t):
        add_person('刘爽（衡山太子）', ['太子爽', '長男爽', '爽'], '刘赐长子，立为太子，被废后弃市', pid)
    if '孝' in t and ('次男孝' in t or '孝' in t and pid >= 'p24'):
        add_person('刘孝', ['次男孝', '孝'], '刘赐次子，与父谋反，后自首仍因通奸弃市', pid)
    if '無采' in t:
        add_person('刘无采', ['次女無采', '無采'], '刘赐之女，出嫁后被休，与奴、客通奸', pid)
    if '徐來' in t:
        add_person('徐来（衡山王后）', ['姬徐來', '王后徐來', '徐來'], '刘赐姬妾，乘舒死后立为王后，因巫蛊杀前王后被弃市', pid)
    if '厥姬' in t:
        add_person('厥姬（美人）', ['美人厥姬', '厥姬'], '刘赐美人，生子二人', pid)
    if '奚慈' in t:
        add_person('奚慈', ['奚慈'], '衡山王部下，参与谋反谋划', pid)
    if '張廣昌' in t:
        add_person('张广昌', ['張廣昌'], '衡山王部下，参与谋反谋划', pid)
    if '衞慶' in t:
        add_person('卫庆（谒者）', ['謁者衞慶', '衞慶'], '衡山国谒者，懂方术，想上书事天子被刘赐迫害', pid)
    if '廣' in t and '其子廣' in t:
        add_person('刘广', ['廣', '其子廣'], '徐来之子，徐来想立他为太子', pid)
    if '救赫' in t:
        add_person('救赫', ['救赫'], '刘孝宾客，江都人，为衡山王制造战车箭矢', pid)
    if '陳喜' in t:
        add_person('陈喜', ['陳喜'], '刘孝宾客，参与谋反，被刘孝藏匿后事发', pid)
    if '周丘' in t:
        add_person('周丘', ['周丘'], '吴王刘濞部下壮士，下邳城奇功', pid)
    if '白嬴' in t:
        add_person('白嬴', ['白嬴'], '刘爽亲信，被派到长安上书，被捕', pid)
    if '中尉安' in t or '安' in t and '中尉安' in t:
        add_person('司马安（中尉）', ['中尉安', '安'], '汉朝中尉，奉命审问衡山王', pid)
    if '大行息' in t or '息' in t and '大行息' in t:
        add_person('李息（大行令）', ['大行息', '息'], '汉朝大行令，奉命审问衡山王', pid)
    if '趙王如意' in t or '如意' in t and '趙王如意子母' in t:
        add_person('刘如意（赵王）', ['趙王如意', '如意'], '刘邦与戚夫人之子，封赵王，被吕后毒死', pid)
    if '戚夫人' in t or '如意子母' in t:
        add_person('戚夫人', ['趙王如意子母'], '刘邦宠妃，赵王如意生母，被吕后残害', pid)
    if '周公' in t and '周公殺管蔡' in t:
        add_person('周公旦', ['周公'], '周武王弟，摄政，杀管叔放蔡叔，成周大业', pid)
    if '管蔡' in t:
        add_person('管叔鲜', ['管叔'], '周公弟，叛乱被诛', pid)
        add_person('蔡叔度', ['蔡叔'], '周公弟，叛乱被流放', pid)
    if '堯舜' in t:
        add_person('尧（唐尧）', ['堯'], '上古圣王', pid)
        add_person('舜（虞舜）', ['舜'], '上古圣王', pid)
    if '三王' in t and '功高三王' in t:
        add_person('夏禹', ['三王'], '夏朝开国君主', pid)
        add_person('商汤', ['三王'], '商朝开国君主', pid)
        add_person('周文王/周武王', ['三王'], '周朝开国君主', pid)
    
    # ---- 地名提取 ----
    if '東垣' in t:
        add_place('东垣', ['東垣'], '县名，在今河北石家庄东', pid)
    if '趙' in t and ('過趙' in t or '趙王' in t):
        add_place('赵国', ['趙'], '汉初诸侯国，张敖封地，都邯郸', pid)
    if '栢人' in t or '柏人' in t:
        add_place('柏人', ['栢人'], '县名，在今河北隆尧西，贯高谋刺刘邦处', pid)
    if '河內' in t:
        add_place('河内郡', ['河內'], '郡名，治所在怀县（今河南武陟西南）', pid)
    if '真定' in t:
        add_place('真定', ['真定'], '县名，在今河北正定，刘长外祖母家', pid)
    if '淮南' in t and ('淮南王' in t or '淮南國' in t):
        add_place('淮南国', ['淮南'], '汉初诸侯国，原黥布封地，刘长、刘安先后为王，都寿春', pid)
    if '長安' in t:
        add_place('长安', ['長安'], '西汉都城，在今陕西西安西北', pid)
    if '谷口' in t:
        add_place('谷口', ['谷口'], '县名，在今陕西礼泉东北，刘长谋反起事地', pid)
    if '閩越' in t:
        add_place('闽越', ['閩越'], '古代越族一支，在今福建一带', pid)
    if '匈奴' in t:
        add_place('匈奴', ['匈奴'], '北方游牧民族，汉代主要边患', pid)
    if '肥陵邑' in t:
        add_place('肥陵邑', ['肥陵邑'], '淮南国属县，在今安徽寿县西北，开章葬地', pid)
    if '蜀郡嚴道' in t or '嚴道' in t or '卭郵' in t:
        add_place('严道邛邮', ['蜀郡嚴道卭郵', '嚴道', '卭郵'], '蜀郡严道县邛邮，在今四川荥经，刘长流放地', pid)
    if '雍' in t and '至雍' in t:
        add_place('雍县', ['雍'], '县名，在今陕西凤翔南，刘长死于此', pid)
    if '城陽' in t and '城陽王' in t:
        add_place('城阳国', ['城陽'], '汉初诸侯国，刘喜封地，都莒县（今山东莒县）', pid)
    if '吳' in t and ('吳楚' in t or '吳王' in t):
        add_place('吴国', ['吳'], '汉初诸侯国，刘濞封地，领东阳、鄣、吴、会稽四郡', pid)
    if '楚' in t and '吳楚' in t:
        add_place('楚国', ['楚'], '汉初诸侯国，吴楚七国之乱参与者', pid)
    if '曲城' in t:
        add_place('曲城', ['曲城'], '地名，蛊捷封地，在今山东掖县东北', pid)
    if '廬江' in t:
        add_place('庐江国/郡', ['廬江'], '汉初诸侯国/郡，刘赐封地，在今安徽西南', pid)
    if '衡山' in t and ('衡山王' in t or '衡山國' in t):
        add_place('衡山国/郡', ['衡山'], '汉初诸侯国/郡，刘勃、刘赐封地，在今安徽六安、湖北黄冈一带', pid)
    if '濟北' in t and '濟北王' in t:
        add_place('济北国', ['濟北'], '诸侯国，刘勃徙封于此，在今山东长清南', pid)
    if '越' in t and ('越' in t or '使越' in t):
        add_place('越国（东越/南越）', ['越'], '南方越族政权，包括东越、南越', pid)
    if '霸上' in t:
        add_place('霸上', ['霸上'], '地名，在今陕西西安东，长安东面要道，田蚡迎刘安处', pid)
    if '南陽' in t:
        add_place('南阳郡', ['南陽'], '郡名，治所在宛县（今河南南阳）', pid)
    if '武關' in t:
        add_place('武关', ['武關'], '关名，在今陕西丹凤东南，关中通往南阳要道', pid)
    if '壽春' in t:
        add_place('寿春', ['壽春'], '淮南国都，在今安徽寿县', pid)
    if '河南' in t and ('河南治' in t or '河南郡' in t):
        add_place('河南郡/雒阳', ['河南', '雒陽'], '郡名，治所在雒阳（今河南洛阳）', pid)
    if '頴川' in t:
        add_place('颍川郡', ['頴川'], '郡名，治所在阳翟（今河南禹州）', pid)
    if '轘轅' in t:
        add_place('轘辕关', ['轘轅'], '关名，在今河南偃师东南，山路险要', pid)
    if '伊闕' in t:
        add_place('伊阙关', ['伊闕'], '关名，在今河南洛阳南，洛阳南面险要', pid)
    if '成皐' in t:
        add_place('成皋关（虎牢关）', ['成皐'], '关名，在今河南荥阳汜水镇，洛阳东面险要关隘', pid)
    if '臨晉關' in t:
        add_place('临晋关', ['臨晉關'], '关名，在今陕西大荔东，关中通往河东要道', pid)
    if '河東' in t:
        add_place('河东郡', ['河東'], '郡名，治所在安邑（今山西夏县西北）', pid)
    if '上黨' in t:
        add_place('上党郡', ['上黨'], '郡名，治所在长子（今山西长子西）', pid)
    if '三川' in t:
        add_place('三川', ['三川'], '秦郡名，汉为河南郡，因黄河、洛水、伊水得名，成皋所在地区', pid)
    if '朔方' in t:
        add_place('朔方郡', ['朔方'], '郡名，汉武帝时新设，在今内蒙古河套地区', pid)
    if '上林' in t:
        add_place('上林苑', ['上林'], '皇帝的苑囿，在长安郊外', pid)
    if '江都' in t:
        add_place('江都国', ['江都'], '诸侯国，在今江苏扬州一带', pid)
    if '會稽' in t:
        add_place('会稽郡', ['會稽'], '郡名，在今江苏南部、浙江一带', pid)
    if '尋陽' in t:
        add_place('寻阳', ['尋陽'], '县名，在今湖北黄梅西南，长江边', pid)
    if '下雉' in t:
        add_place('下雉', ['下雉'], '县名，在今湖北阳新东南', pid)
    if '九江' in t:
        add_place('九江', ['九江'], '指今安徽江西一带长江北岸地区', pid)
    if '豫章' in t:
        add_place('豫章郡', ['豫章'], '郡名，在今江西，湖口在其北境', pid)
    if '南郡' in t:
        add_place('南郡', ['南郡'], '郡名，治所在江陵（今湖北荆州）', pid)
    if '沛郡' in t:
        add_place('沛郡', ['沛郡'], '郡名，在今安徽淮北西北，审理衡山王案地', pid)
    if '阿房之宮' in t or '阿房' in t:
        add_place('阿房宫', ['阿房之宮'], '秦朝宫殿，在渭水南，规模宏大，未完工即被焚毁', pid)
    if '長城' in t:
        add_place('万里长城', ['長城'], '蒙恬主持修筑的秦长城', pid)
    if '蓬萊山' in t:
        add_place('蓬莱山', ['蓬萊山'], '传说中海上三神山之一', pid)
    if '五嶺' in t:
        add_place('五岭', ['五嶺'], '即南岭，长江流域与珠江流域分水岭，越城、都庞、萌渚、骑田、大庾五岭', pid)
    if '百越' in t:
        add_place('百越', ['百越'], '岭南地区越族总称', pid)
    if '豐沛' in t:
        add_place('丰沛', ['豐沛'], '今江苏丰县、沛县，刘邦故乡，起义地', pid)
    if '大澤' in t:
        add_place('大泽乡', ['大澤'], '在今安徽宿县东南，陈胜吴广起义地', pid)
    if '戲' in t and '西至於戲' in t:
        add_place('戏水', ['戲'], '水名，在今陕西临潼东，陈胜起义军西至此处', pid)
    if '大梁' in t:
        add_place('大梁', ['大梁'], '今河南开封，吴楚军被击破处', pid)
    if '狐父' in t:
        add_place('狐父', ['狐父'], '地名，在今安徽砀山，吴楚军战败处', pid)
    if '丹徒' in t:
        add_place('丹徒', ['丹徒'], '今江苏镇江东南，刘濞被俘处死地', pid)
    if '姑蘇之臺' in t:
        add_place('姑苏台', ['姑蘇之臺'], '吴王夫差建造的台观，在今江苏苏州', pid)
    if '江' in t and ('長江' in t or '江' in t):
        add_place('长江', ['江'], '中国第一大河，淮南、江南地区分界线', pid)
    if '淮' in t and ('江淮' in t):
        add_place('淮河', ['淮'], '中国大河，江淮地区即江淮之间', pid)
    
    # ---- 事件提取 ----
    if p['id'] == 'p0':
        add_event('刘长身世', '刘长是刘邦少子，母为赵王张敖美人，因贯高事被牵连下狱自杀，刘长由吕后收养', pid)
    if '椎辟陽侯' in t or '剄之' in t:
        add_event('刘长锤杀审食其', '刘长为报母仇，袖铁椎锤击辟阳侯审食其，命魏敬斩首，向文帝谢罪获赦', pid)
    if '谷口' in t and '反' in t:
        add_event('刘长谷口谋反', '刘长令但等七十人与柴奇谋划，以四十辆货车在谷口谋反，联络闽越、匈奴，事觉被召至长安', pid)
    if '盡誅所與謀者' in t and '不食死' in t:
        add_event('刘长绝食而死', '刘长被废王位流放蜀郡，沿途各县不敢开封门，刘长绝食死于雍县，文帝斩相关官员，以列侯礼葬', pid)
    if '一尺布' in t:
        add_event('民间作尺布斗粟谣', '民间作歌谣讽刺文帝与淮南王兄弟不相容，文帝闻而叹，徙城阳王王淮南故地，追谥刘长为厉王', pid)
    if '立其三子' in t and '參分之' in t:
        add_event('文帝三分淮南封刘长三子', '文帝怜刘长失国早死，立刘安为淮南王、刘勃为衡山王、刘赐为庐江王，三分淮南故地', pid)
    if '吳楚七國反' in t:
        add_event('七国之乱淮南完国', '吴楚七国反，刘安欲发兵应吴，淮南相率兵守城为汉，汉兵救淮南，淮南得以保全，衡山王坚守无贰心', pid)
    if '武安侯' in t and '逆王霸上' in t:
        add_event('田蚡霸上迎刘安语立嗣', '武安侯田蚡为太尉时在霸上迎刘安，说武帝无太子、刘安当立，刘安大喜，厚赠财物，加紧谋反', pid)
    if '彗星見' in t:
        add_event('彗星现刘安加紧谋反', '建元六年彗星现，有人劝刘安说彗星长竟天天下兵当大起，刘安愈治攻战具、贿赂诸侯，谋反滋甚', pid)
    if '太子學用劔' in t and '誤中太子' in t:
        add_event('雷被击剑误中太子', '太子刘迁学剑，与雷被比剑误中，雷被恐惧愿奋击匈奴，被刘迁诋毁免官，逃长安上书自明', pid)
    if '公卿請削五縣' in t and '詔削二縣' in t:
        add_event('淮南削地', '雷被事发，公卿请诛刘安、废王、削五县，武帝诏削二县，刘安耻于削地，谋反更甚', pid)
    if '王日夜與伍被' in t and '案輿地圖' in t:
        add_event('刘安与伍被谋划起兵', '刘安日夜与伍被、左吴等查看地图，部署进军路线，认为武帝无太子、诸侯将争位，自己是高帝孙当举事', pid)
    if '伍被諫' in t or '被悵然曰' in t:
        add_event('伍被谏刘安', '伍被以秦亡、吴楚七国败亡为鉴劝谏刘安，说当今天下太平，大将军卫青材能过人，谋反必败，刘安不听', pid)
    if '王孫建' in t and '上書' in t:
        add_event('刘建上书告变', '刘不害之子刘建因不得封侯怨太子，使庄芷上书告发太子及淮南阴谋，审卿与公孙弘深查淮南狱', pid)
    if '偽爲丞相御史請書' in t:
        add_event('伍被为刘安设谋反计', '伍被建议伪造丞相御史书迁徙郡国豪杰、伪造诏狱逮诸侯太子，制造民怨诸侯惧，再派辩士游说，以图侥幸成功', pid)
    if '偽失火' in t and '欲因以發兵' in t:
        add_event('刘安谋发兵方案', '刘安与伍被谋先杀相、二千石，又想使人着捕盗衣从东方来呼南越兵入界借此发兵，伍被建议南收衡山、东收会越南通越拖延时间', pid)
    if '太子自剄' in t and '伍被自詣吏' in t:
        add_event('太子自刎伍被自首', '廷尉逮太子，刘安召相、内史、中尉，内史、中尉不至，太子认为事不成愿就逮，自刎未死；伍被自首告发谋反', pid)
    if '上下公卿治' in t and '國除爲九江郡' in t:
        add_event('淮南谋反案发国除', '官吏围王宫捕谋反者，搜得反具，牵连数千人，胶西王端议其大逆无道，刘安自刎，王后太子族，伍被诛，淮南国除为九江郡', pid)
    if '徐來' in t and '立徐來爲王后' in t:
        add_event('衡山王室内斗', '王后乘舒死，徐来为后，厥姬谗说徐来蛊杀太子母，太子刺徐来兄，宫中无采、刘孝、徐来互相诋毁，太子与王后有隙', pid)
    if '作輣車鏃矢' in t:
        add_event('衡山王治反具', '衡山王与淮南王约反，使刘孝宾客救赫、陈喜作战车箭矢，刻天子玺、将相印，招揽壮士，计划淮南西进后定江淮', pid)
    if '白嬴之長安上書' in t:
        add_event('刘爽白嬴上书反告', '刘爽听说被废，派白嬴长安上书告刘孝反事，刘赐反告刘爽不孝，元狩元年冬刘孝家捕得陈喜', pid)
    if '孝先自告反' in t and '國除爲衡山郡':
        add_event('衡山谋反案发国除', '刘孝自首谋反，帝遣中尉安、大行息审问刘赐，刘赐自杀，刘孝因通奸弃市，徐来、刘爽弃市，谋反者族，国除为衡山郡', pid)
    
    # ---- 概念/典故提取 ----
    if '一尺布，尚可縫；一斗粟，尚可舂' in t:
        add_concept('尺布斗粟', '汉代民谣，讽刺汉文帝与淮南王兄弟不相容，后指兄弟不能相容', pid)
    if '忠言逆於耳利於行' in t or '毒藥苦於口利於病' in t:
        add_concept('良药苦口忠言逆耳', '古代谚语，指良药苦口利于病，忠言逆耳利于行', pid)
    if '麋鹿游姑蘇之臺' in t:
        add_concept('麋鹿游姑苏台', '伍子胥预言吴将亡国，宫殿将成废墟麋鹿游栖，后指亡国之兆', pid)
    if '萬舉萬全' in t:
        add_concept('万举万全', '指做事谋划周密，每次行动都万无一失', pid)
    if '士五' in t:
        add_concept('士伍', '秦汉时指有罪失去官爵的人，编入士卒伍籍', pid)
    if '關內侯' in t:
        add_concept('关内侯', '秦汉二十等爵第十九级，有侯号无封国，居京畿', pid)
    if '二千石' in t:
        add_concept('二千石', '汉代高级官员俸禄等级，月俸百二十斛，指郡守、诸侯国相以上高级官员', pid)
    if '城旦舂' in t:
        add_concept('城旦舂', '汉代刑罚，四年徒刑，男犯筑城，女犯舂米', pid)
    if '弃市' in t:
        add_concept('弃市', '古代死刑，在闹市执行死刑并暴尸街头示众', pid)
    if '黃屋蓋' in t:
        add_concept('黄屋盖', '皇帝专用的黄缯车盖，指帝王车制，僭用即谋反', pid)
    if '警蹕' in t:
        add_concept('警跸', '古代帝王出入时清道戒严，禁止行人通行，是天子礼制', pid)
    if '制' in t and '稱制' in t:
        add_concept('称制', '自称制诏，即把自己的命令称为皇帝的制，僭越天子礼制', pid)
    if '輂車' in t:
        add_concept('輂车', '古代马拉的大车、货车，可用于军事运输', pid)
    if '鋋' not in t and '棘矜' in t:
        add_concept('鉏耰棘矜', '指农具木棍，形容起义军武器简陋，出自贾谊《过秦论》，此处伍被用来形容陈胜吴广武器简陋', pid)
    if '阿房之宮' in t:
        add_concept('阿房宫', '秦始皇营建的大型宫殿，规模宏大，未完工即被项羽焚毁，是秦朝暴政象征', pid)
    if '發閭左之戍' in t:
        add_concept('闾左戍边', '秦代征发居里门左侧的贫民戍边，是秦朝暴政之一，闾左指贫民', pid)
    if '太半之賦' in t:
        add_concept('泰半之赋', '征收百姓收入三分之二作为赋税，形容赋税沉重', pid)
    if '如發蒙耳' in t:
        add_concept('发蒙振落', '揭去覆盖物、摇掉落叶，比喻轻而易举', pid)
    if '臣無將，將而誅' in t:
        add_concept('臣无将，将而诛', '《春秋》经义，指臣子不得作乱、不得有叛逆之心，有逆谋就该诛杀', pid)
    if '七國之亂' not in t and '吳楚七國反' in t:
        add_concept('吴楚七国之乱', '汉景帝三年（前154年）吴王刘濞联合楚、赵等七国以诛晁错为名发动的叛乱，三个月即被周亚夫平定', pid)
    if '轞車' in t:
        add_concept('槛车', '古代囚车，押解犯人用的有栅栏的车', pid)
    if '推恩令' not in t and '分子弟爲侯' in t:
        add_concept('推恩令', '汉武帝时主父偃建议的政策，允许诸侯王分封子弟为侯，拆分诸侯国，削弱诸侯势力', pid)
    if '蠱道' in t:
        add_concept('巫蛊', '古代巫术，用巫术诅咒害人，汉代宫廷多巫蛊之祸', pid)
    if '符節' in t:
        add_concept('符节', '古代使者所持的凭证，用竹、木、金属制成，代表皇帝授权', pid)
    if '宗正' in t:
        add_concept('宗正', '官名，九卿之一，掌管皇族事务，由皇族担任', pid)
    if '大行' in t:
        add_concept('大行令', '官名，九卿之一，原名典客，掌管少数民族事务、接待宾客、朝会礼仪', pid)
    if '廷尉' in t:
        add_concept('廷尉', '官名，九卿之一，掌管全国司法刑狱，是最高司法官', pid)
    if '戎狄是膺，荊舒是懲' in t:
        add_concept('戎狄是膺荆舒是惩', '出自《诗经·鲁颂·閟宫》，意思是打击戎狄、惩罚荆楚，司马迁用来评价淮南衡山谋反', pid)
    if '乃公' in t:
        add_concept('乃公', '傲慢自称，即「你老子我」，刘长对侍者自称，可见其骄横', pid)
    if '同姓封建' not in t and '諸侯' in t and pid >= 'p29':
        add_concept('同姓分封', '汉初分封同姓诸侯王，诸侯国强盛威胁中央，经文帝众建诸侯、景帝削藩、武帝推恩，逐步解决王国问题', pid)

# 为每个实体分配id
for i, p in enumerate(persons):
    p['id'] = f'person_{i:03d}'
for i, pl in enumerate(places):
    pl['id'] = f'place_{i:03d}'
for i, e in enumerate(events):
    e['id'] = f'event_{i:03d}'
for i, c in enumerate(concepts):
    c['id'] = f'concept_{i:03d}'

# 构建最终JSON
output = {
    'book_id': 'shiji',
    'chapter_id': '58',
    'chapter_title': '淮南衡山列传第五十八',
    'version': '1.0',
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'entities': {
        'persons': persons,
        'places': places,
        'events': events,
        'concepts': concepts
    }
}

# 写入文件
with open('/home/user/workspace/17521090448082856013/history-site/data/books/shiji/ontology/实体-初稿-淮南衡山列传第五十八.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'实体初稿生成完成：')
print(f'  人物：{len(persons)} 个')
print(f'  地名：{len(places)} 个')
print(f'  事件：{len(events)} 个')
print(f'  概念：{len(concepts)} 个')
print(f'  总段落数：{len(paragraphs)} 段')
