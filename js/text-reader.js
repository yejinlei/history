// 正史文本阅读页 - 公共逻辑
let currentBook = null;
let currentChapterIdx = {}; // {groupId, itemId}
let notesHidden = false;

function getBookById(id) {
  return ZHENGSHI_BOOKS.find(b => b.id === id);
}

// 渲染左侧目录
function renderSidebar(bookId, activeFile) {
  const book = getBookById(bookId);
  if (!book) return;
  currentBook = book;
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;
  let html = `<div class="sidebar-title">📚 ${book.title}目录</div>`;
  book.groups.forEach((group, gi) => {
    html += `<div class="juan-group"><div class="juan-group-title">${group.name}</div><ul class="chapter-list">`;
    group.list.forEach((item, ii) => {
      const cls = item.file === activeFile ? 'active' : (item.status === 'wip' ? 'wip' : '');
      if (item.status === 'online' && item.file) {
        html += `<li><a href="${item.file}" class="${cls}">${item.title}</a></li>`;
      } else {
        html += `<li><a href="javascript:void(0)" class="${cls}" title="录入中">${item.title}</a></li>`;
      }
      if (item.file === activeFile) {
        currentChapterIdx = {groupId: gi, itemId: ii};
      }
    });
    html += `</ul></div>`;
  });
  sidebar.innerHTML = html;
}

// 注疏弹窗逻辑
function initNotePopups() {
  const popup = document.getElementById('note-popup');
  const markers = document.querySelectorAll('.note-marker');
  markers.forEach(m => {
    m.addEventListener('click', (e) => {
      e.stopPropagation();
      const source = m.getAttribute('data-source');
      const content = m.getAttribute('data-content');
      popup.querySelector('.note-source').textContent = source;
      popup.querySelector('.note-body').textContent = content;
      const rect = m.getBoundingClientRect();
      let left = rect.right + 10;
      let top = rect.top;
      if (left + 480 > window.innerWidth) left = rect.left - 490;
      if (top + 200 > window.innerHeight) top = window.innerHeight - 220;
      if (top < 10) top = 10;
      popup.style.left = left + 'px';
      popup.style.top = top + 'px';
      popup.style.display = 'block';
    });
  });
  document.querySelector('.note-popup .close-btn').addEventListener('click', () => {
    popup.style.display = 'none';
  });
  document.addEventListener('click', (e) => {
    if (!popup.contains(e.target) && !e.target.classList.contains('note-marker')) {
      popup.style.display = 'none';
    }
  });
}

// 切换注疏显示
function toggleNotes(btn) {
  notesHidden = !notesHidden;
  const markers = document.querySelectorAll('.note-marker');
  markers.forEach(m => {
    m.style.display = notesHidden ? 'none' : 'inline';
  });
  if (notesHidden) {
    document.getElementById('note-popup').style.display = 'none';
  }
  btn.textContent = notesHidden ? '显示注疏' : '隐藏注疏';
  btn.classList.toggle('active');
}

// 前后篇导航
function renderNav(bookId, activeFile) {
  const nav = document.getElementById('text-nav');
  if (!nav) return;
  const book = getBookById(bookId);
  if (!book) return;
  let flat = [];
  book.groups.forEach(g => g.list.forEach(i => flat.push(i)));
  const onlineItems = flat.filter(i => i.status === 'online' && i.file);
  const idx = onlineItems.findIndex(i => i.file === activeFile);
  let html = '<a href="../zhengshi-texts.html">← 返回正史列表</a><span style="display:flex;gap:10px;">';
  if (idx > 0) {
    html += `<a href="${onlineItems[idx-1].file}">← ${onlineItems[idx-1].title}</a>`;
  } else {
    html += `<a href="../books/${bookId}-toc.html">← ${book.title}目录</a>`;
  }
  if (idx < onlineItems.length - 1) {
    html += `<a href="${onlineItems[idx+1].file}">${onlineItems[idx+1].title} →</a>`;
  }
  html += '</span>';
  nav.innerHTML = html;
}
