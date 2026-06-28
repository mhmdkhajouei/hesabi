// Works locally (direct Flask) and in Docker (Nginx proxies /api/ to backend)
const API = '/api';

// ─── SVG ICONS ──────────────────────────────────────────────────────────────

const ICON_INCOME = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>`;
const ICON_EXPENSE = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>`;
const ICON_NAV_HOME = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`;
const ICON_NAV_TX = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>`;
const ICON_NAV_CAT = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>`;

// ─── STATE ───────────────────────────────────────────────────────────────────

let state = {
  transactions: [],
  categories: [],
  balances: {},
  currentCategoryId: null,
  currentTransactionId: null,
  txDetailFromHome: false,
  txFormMode: 'add',      // 'add' | 'edit'
  catFormMode: 'add',     // 'add' | 'edit'
};

// ─── UTILITIES ───────────────────────────────────────────────────────────────

function formatAmount(n) {
  if (n === null || n === undefined) return '0 T';
  return Number(n).toLocaleString('en-US') + ' T';
}

function formatDate(d) {
  if (!d) return '—';
  const date = new Date(d);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function showToast(msg, isError = false) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.className = 'toast' + (isError ? ' error' : '');
  requestAnimationFrame(() => {
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
  });
}

function setError(id, msg) {
  const el = document.getElementById(id);
  if (el) el.textContent = msg;
}

function clearError(id) {
  const el = document.getElementById(id);
  if (el) el.textContent = '';
}

async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Something went wrong');
  return data;
}

// ─── NAVIGATION ──────────────────────────────────────────────────────────────

function navigateTo(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.querySelectorAll('.bottom-nav-item').forEach(n => n.classList.remove('active'));

  const page = document.getElementById('page-' + pageId);
  if (page) page.classList.add('active');

  const navMap = { home: 0, transactions: 1, categories: 2 };
  const navItems = document.querySelectorAll('.nav-item');
  const navIndex = navMap[pageId];
  if (navIndex !== undefined) navItems[navIndex].classList.add('active');

  const bottomNavItem = document.querySelector(`.bottom-nav-item[data-page="${pageId}"]`);
  if (bottomNavItem) bottomNavItem.classList.add('active');

  if (pageId === 'home') loadHome();
  if (pageId === 'transactions') loadTransactions();
  if (pageId === 'categories') loadCategories();
}

// ─── HOME ────────────────────────────────────────────────────────────────────

async function loadHome() {
  try {
    const [total, income, expense, txData] = await Promise.all([
      apiFetch('/compute/total'),
      apiFetch('/compute/income'),
      apiFetch('/compute/expense'),
      apiFetch('/transactions/'),
    ]);

    document.getElementById('total-balance').textContent = formatAmount(total.total);
    document.getElementById('income-balance').textContent = formatAmount(income.income);
    document.getElementById('expense-balance').textContent = formatAmount(expense.expense);

    const list = txData.data || [];
    const recent = list.slice(-3).reverse();
    renderTxList('home-tx-list', recent, true);
  } catch (e) {
    console.error('loadHome error:', e);
    showToast(e.message, true);
  }
}

// ─── TRANSACTIONS ────────────────────────────────────────────────────────────

async function loadTransactions() {
  try {
    const [txData, catData] = await Promise.all([
      apiFetch('/transactions/'),
      apiFetch('/categories/'),
    ]);

    state.transactions = txData.data || [];
    state.categories = catData.data || [];

    renderTxList('all-tx-list', [...state.transactions].reverse(), false);
    populateCategorySelect();
  } catch (e) {
    showToast(e.message, true);
  }
}

function renderTxList(containerId, transactions, isHome) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!transactions.length) {
    container.innerHTML = '<div class="empty-state">No transactions yet. Add your first one.</div>';
    return;
  }

  container.innerHTML = transactions.map(tx => {
    const isIncome = tx.transaction_type === 'income';
    const icon = isIncome ? ICON_INCOME : ICON_EXPENSE;
    const pillClass = isIncome ? 'income' : 'expense';
    const pillLabel = isIncome ? 'income' : 'expense';
    const catName = tx.category_id ? getCategoryName(tx.category_id) : '';
    const dateStr = catName ? `${formatDate(tx.transaction_date)} · ${catName}` : formatDate(tx.transaction_date);
    const note = tx.note || 'No note';

    return `
      <div class="tx-card" onclick="openTransactionDetail(${tx.transaction_id}, '${isHome ? 'home' : 'transactions'}')">
        <div class="tx-left">
          <div class="tx-icon ${pillClass}">${icon}</div>
          <div>
            <div class="tx-name">${tx.note || (isIncome ? 'Income' : 'Expense')}</div>
            <div class="tx-date">${dateStr}</div>
          </div>
        </div>
        <div class="tx-right">
          <div class="tx-amount">${formatAmount(tx.amount)}</div>
          <div class="tx-pill ${pillClass}">
            ${icon}
            ${pillLabel}
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function getCategoryName(id) {
  const cat = state.categories.find(c => c.category_id === id);
  return cat ? cat.category_name : '';
}

function populateCategorySelect() {
  const select = document.getElementById('tx-category');
  if (!select) return;
  const options = state.categories.map(c =>
    `<option value="${c.category_id}">${c.category_name}</option>`
  ).join('');
  select.innerHTML = '<option value="">None</option>' + options;
}

async function submitTransaction() {
  clearError('tx-error');

  const amount = parseInt(document.getElementById('tx-amount').value);
  const type = document.getElementById('tx-type').value;
  const date = document.getElementById('tx-date').value;
  const categoryId = document.getElementById('tx-category').value;
  const note = document.getElementById('tx-note').value;

  if (!amount || amount <= 0) { setError('tx-error', 'Amount must be greater than zero.'); return; }
  if (!date) { setError('tx-error', 'Date is required.'); return; }

  const body = {
    amount,
    transaction_type: type,
    transaction_date: date,
    category_id: categoryId ? parseInt(categoryId) : null,
    note: note || null,
  };

  try {
    if (state.txFormMode === 'edit') {
      await apiFetch(`/transactions/${state.currentTransactionId}`, {
        method: 'PUT',
        body: JSON.stringify(body),
      });
      showToast('Transaction updated');
    } else {
      await apiFetch('/transactions/', { method: 'POST', body: JSON.stringify(body) });
      showToast('Transaction added');
    }
    resetTxForm();
    await loadTransactions();
    if (state.txFormMode === 'edit') navigateTo('transactions');
  } catch (e) {
    setError('tx-error', e.message);
  }
}

function resetTxForm() {
  document.getElementById('tx-amount').value = '';
  document.getElementById('tx-type').value = 'expense';
  document.getElementById('tx-date').value = todayString();
  document.getElementById('tx-category').value = '';
  document.getElementById('tx-note').value = '';
  clearError('tx-error');
  state.txFormMode = 'add';
  document.getElementById('tx-submit-label').textContent = 'Add transaction';
}

async function startEditTransaction() {
  const tx = state.transactions.find(t => t.transaction_id === state.currentTransactionId);
  if (!tx) { showToast('Transaction not found', true); return; }

  await loadTransactions(); // ensures category select is populated

  document.getElementById('tx-amount').value = tx.amount;
  document.getElementById('tx-type').value = tx.transaction_type;
  document.getElementById('tx-date').value = (tx.transaction_date || '').split('T')[0].split(' ')[0];
  document.getElementById('tx-category').value = tx.category_id || '';
  document.getElementById('tx-note').value = tx.note || '';
  clearError('tx-error');

  state.txFormMode = 'edit';
  document.getElementById('tx-submit-label').textContent = 'Save changes';

  navigateTo('transactions');
}

async function deleteTransaction() {
  if (!confirm('Delete this transaction? This cannot be undone.')) return;
  try {
    await apiFetch(`/transactions/${state.currentTransactionId}`, { method: 'DELETE' });
    showToast('Transaction deleted');
    navigateTo(state.txDetailFromHome ? 'home' : 'transactions');
  } catch (e) {
    showToast(e.message, true);
  }
}

function todayString() {
  return new Date().toISOString().split('T')[0];
}

// ─── TRANSACTION DETAIL ───────────────────────────────────────────────────────

async function openTransactionDetail(txId, from) {
  state.currentTransactionId = txId;
  state.txDetailFromHome = from === 'home';

  const backBtn = document.getElementById('tx-detail-back');
  if (backBtn) {
    backBtn.onclick = () => navigateTo(from === 'home' ? 'home' : 'transactions');
    backBtn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
      Back to ${from === 'home' ? 'home' : 'transactions'}
    `;
  }

  let tx = state.transactions.find(t => t.transaction_id === txId);

  if (!tx) {
    try {
      const res = await apiFetch('/transactions/');
      state.transactions = res.data || [];
      tx = state.transactions.find(t => t.transaction_id === txId);
    } catch (e) {
      showToast(e.message, true);
      return;
    }
  }

  if (!tx) { showToast('Transaction not found', true); return; }

  const isIncome = tx.transaction_type === 'income';
  const catName = tx.category_id ? getCategoryName(tx.category_id) : '—';

  document.getElementById('tx-detail-content').innerHTML = `
    <div class="detail-row"><span class="detail-key">Amount</span><span class="detail-val">${formatAmount(tx.amount)}</span></div>
    <div class="detail-row">
      <span class="detail-key">Type</span>
      <span class="detail-val">
        <span class="tx-pill ${isIncome ? 'income' : 'expense'}" style="font-size:12px">
          ${isIncome ? ICON_INCOME : ICON_EXPENSE}
          ${tx.transaction_type}
        </span>
      </span>
    </div>
    <div class="detail-row"><span class="detail-key">Date</span><span class="detail-val">${formatDate(tx.transaction_date)}</span></div>
    <div class="detail-row"><span class="detail-key">Category</span><span class="detail-val">${catName}</span></div>
    <div class="detail-row"><span class="detail-key">Note</span><span class="detail-val">${tx.note || '—'}</span></div>
    <div class="detail-row"><span class="detail-key">ID</span><span class="detail-val" style="color:var(--color-text-muted)">#${tx.transaction_id}</span></div>
  `;

  navigateTo('transaction-detail');
}

// ─── CATEGORIES ───────────────────────────────────────────────────────────────

async function loadCategories() {
  try {
    const [catData, balanceData] = await Promise.all([
      apiFetch('/categories/'),
      apiFetch('/compute/categories/balance'),
    ]);

    state.categories = catData.data || [];
    const balances = balanceData.categories_balance || [];

    const balanceMap = {};
    balances.forEach(b => { balanceMap[b.name] = b; });

    renderCategoryGrid(state.categories, balanceMap);
  } catch (e) {
    showToast(e.message, true);
  }
}

function renderCategoryGrid(categories, balanceMap) {
  const grid = document.getElementById('cat-grid');
  if (!grid) return;

  if (!categories.length) {
    grid.innerHTML = '<div class="empty-state" style="grid-column:1/-1">No categories yet. Add your first one.</div>';
    return;
  }

  grid.innerHTML = categories.map(cat => {
    const b = balanceMap[cat.category_name] || { budget: 0, spent: 0, remaining: 0 };
    const pct = b.budget > 0 ? Math.min(100, Math.round((b.spent / b.budget) * 100)) : 0;
    const overBudget = pct >= 100;

    return `
      <div class="cat-card" onclick="openCategoryDetail(${cat.category_id})">
        <div class="cat-name">${cat.category_name}</div>
        <div class="cat-bar-bg">
          <div class="cat-bar-fill ${overBudget ? 'over-budget' : ''}" style="width:${pct}%"></div>
        </div>
        <div class="cat-stats">
          <div class="cat-stat">Spent<span>${formatAmount(b.spent)}</span></div>
          <div class="cat-stat">Budget<span>${formatAmount(b.budget)}</span></div>
          <div class="cat-stat">Remaining<span>${formatAmount(b.remaining)}</span></div>
        </div>
      </div>
    `;
  }).join('');
}

async function submitCategory() {
  clearError('cat-error');

  const name = document.getElementById('cat-name').value.trim();
  const budget = parseInt(document.getElementById('cat-budget').value);

  if (!name) { setError('cat-error', 'Category name is required.'); return; }
  if (!budget || budget <= 0) { setError('cat-error', 'Budget goal must be greater than zero.'); return; }

  try {
    if (state.catFormMode === 'edit') {
      await apiFetch(`/categories/${state.currentCategoryId}`, {
        method: 'PUT',
        body: JSON.stringify({ category_name: name, budget_goal: budget }),
      });
      showToast('Category updated');
    } else {
      await apiFetch('/categories/', {
        method: 'POST',
        body: JSON.stringify({ category_name: name, budget_goal: budget }),
      });
      showToast('Category added');
    }
    resetCatForm();
    await loadCategories();
    if (state.catFormMode === 'edit') navigateTo('categories');
  } catch (e) {
    setError('cat-error', e.message);
  }
}

function resetCatForm() {
  document.getElementById('cat-name').value = '';
  document.getElementById('cat-budget').value = '';
  clearError('cat-error');
  state.catFormMode = 'add';
  document.getElementById('cat-submit-label').textContent = 'Add category';
}

async function startEditCategory() {
  const cat = state.categories.find(c => c.category_id === state.currentCategoryId);
  if (!cat) { showToast('Category not found', true); return; }

  document.getElementById('cat-name').value = cat.category_name;
  document.getElementById('cat-budget').value = cat.budget_goal || '';
  clearError('cat-error');

  state.catFormMode = 'edit';
  document.getElementById('cat-submit-label').textContent = 'Save changes';

  navigateTo('categories');
}

async function deleteCategory() {
  if (!confirm('Delete this category? Its transactions will lose their category reference.')) return;
  try {
    await apiFetch(`/categories/${state.currentCategoryId}`, { method: 'DELETE' });
    showToast('Category deleted');
    navigateTo('categories');
  } catch (e) {
    showToast(e.message, true);
  }
}

// ─── CATEGORY DETAIL ──────────────────────────────────────────────────────────

async function openCategoryDetail(categoryId) {
  state.currentCategoryId = categoryId;

  try {
    const [catData, balanceData, txData] = await Promise.all([
      apiFetch('/categories/'),
      apiFetch(`/compute/category/${categoryId}/balance`),
      apiFetch('/transactions/'),
    ]);

    const cat = (catData.data || []).find(c => c.category_id === categoryId);
    if (!cat) { showToast('Category not found', true); return; }

    state.categories = catData.data || [];
    state.transactions = txData.data || [];

    const b = balanceData.category_balance || { budget: 0, spent: 0, remaining: 0 };
    const pct = b.budget > 0 ? Math.min(100, Math.round((b.spent / b.budget) * 100)) : 0;
    const overBudget = pct >= 100;

    document.getElementById('cat-detail-name').textContent = cat.category_name;

    document.getElementById('cat-detail-stats').innerHTML = `
      <div class="detail-row"><span class="detail-key">Budget goal</span><span class="detail-val">${formatAmount(b.budget)}</span></div>
      <div class="detail-row"><span class="detail-key">Total spent</span><span class="detail-val">${formatAmount(b.spent)}</span></div>
      <div class="detail-row"><span class="detail-key">Remaining</span><span class="detail-val">${formatAmount(b.remaining)}</span></div>
      <div class="detail-row"><span class="detail-key">Usage</span><span class="detail-val">${pct}%</span></div>
      <div class="cat-bar-bg" style="margin-top:8px">
        <div class="cat-bar-fill ${overBudget ? 'over-budget' : ''}" style="width:${pct}%"></div>
      </div>
    `;

    const catTx = state.transactions.filter(tx => tx.category_id === categoryId).reverse();
    renderTxList('cat-detail-tx-list', catTx, false);

    navigateTo('category-detail');
  } catch (e) {
    showToast(e.message, true);
  }
}

// ─── NAV ICONS ───────────────────────────────────────────────────────────────

function injectNavIcons() {
  const items = document.querySelectorAll('.nav-item');
  const icons = [ICON_NAV_HOME, ICON_NAV_TX, ICON_NAV_CAT];
  items.forEach((item, i) => {
    const icon = document.createElement('span');
    icon.innerHTML = icons[i];
    item.prepend(icon);
  });
}

// ─── INIT ────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  injectNavIcons();

  const today = todayString();
  const txDateInput = document.getElementById('tx-date');
  if (txDateInput) txDateInput.value = today;

  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      const page = item.dataset.page;
      if (page) navigateTo(page);
    });
  });

  document.querySelectorAll('.bottom-nav-item').forEach(item => {
    item.addEventListener('click', () => {
      const page = item.dataset.page;
      if (page) navigateTo(page);
    });
  });

  loadHome();
});