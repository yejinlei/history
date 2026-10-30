// 通用页头 - 全站统一导航栏
function renderHeader(activePage) {
  return `
  <header class="site-header">
    <nav class="main-nav">
      <a href="https://yejinlei.github.io/history/index.html" class="site-title">📜 中国历史本体论</a>
      <ul class="nav-menu">
        <li><a href="https://yejinlei.github.io/history/index.html" class="${activePage === 'home' ? 'active' : ''}">首页</a></li>
        <li class="dropdown">
          <a href="https://yejinlei.github.io/history/pages/ontology.html" class="${activePage === 'ontology' ? 'active' : ''}">本体总纲 ▾</a>
          <div class="dropdown-content">
            <a href="https://yejinlei.github.io/history/pages/ontology.html">总纲索引</a>
            <a href="https://yejinlei.github.io/history/pages/ontology/architecture.html">核心架构：四轴七层</a>
            <a href="https://yejinlei.github.io/history/pages/ontology/single-books.html">单本史书构建方案</a>
            <a href="https://yejinlei.github.io/history/pages/ontology/panorama-system.html">历史全景构建方案</a>
            <a href="https://yejinlei.github.io/history/pages/ontology/roadmap.html">路线图与质量规范</a>
          </div>
        </li>
        <li class="dropdown">
          <a href="javascript:void(0)" class="${activePage === 'panorama' ? 'active' : ''}">历史全景 ▾</a>
          <div class="dropdown-content">
            <a href="https://yejinlei.github.io/history/pages/panorama.html">历史全景·概览</a>
            <a href="https://yejinlei.github.io/history/pages/statistics.html">历史统计与推论（建设中）</a>
            <div class="dropdown-divider"></div>
            <span style="display:block;padding:6px 16px;font-size:0.8em;color:#999;">跨书全局研究，合全体正史为一整体</span>
          </div>
        </li>
        <li class="dropdown">
          <a href="javascript:void(0)" class="${activePage === 'zhengshi' ? 'active' : ''}">正史 ▾</a>
          <div class="dropdown-content">
            <a href="https://yejinlei.github.io/history/pages/zhengshi-texts.html">📖 阅读正史文本</a>
            <div class="dropdown-divider"></div>
            <a href="https://yejinlei.github.io/history/pages/shiji.html">《史记》【已上线】</a>
            <a href="https://yejinlei.github.io/history/pages/zizhitongjian.html">《资治通鉴》【已上线】</a>
            <a href="javascript:void(0)" style="color:#888;cursor:not-allowed;">《汉书》（建设中）</a>
            <a href="javascript:void(0)" style="color:#888;cursor:not-allowed;">《后汉书》（建设中）</a>
            <a href="javascript:void(0)" style="color:#888;cursor:not-allowed;">《三国志》（建设中）</a>
            <div class="dropdown-divider"></div>
            <span style="display:block;padding:6px 16px;font-size:0.8em;color:#999;">其余22部正史逐步建设中</span>
          </div>
        </li>
        <li class="dropdown">
          <a href="javascript:void(0)" class="${activePage === 'topic' ? 'active' : ''}">专题研究 ▾</a>
          <div class="dropdown-content">
            <a href="https://yejinlei.github.io/history/pages/scholars.html">现代史学四大家（建设中）</a>
            <a href="javascript:void(0)" style="color:#888;cursor:not-allowed;">中国历代政治制度（建设中）</a>
            <a href="javascript:void(0)" style="color:#888;cursor:not-allowed;">历史地理沿革（建设中）</a>
          </div>
        </li>
        <li><a href="https://github.com/yejinlei/history" target="_blank">GitHub</a></li>
      </ul>
    </nav>
  </header>
  <style>
    .site-header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 64px;
      background: rgba(255, 251, 240, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 2px solid #8b2323;
      z-index: 999;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .main-nav {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 30px;
      height: 100%;
    }
    .site-title {
      font-family: "STKaiti", "KaiTi", serif;
      font-size: 1.4em;
      color: #8b2323;
      text-decoration: none;
      font-weight: bold;
      letter-spacing: 0.1em;
    }
    .nav-menu {
      list-style: none;
      display: flex;
      gap: 8px;
      margin: 0;
      padding: 0;
    }
    .nav-menu li {
      position: relative;
    }
    .nav-menu > li > a {
      display: block;
      padding: 8px 16px;
      color: #3a2a1a;
      text-decoration: none;
      font-size: 1.05em;
      border-radius: 4px;
      transition: all 0.2s;
      cursor: pointer;
    }
    .nav-menu > li > a:hover, .nav-menu > li > a.active {
      background: #8b2323;
      color: #fffbf0;
    }
    .dropdown-content {
      display: none;
      position: absolute;
      right: 0;
      top: 100%;
      background: #fffbf0;
      min-width: 260px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      border: 1px solid #d4c4a8;
      border-top: 3px solid #8b2323;
      z-index: 1000;
      border-radius: 0 0 4px 4px;
    }
    .dropdown-content a {
      display: block;
      padding: 10px 16px;
      color: #3a2a1a;
      text-decoration: none;
      transition: background 0.2s;
    }
    .dropdown-content a:hover {
      background: #f0e6d2;
      color: #8b2323;
    }
    .dropdown-divider {
      height: 1px;
      background: #d4c4a8;
      margin: 5px 0;
    }
    .dropdown:hover .dropdown-content {
      display: block;
    }
    body {
      padding-top: 64px;
      margin: 0;
      background: #f5efe0;
      font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    }
    @media (max-width: 768px) {
      .main-nav { padding: 0 15px; }
      .site-title { font-size: 1.1em; }
      .nav-menu { gap: 2px; }
      .nav-menu > li > a { padding: 6px 7px; font-size: 0.85em; }
      .dropdown-content { min-width: 200px; font-size: 0.9em; }
    }
  </style>
  `;
}

// 自动注入页头
document.addEventListener('DOMContentLoaded', function() {
  const headerDiv = document.getElementById('site-header');
  if (headerDiv) {
    headerDiv.innerHTML = renderHeader(headerDiv.dataset.page);
  }
  
  // 注疏弹窗逻辑
  const notePopups = document.querySelectorAll('.note-popup');
  const markers = document.querySelectorAll('.note-marker');
  markers.forEach(m => {
    m.addEventListener('click', function(e) {
      const noteId = this.dataset.note;
      notePopups.forEach(p => p.style.display = 'none');
      const popup = document.getElementById('note-' + noteId);
      if (popup) {
        const rect = this.getBoundingClientRect();
        popup.style.display = 'block';
        let left = rect.left + window.scrollX - 200;
        if (left < 10) left = 10;
        if (left + 450 > window.innerWidth) left = window.innerWidth - 460;
        popup.style.left = left + 'px';
        popup.style.top = (rect.bottom + window.scrollY + 8) + 'px';
      }
      e.stopPropagation();
    });
  });
  
  document.addEventListener('click', function() {
    notePopups.forEach(p => p.style.display = 'none');
  });
  notePopups.forEach(p => p.addEventListener('click', e => e.stopPropagation()));
  
  const toggleBtn = document.getElementById('toggle-notes');
  if (toggleBtn) {
    let showNotes = true;
    toggleBtn.addEventListener('click', function() {
      showNotes = !showNotes;
      markers.forEach(m => m.style.display = showNotes ? 'inline' : 'none');
      toggleBtn.textContent = showNotes ? '隐藏注疏' : '显示注疏';
      toggleBtn.classList.toggle('active', showNotes);
    });
  }
});
