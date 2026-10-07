const STORAGE_KEY = 'reading-list';
const STARTER_ITEMS = [
  { id: 'r-1', title: 'Keyboard-friendly forms', url: 'https://example.test/forms', note: 'Review the keyboard flow', status: 'unread' },
  { id: 'r-2', title: '给新同事的设计笔记', url: 'https://example.test/design', note: '含有逗号，和引号“引用内容”\n第二行备注。', status: 'reading' },
  { id: 'r-3', title: 'A tiny field guide', url: 'https://example.test/field-guide', note: '', status: 'read' },
];

const status = document.querySelector('#status');
const itemsNode = document.querySelector('#items');
let items = loadItems();

function loadItems() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw === null) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(STARTER_ITEMS));
    return STARTER_ITEMS.map(item => ({ ...item }));
  }
  try {
    const saved = JSON.parse(raw);
    return Array.isArray(saved) ? saved : [];
  } catch {
    return [];
  }
}

function saveItems() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function renderItems() {
  itemsNode.replaceChildren();
  for (const item of items) {
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.href = item.url;
    link.textContent = item.title;
    const note = document.createElement('p');
    note.textContent = `${item.status}${item.note ? ` · ${item.note}` : ''}`;
    li.append(link, note);
    itemsNode.append(li);
  }
}

document.querySelector('#add-form').addEventListener('submit', event => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  items.push({
    id: crypto.randomUUID(),
    title: String(form.get('title')).trim(),
    url: String(form.get('url')).trim(),
    note: String(form.get('note')).trim(),
    status: 'unread',
  });
  saveItems();
  renderItems();
  event.currentTarget.reset();
  status.textContent = '已添加。';
});

document.querySelector('#clear-list').addEventListener('click', () => {
  items = [];
  saveItems();
  renderItems();
  status.textContent = '列表已清空。';
});

renderItems();
