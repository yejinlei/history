# 历史本体论底层数据结构关联规范（v1.0）

> 本文档规定了单本史书本体与历史全景本体之间的数据关联规则，所有数据录入必须遵守本规范。

---

## 一、整体架构：三层本体+统一ID空间

整个本体体系采用严格的三层结构，每层拥有独立命名空间，通过`global_id`统一关联：

```
┌─────────────────────────────────────────────────────────┐
│  L3 历史全景层（Global）                                  │
│  命名空间 global:  /data/global/                         │
│  实体：统一人物/事件/地理/制度/朝代/年代                   │
│  核心：去重对齐、跨书聚合、因果贯通、沿革追踪              │
└───────────────▲─────────────────────────▲───────────────┘
                │ recorded_in / same_as   │ belongs_to
┌───────────────┴─────────────────────────┴───────────────┐
│  L2 单本书本体层（Book）                                  │
│  命名空间 book:  /data/books/{book_id}/                  │
│  实体：书目元数据/体例单元/注疏/作者/版本                  │
│  核心：按书建模、体例差异化、版本校勘、注疏归属            │
└───────────────▲─────────────────────────▲───────────────┘
                │ in_paragraph / in_chapter
┌───────────────┴─────────────────────────┴───────────────┐
│  L1 原始文本层（Text）                                    │
│  命名空间 text:  /data/books/{book_id}/                  │
│  文件：text.json / annotations.json / chapters.json      │
│  核心：逐句编号、正文批注分离、版本原始面貌保留            │
└─────────────────────────────────────────────────────────┘
```

---

## 二、命名空间与全局ID规范

所有实体必须拥有唯一全局ID，格式：`{namespace}:{type}:{id}`

| 层级 | 命名空间前缀 | ID格式示例 | 说明 |
|---|---|---|---|
| 历史全景层 | `global` | `global:person:liubei` | 统一人物，name做拼音slug |
| 历史全景层 | `global` | `global:event:chibi_battle_208ad` | 统一事件，`{slug}_{年份}` |
| 历史全景层 | `global` | `global:place:chibi` | 统一地理，今地名+古地名 |
| 历史全景层 | `global` | `global:institution:keju` | 统一制度/官职 |
| 历史全景层 | `global` | `global:dynasty:han_west` | 统一朝代/时期 |
| 单本书层 | `book:shiji` | `book:shiji:chapter:benji01` | 史记第一篇本纪 |
| 单本书层 | `book:shiji` | `book:shiji:annotation:123` | 史记第123条注疏 |
| 单本书层 | `book:hanshu` | `book:hanshu:juan:001` | 汉书第一卷 |
| 文本层 | `text:shiji` | `text:shiji:sentence:benji01_001` | 史记·五帝本纪第1句 |

### ID规则
1. 所有ID使用英文小写，拼音/英文slug，不得含中文、空格、特殊字符
2. 历史全景层同一实体只有一个global_id，所有书中的对应条目均映射到这个ID
3. 单本书层ID前缀必须带book_id，避免跨书冲突
4. 文本层句子ID必须包含篇章ID，便于快速定位章节

---

## 三、各层核心数据结构定义

### 3.1 L1 原始文本层（最低层）

#### 3.1.1 篇章结构文件 `/data/books/{book_id}/chapters.json`
```json
{
  "book_id": "shiji",
  "book_name": "史记",
  "structure_type": "jizhuan", // jizhuan纪传 / biannian编年 / jishi纪事本末
  "volumes": [
    {
      "juan_id": "book:shiji:juan:001",
      "juan_number": 1,
      "juan_name": "五帝本纪第一",
      "category": "benji", // benji/biao/shu/shijia/liezhuan/ji/kaoyi
      "chapter_id": "book:shiji:chapter:benji01"
    }
  ]
}
```

#### 3.1.2 纯正文文件 `/data/books/{book_id}/text.json`
```json
{
  "book_id": "shiji",
  "chapter_id": "book:shiji:chapter:benji01",
  "chapter_name": "五帝本纪第一",
  "paragraphs": [
    {
      "para_id": "text:shiji:para:benji01_p001",
      "sentences": [
        {
          "sent_id": "text:shiji:sentence:benji01_001",
          "text": "黄帝者，少典之子，姓公孙，名曰轩辕。",
          "order_in_chapter": 1
        }
      ]
    }
  ]
}
```

#### 3.1.3 批注文件 `/data/books/{book_id}/annotations.json`
```json
{
  "book_id": "shiji",
  "annotations": [
    {
      "anno_id": "book:shiji:annotation:000001",
      "annotator": "裴骃",
      "anno_type": "shiji", // jijie/suoyin/zhengyi/hu_sheng/hanshu_yan/peisongzhi
      "target_sent_id": "text:shiji:sentence:benji01_001",
      "position_offset": 2, // 绑定到句子第几个字后
      "content": "少典，有熊氏国君也。",
      "source_version": "武英殿本三家注史记"
    }
  ]
}
```

---

### 3.2 L2 单本书本体层

#### 3.2.1 书目元数据 `/data/books/{book_id}/meta.json`
```json
{
  "book_id": "shiji",
  "book_name": "史记",
  "full_name": "太史公书",
  "author": "司马迁",
  "author_dynasty": "西汉",
  "compose_year_start": -104, // 太初元年
  "compose_year_end": -91,
  "volumes_count": 130,
  "word_count": 526500,
  "structure": {
    "benji": 12, "biao": 10, "shu": 8, "shijia": 30, "liezhuan": 70
  },
  "annotation_versions": ["裴骃集解", "司马贞索隐", "张守节正义"],
  "best_version": "中华书局点校本二十四史1959年版",
  "genre": "jizhuan_tongshi",
  "covers_period": {"start": -2697, "end": -122},
  "links": {
    "ontology_page": "/pages/shiji.html",
    "text_index": "/pages/texts/reader.html?book=shiji"
  }
}
```

#### 3.2.2 单本书实体 `/data/books/{book_id}/entities.json`
> 这是**单本书视角**下的实体，未做跨书去重，保留该书原始记载
```json
{
  "book_id": "shiji",
  "persons": [
    {
      "book_person_id": "book:shiji:person:huangdi",
      "name_in_book": "黄帝",
      "aliases_in_book": ["轩辕", "有熊氏"],
      "global_id": "global:person:huangdi", // 关联到全景层统一实体
      "first_appear_sent_id": "text:shiji:sentence:benji01_001",
      "in_chapters": ["book:shiji:chapter:benji01", "book:shiji:chapter:benji05"],
      "relations_in_book": [
        {"type": "son_of", "target": "book:shiji:person:shaodian"}
      ]
    }
  ],
  "events_in_book": [
    {
      "book_event_id": "book:shiji:event:banquan_zhan",
      "name_in_book": "阪泉之战",
      "global_id": "global:event:banquan_battle",
      "in_chapters": ["book:shiji:chapter:benji01"],
      "in_sentences": ["text:shiji:sentence:benji01_005"]
    }
  ]
}
```

---

### 3.3 L3 历史全景层（全局统一）

#### 3.3.1 统一人物库 `/data/global/persons.json`
```json
{
  "persons": [
    {
      "global_id": "global:person:huangdi",
      "name": "黄帝",
      "aliases": ["轩辕", "公孙轩辕", "有熊氏", "姬轩辕"],
      "gender": "male",
      "birth_year": -2717,
      "death_year": -2599,
      "dynasty": "global:dynasty:wudi_shidai",
      "identity": ["传说时代帝王", "华夏人文始祖"],
      "appear_in_books": [
        {
          "book_id": "shiji",
          "in_book_id": "book:shiji:person:huangdi",
          "in_chapters": ["book:shiji:chapter:benji01"]
        },
        {
          "book_id": "zizhitongjian",
          "in_book_id": "book:zizhitongjian:person:huangdi",
          "in_juan": 1
        }
      ],
      "same_as_confirmed": true, // 跨书去重已确认
      "variants_in_books": [] // 异文记录
    }
  ]
}
```

#### 3.3.2 统一事件库 `/data/global/events.json`
```json
{
  "events": [
    {
      "global_id": "global:event:chibi_battle_208ad",
      "name": "赤壁之战",
      "start_year": 208,
      "end_year": 208,
      "location": "global:place:chibi",
      "participants": [
        "global:person:caocao",
        "global:person:liubei",
        "global:person:sunquan",
        "global:person:zhouyu",
        "global:person:zhugeliang"
      ],
      "influences": ["奠定三国鼎立基础"],
      "recorded_in": [
        {"book_id": "sanguozhi", "juan": 1, "sent_id": "text:sanguozhi:..."},
        {"book_id": "zizhitongjian", "juan": 65, "sent_id": "text:zizhitongjian:..."}
      ],
      "kaoyi": [
        {
          "annotator": "司马光",
          "content": "赤壁战地，诸说不同...",
          "source_anno_id": "book:zizhitongjian:annotation:..."
        }
      ]
    }
  ]
}
```

#### 3.3.3 统一地理库 `/data/global/places.json`
#### 3.3.4 统一制度/官职库 `/data/global/institutions.json`
#### 3.3.5 统一朝代年表 `/data/global/dynasties.json`
#### 3.3.6 跨书关系库 `/data/global/relations.json`
> 存储所有全局实体之间的关系，不绑定单一书籍
```json
{
  "relations": [
    {
      "rel_id": "global:rel:000001",
      "type": "participated_in", // 预定义谓词表见本体总纲
      "from": "global:person:zhugeliang",
      "to": "global:event:chibi_battle_208ad",
      "evidence": ["text:sanguozhi:sentence:shuguo05_023", "text:zizhitongjian:juan65_012"],
      "source_book": ["sanguozhi", "zizhitongjian"]
    },
    {
      "rel_id": "global:rel:000002",
      "type": "evolves_from",
      "from": "global:institution:chaju_han",
      "to": "global:institution:jiupin_zhongzheng",
      "evidence": ["..."]
    }
  ]
}
```

---

## 四、核心关联机制：从原文到全景的四级锚点

所有全局实体最终必须锚定到原文句子，保证"无一字无来处"，形成完整溯源链：

```
global:person:huangdi （全景层统一人物）
    └── appear_in_books → book:shiji:person:huangdi （单本书视角实体）
        └── first_appear → text:shiji:sentence:benji01_001 （原文句子）
            └── 对应正文："黄帝者，少典之子，姓公孙，名曰轩辕。"
                └── 书口批注：book:shiji:annotation:000001 （裴骃集解注）
```

### 关联规则
1. **向上聚合规则**：单本书实体可以映射到多个全局实体（异名同实），必须通过`same_as`确认，未确认的标记`same_as_confirmed: false`，不进入全局统计
2. **向下溯源规则**：所有全局实体的属性、关系，必须至少有一条`evidence`指向原文sent_id，无证据的关系不入库
3. **异文保留规则**：不同书对同一事件/人物的记载差异，存在`variants_in_books`字段，不覆盖原书记载
4. **考异机制**：《资治通鉴考异》类条目直接作为`kaoyi`字段挂载到全局事件下，作为史学考证证据
5. **注疏关联规则**：注疏可以绑定全局实体（比如"徐广曰：皇甫谧云黄帝在位百年"），通过`target_sent_id`间接关联到全局实体，也可以直接标注`related_global_entity`字段

---

## 五、数据同步规则

1. **录入顺序**：L1文本层 → L2单本实体层 → L3全局对齐层，不得跳过
2. **新增一本书流程**：
   1. 放入text/annotations/chapters/meta四个基础文件
   2. 抽取该书内的persons/events/places，写入单本entities.json，先不做全局对齐
   3. 人工/半自动对齐到global_id，标记`same_as_confirmed`
   4. 全局实体库中追加appear_in_books记录
   5. 抽取全局关系，写入global/relations.json
3. **版本控制**：所有数据文件均为JSON格式，纳入Git版本管理，修改保留历史
4. **校验工具**：
   - 所有sent_id必须在text.json中存在
   - 所有global_id必须在全局实体库中存在
   - 所有relation必须有至少一条evidence
   - 不允许存在悬空引用

---

## 六、当前已落实的文件结构

```
history-site/data/
├── schema/
│   └── data-structure.md （本文档）
├── global/
│   ├── persons.json （统一人物库，待填充）
│   ├── events.json （统一事件库，待填充）
│   ├── places.json
│   ├── institutions.json
│   ├── dynasties.json
│   └── relations.json
└── books/
    ├── shiji/
    │   ├── meta.json （已完成）
    │   ├── chapters.json
    │   ├── text.json （已完成分离）
    │   ├── annotations.json （已完成分离）
    │   └── entities.json （待抽取）
    ├── zizhitongjian/
    │   └── ...
    └── hanshu/
        └── ...
```

---

## 七、后续落地步骤
1. **M1（当前）**：完成Schema规范定义、底层文件结构搭建、史记/资治通鉴L1+L2基础文件
2. **M2**：抽取史记中100个核心人物、50个核心事件，完成对齐到全局层，形成可运行样板
3. **M3**：开发自动对齐工具，支持异名匹配、消歧，批量对齐汉书、后汉书、三国志
4. **M4**：开发全局统计面板（历史全景页面），基于全局库生成各类统计、可视化
5. **M5**：补全注疏与全局实体关联，支持"点击注疏→跳转对应全局人物/地理/制度页面"
