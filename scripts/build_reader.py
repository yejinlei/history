#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, re

BOOK_META = {
    "shiji": {
        "name": "史记",
        "fullname": "史记",
        "author": "司马迁",
        "dynasty": "西汉",
        "annotation": "裴骃集解、司马贞索隐、张守节正义",
        "category": "二十四史·第一部",
        "juan": 130,
        "intro": "《史记》原名《太史公书》，是中国第一部纪传体通史，记载上起黄帝、下至汉武帝太初年间共约三千年历史。全书共一百三十篇，五十二万余字，分为十二本纪、十表、八书、三十世家、七十列传。"
    }
}

# 生成单书目录页（代替原来单页面硬编码）
def build_index(book_id):
    meta = BOOK_META[book_id]
    with open(f"data/texts/{book_id}/chapters.json", "r", encoding="utf-8") as f:
        chapters = json.load(f)
    
    # 按部分分组
    sections = {}
    for ch in chapters:
        sec = ch["section"]
        if sec not in sections:
            sections[sec] = []
        sections[sec].append(ch)
    
    sec_order = ["十二本纪","十表","八书","三十世家","七十列传","其他"]
    toc_html = ""
    for sec in sec_order:
        if sec not in sections:
            continue
        items = sections[sec]
        toc_html += f'<div class="toc-section"><div class="toc-section-title">{sec}（{len(items)}）</div><div class="toc-items">'
        for ch in items:
            toc_html += f'<a class="toc-item" href="{book_id}-reader.html?ch={ch["slug"]}">{ch["title"]}</a>'
        toc_html += '</div></div>'
    
    # 读取导航
    nav = open("pages/shiji.html","r",encoding="utf-8").read() if os.path.exists("pages/shiji.html") else ""
    # 从现有页面提取nav
    nav_match = re.search(r'(<nav.*?</nav>)', nav, re.DOTALL)
    nav_html = nav_match.group(1) if nav_match else '<nav class="navbar"></nav>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta["name"]}·目录 - 中国历史本体论</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: "Noto Serif SC", "SimSun", serif; background: #f5efe0 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Cpath d='M0 0h80v80H0z' fill='%23f5efe0'/%3E%3Cpath d='M0 0h1v80H0zm20 0h1v80h-1zm20 0h1v80h-1zm20 0h1v80h-1zm20 0h1v80h-1zM0 0h80v1H0zm0 20h80v1H0zm0 20h80v1H0zm0 20h80v1H0zm0 20h80v1H0z' fill='%23e8ddc4' opacity='.3'/%3E%3C/svg%3E"); color:#3a2e1f; min-height:100vh; }}
.navbar {{ position:sticky; top:0; z-index:100; background:rgba(245,239,224,0.95); backdrop-filter:blur(8px); border-bottom:2px solid #a33; padding:12px 24px; display:flex; align-items:center; gap:28px; }}
.navbar .logo {{ font-size:22px; font-weight:bold; color:#a33; text-decoration:none; }}
.navbar a.nav-link {{ color:#3a2e1f; text-decoration:none; font-size:16px; padding:6px 4px; position:relative; }}
.navbar a.nav-link:hover {{ color:#a33; }}
.container {{ max-width:1100px; margin:0 auto; padding:40px 24px; }}
.book-header {{ background:linear-gradient(135deg, #fff8e8 0%, #f5efe0 100%); border:1px solid #c9b48a; border-left:6px solid #a33; padding:32px 36px; margin-bottom:40px; border-radius:4px; position:relative; }}
.book-header::before {{ content:""; position:absolute; top:12px; left:12px; right:12px; bottom:12px; border:1px solid #d4c5a0; pointer-events:none; border-radius:2px; }}
.book-title {{ font-size:40px; color:#a33; font-weight:bold; margin-bottom:8px; letter-spacing:6px; }}
.book-meta {{ font-size:15px; color:#6a5a3f; margin:8px 0; line-height:1.8; }}
.book-intro {{ font-size:16px; line-height:1.9; color:#4a3f2c; margin-top:16px; text-indent:2em; }}
.toc-section {{ margin-bottom:28px; }}
.toc-section-title {{ font-size:20px; color:#a33; border-bottom:2px solid #c9b48a; padding-bottom:6px; margin-bottom:14px; font-weight:bold; letter-spacing:2px; }}
.toc-items {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:8px; }}
.toc-item {{ display:block; padding:8px 14px; background:#fff8e8; border:1px solid #e0d5ba; color:#3a2e1f; text-decoration:none; border-radius:3px; font-size:15px; transition:all .2s; }}
.toc-item:hover {{ background:#a33; color:#fff8e8; border-color:#a33; transform:translateY(-1px); }}
.footer {{ text-align:center; padding:40px 20px; color:#8a7a5f; font-size:14px; border-top:1px solid #d4c5a0; margin-top:60px; }}
</style>
</head>
<body>
{nav_html.replace("shiji.html", "shiji-index.html").replace("zizhitongjian.html","#")}
<div class="container">
    <div class="book-header">
        <div class="book-title">{meta["name"]}</div>
        <div class="book-meta">📖 作者：【{meta["dynasty"]}】{meta["author"]} &nbsp;|&nbsp; 📑 注疏：{meta["annotation"]} &nbsp;|&nbsp; 📚 分类：{meta["category"]} &nbsp;|&nbsp; 📜 共{meta["juan"]}卷</div>
        <div class="book-intro">{meta["intro"]}</div>
    </div>
    <h2 style="color:#a33; font-size:24px; margin-bottom:24px; letter-spacing:4px;">📚 篇目总目（共{len(chapters)}篇）</h2>
    {toc_html}
</div>
<div class="footer">
    中国历史本体论 · 正史文本库 · {meta["name"]}
</div>
</body>
</html>'''
    
    out = f"pages/texts/{book_id}-index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已生成目录页: {out}")

def build_reader(book_id):
    meta = BOOK_META[book_id]
    nav_html = ""
    for fn in ["pages/shiji.html","pages/zhengshi-texts.html"]:
        if os.path.exists(fn):
            c = open(fn,"r",encoding="utf-8").read()
            m = re.search(r'(<nav.*?</nav>)', c, re.DOTALL)
            if m:
                nav_html = m.group(1)
                break
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta["name"]}·正文阅读 - 中国历史本体论</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: "Noto Serif SC", "SimSun", serif; background: #f5efe0 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Cpath d='M0 0h80v80H0z' fill='%23f5efe0'/%3E%3Cpath d='M0 0h1v80H0zm20 0h1v80h-1zm20 0h1v80h-1zm20 0h1v80h-1zm20 0h1v80h-1zM0 0h80v1H0zm0 20h80v1H0zm0 20h80v1H0zm0 20h80v1H0zm0 20h80v1H0z' fill='%23e8ddc4' opacity='.3'/%3E%3C/svg%3E"); color:#3a2e1f; min-height:100vh; }}
.navbar {{ position:sticky; top:0; z-index:100; background:rgba(245,239,224,0.95); backdrop-filter:blur(8px); border-bottom:2px solid #a33; padding:12px 24px; display:flex; align-items:center; gap:28px; flex-wrap:wrap; }}
.navbar .logo {{ font-size:22px; font-weight:bold; color:#a33; text-decoration:none; }}
.navbar a.nav-link {{ color:#3a2e1f; text-decoration:none; font-size:16px; padding:6px 4px; }}
.navbar a.nav-link:hover {{ color:#a33; }}
.layout {{ display:flex; max-width:1400px; margin:0 auto; }}
.sidebar {{ width:280px; flex-shrink:0; position:sticky; top:65px; height:calc(100vh - 65px); overflow-y:auto; background:#faf4e4; border-right:2px solid #c9b48a; padding:20px 14px; }}
.sidebar::-webkit-scrollbar {{ width:6px; }}
.sidebar::-webkit-scrollbar-thumb {{ background:#c9b48a; border-radius:3px; }}
.sidebar-title {{ font-size:17px; color:#a33; font-weight:bold; margin-bottom:12px; padding-bottom:8px; border-bottom:1px solid #c9b48a; letter-spacing:2px; text-align:center; }}
.sidebar-section {{ margin-bottom:16px; }}
.sidebar-section-title {{ font-size:14px; color:#7a3030; font-weight:bold; margin:8px 0 6px; padding-left:6px; border-left:3px solid #a33; }}
.sidebar a {{ display:block; padding:5px 8px; color:#4a3f2c; text-decoration:none; font-size:14px; border-radius:3px; margin-bottom:2px; line-height:1.5; }}
.sidebar a:hover {{ background:#fff8e8; color:#a33; }}
.sidebar a.active {{ background:#a33; color:#fff8e8; }}
.main {{ flex:1; padding:40px 56px; min-width:0; }}
.chapter-header {{ text-align:center; margin-bottom:36px; padding-bottom:24px; border-bottom:2px double #c9b48a; }}
.chapter-title {{ font-size:36px; color:#3a2e1f; font-weight:bold; letter-spacing:8px; margin-bottom:14px; }}
.chapter-meta {{ font-size:14px; color:#7a6a4f; }}
.chapter-meta span {{ margin:0 10px; }}
.toolbar {{ display:flex; align-items:center; gap:16px; padding:12px 20px; background:#fff8e8; border:1px solid #d4c5a0; border-left:4px solid #a33; margin-bottom:32px; border-radius:3px; font-size:14px; flex-wrap:wrap; }}
.toolbar label {{ color:#7a6a4f; }}
.toolbar button {{ padding:6px 16px; border:1px solid #c9b48a; background:#f5efe0; color:#3a2e1f; border-radius:3px; cursor:pointer; font-family:inherit; font-size:14px; }}
.toolbar button.active, .toolbar button:hover {{ background:#a33; color:#fff8e8; border-color:#a33; }}
.toolbar .tip {{ margin-left:auto; color:#8a7a5f; font-size:13px; }}
.content {{ font-size:18px; line-height:2.1; color:#2a1e0f; }}
.content p {{ text-indent:2em; margin-bottom:8px; }}
sup.note-mark {{ color:#a33; font-weight:bold; cursor:pointer; font-size:13px; padding:0 2px; margin:0 1px; border-radius:2px; }}
sup.note-mark:hover {{ background:#a33; color:#fff8e8; }}
sup.paren-mark {{ color:#2a6a8a; cursor:pointer; font-size:13px; }}
sup.paren-mark:hover {{ background:#2a6a8a; color:#fff; }}
.note-popup {{ position:absolute; background:#fffdf5; border:1px solid #c9b48a; border-left:4px solid #a33; padding:12px 18px; border-radius:3px; box-shadow:0 4px 16px rgba(100,60,20,0.18); max-width:420px; font-size:15px; line-height:1.8; color:#4a3f2c; z-index:200; display:none; }}
.note-popup .note-tag {{ display:inline-block; background:#a33; color:#fff; padding:1px 8px; border-radius:2px; font-size:12px; margin-right:8px; }}
.note-popup .note-tag.paren {{ background:#2a6a8a; }}
.nav-buttons {{ display:flex; justify-content:space-between; margin-top:50px; padding-top:24px; border-top:1px solid #d4c5a0; }}
.nav-buttons a {{ padding:10px 24px; background:#fff8e8; border:1px solid #c9b48a; color:#3a2e1f; text-decoration:none; border-radius:3px; }}
.nav-buttons a:hover {{ background:#a33; color:#fff8e8; border-color:#a33; }}
@media (max-width:900px) {{
    .sidebar {{ display:none; }}
    .main {{ padding:24px 20px; }}
    .chapter-title {{ font-size:26px; letter-spacing:4px; }}
    .content {{ font-size:16px; line-height:1.9; }}
}}
</style>
</head>
<body>
{nav_html}
<div class="layout">
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-title">📖 {meta["name"]}目录</div>
        <div id="toc"></div>
    </aside>
    <main class="main">
        <div class="chapter-header">
            <div class="chapter-title" id="ch-title">加载中...</div>
            <div class="chapter-meta">
                <span>📝 作者：【{meta["dynasty"]}】{meta["author"]}</span>
                <span>📑 注疏：{meta["annotation"]}</span>
                <span id="ch-section"></span>
            </div>
        </div>
        <div class="toolbar">
            <label>注疏显示：</label>
            <button id="btn-show" class="active" onclick="toggleNotes(true)">显示注疏</button>
            <button id="btn-hide" onclick="toggleNotes(false)">隐藏注疏</button>
            <span class="tip">点击正文中朱红色数字查看注疏</span>
        </div>
        <div class="content" id="content"></div>
        <div class="nav-buttons" id="nav-buttons"></div>
    </main>
</div>
<div class="note-popup" id="note-popup"></div>

<script>
const BOOK_ID = "{book_id}";
let chapters = [];
let currentIdx = 0;
let notesVisible = true;

async function init() {{
    const resp = await fetch("../../data/texts/" + BOOK_ID + "/chapters.json");
    chapters = await resp.json();
    
    // build sidebar
    const sections = {{}};
    chapters.forEach((ch, i) => {{
        ch._idx = i;
        if(!sections[ch.section]) sections[ch.section] = [];
        sections[ch.section].push(ch);
    }});
    const order = ["十二本纪","十表","八书","三十世家","七十列传","十六纪","其他"];
    const toc = document.getElementById("toc");
    order.forEach(sec => {{
        if(!sections[sec]) return;
        const div = document.createElement("div");
        div.className = "sidebar-section";
        div.innerHTML = '<div class="sidebar-section-title">' + sec + '（' + sections[sec].length + '）</div>';
        sections[sec].forEach(ch => {{
            const a = document.createElement("a");
            a.href = "?ch=" + ch.slug;
            a.textContent = ch.title;
            a.dataset.slug = ch.slug;
            div.appendChild(a);
        }});
        toc.appendChild(div);
    }});
    
    // load chapter
    const params = new URLSearchParams(location.search);
    let slug = params.get("ch");
    if(!slug) slug = chapters[0].slug;
    currentIdx = chapters.findIndex(c => c.slug === slug);
    if(currentIdx < 0) currentIdx = 0;
    renderChapter();
}}

function renderChapter() {{
    const ch = chapters[currentIdx];
    document.getElementById("ch-title").textContent = ch.title;
    document.getElementById("ch-section").textContent = "📚 所属：" + ch.section;
    
    // process body - insert note marks
    let html = ch.body;
    // paragraphs
    html = html.split(/\\n+/).map(p => '<p>' + p.trim() + '</p>').join('');
    
    // insert marks for 【】 annotations
    let noteId = 1;
    const notes = [];
    
    // first handle 【】
    html = html.replace(/【([^】]+)】/g, (m, note) => {{
        const id = noteId++;
        notes.push({{id, text:note, type:"zhu"}});
        return '<sup class="note-mark" data-note="' + id + '">[' + id + ']</sup>';
    }});
    // then handle （ ） containing phonetic/explanation
    html = html.replace(/（([^）]+)）/g, (m, note) => {{
        if(/[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/.test(note) || note.length < 18) {{
            const id = noteId++;
            notes.push({{id, text:note, type:"yin"}});
            return '<sup class="note-mark paren-mark" data-note="' + id + '">(' + id + ')</sup>';
        }}
        return m;
    }});
    
    window._notes = notes;
    document.getElementById("content").innerHTML = html;
    
    // attach events
    document.querySelectorAll(".note-mark").forEach(el => {{
        el.addEventListener("click", (e) => {{
            const id = parseInt(el.dataset.note);
            showNote(e, notes.find(n => n.id === id));
        }});
    }});
    
    // update sidebar active
    document.querySelectorAll(".sidebar a").forEach(a => a.classList.remove("active"));
    const activeA = document.querySelector('.sidebar a[data-slug="' + ch.slug + '"]');
    if(activeA) {{
        activeA.classList.add("active");
        activeA.scrollIntoView({{block:"center"}});
    }}
    
    // prev/next
    const nav = document.getElementById("nav-buttons");
    nav.innerHTML = "";
    if(currentIdx > 0) {{
        const prev = chapters[currentIdx-1];
        nav.innerHTML += '<a href="?ch=' + prev.slug + '">← ' + prev.title + '</a>';
    }} else {{ nav.innerHTML += '<span></span>'; }}
    if(currentIdx < chapters.length-1) {{
        const next = chapters[currentIdx+1];
        nav.innerHTML += '<a href="?ch=' + next.slug + '">' + next.title + ' →</a>';
    }}
    
    document.title = ch.title + " - {meta["name"]} - 中国历史本体论";
    applyNoteVisibility();
}}

function showNote(e, note) {{
    const popup = document.getElementById("note-popup");
    const tagClass = note.type === "yin" ? "paren" : "";
    const tagLabel = note.type === "yin" ? "注音/简释" : "注";
    popup.innerHTML = '<span class="note-tag ' + tagClass + '">' + tagLabel + '</span>' + note.text;
    popup.style.display = "block";
    const rect = e.target.getBoundingClientRect();
    popup.style.left = (window.scrollX + rect.left) + "px";
    popup.style.top = (window.scrollY + rect.bottom + 8) + "px";
    setTimeout(() => {{
        document.addEventListener("click", closeNote, {{once:true}});
    }}, 10);
}}
function closeNote() {{ document.getElementById("note-popup").style.display = "none"; }}

function toggleNotes(show) {{
    notesVisible = show;
    document.getElementById("btn-show").classList.toggle("active", show);
    document.getElementById("btn-hide").classList.toggle("active", !show);
    applyNoteVisibility();
}}
function applyNoteVisibility() {{
    document.querySelectorAll(".note-mark").forEach(el => {{
        el.style.display = notesVisible ? "inline" : "none";
    }});
}}

init();
</script>
</body>
</html>'''
    
    out = f"pages/texts/{book_id}-reader.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已生成阅读器: {out}")

if __name__ == "__main__":
    build_index("shiji")
    build_reader("shiji")
