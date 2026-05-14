// ============================================================================
// Insurance Fund Simulation Dashboard.
// Talks to /api and /api/population. Auto-refreshes on form input (debounced).
// ============================================================================

// Fields that travel as 0-1 floats over the wire but display as 0-100 percent.
const PERCENT_FIELDS = [
  'inflation_rate',
  'insurance_fee_from_salary',
  'added_people_rate',
  'death_to_survivor_rate',
];

// Integer / passthrough numeric fields.
const NUMBER_FIELDS = [
  'simulation_years',
  'retirement_age',
  'survivor_final_year_of_payroll',
];

const FLAG_FIELDS = [
  'basic_retirement_strategy',
  'proposed_survivor_strategy',
];

// Filled from /openapi.json at boot.
const defaults = {};

const COLORS = {
  insured: '#2f6bff',
  retired: '#d8504e',
  survivor: '#f5a623',
  azkaroftadeh: '#8b6dff',
  income: '#2aa86b',
  ageGroups: ['#2f6bff', '#5f87ff', '#8aa9ff', '#b8c9ff', '#f5a623', '#d8504e', '#8b6dff'],
};

const charts = {};
const state = {
  data: null,
  population: null,
  inflight: null,
};

// ---------------------------------------------------------------------------
// Slider ↔ number-input pairing
// ---------------------------------------------------------------------------

function pairSliderAndNumber(id) {
  const slider = document.getElementById(id + '_slider');
  const num = document.getElementById(id);
  if (!slider || !num) return;
  // Mirror in both directions. `input` fires on each step.
  slider.addEventListener('input', () => {
    num.value = slider.value;
    onConfigInput();
  });
  num.addEventListener('input', () => {
    if (num.value === '') return;
    slider.value = num.value;
    onConfigInput();
  });
}

function applyDefaultsToForm() {
  for (const id of PERCENT_FIELDS) {
    const v = defaults[id];
    if (v === undefined) continue;
    const percent = Math.round(v * 1000) / 10; // 0.222 → 22.2
    const num = document.getElementById(id);
    const slider = document.getElementById(id + '_slider');
    if (num) num.value = percent;
    if (slider) slider.value = Math.round(percent);
  }
  for (const id of NUMBER_FIELDS) {
    const v = defaults[id];
    if (v === undefined) continue;
    const num = document.getElementById(id);
    const slider = document.getElementById(id + '_slider');
    if (num) num.value = v;
    if (slider) slider.value = v;
  }
  for (const id of FLAG_FIELDS) {
    const v = defaults[id];
    if (v === undefined) continue;
    const el = document.getElementById(id);
    if (el) el.checked = !!v;
  }
}

function readConfigFromForm() {
  const body = {};
  for (const id of PERCENT_FIELDS) {
    const el = document.getElementById(id);
    if (el && el.value !== '') body[id] = Number(el.value) / 100;
  }
  for (const id of NUMBER_FIELDS) {
    const el = document.getElementById(id);
    if (el && el.value !== '') body[id] = Number(el.value);
  }
  for (const id of FLAG_FIELDS) {
    const el = document.getElementById(id);
    if (el) body[id] = !!el.checked;
  }
  return body;
}

// ---------------------------------------------------------------------------
// Fetch + render
// ---------------------------------------------------------------------------

async function loadDefaults() {
  const res = await fetch('/api/defaults');
  if (!res.ok) throw new Error(`/api/defaults ${res.status}`);
  Object.assign(defaults, await res.json());
  applyDefaultsToForm();
}

function setStatus(message, mode) {
  const el = document.getElementById('status');
  if (!el) return;
  el.textContent = message;
  el.className = `status ${mode || ''}`.trim();
}

async function runSimulation() {
  // Cancel in-flight if any — only the latest run matters.
  if (state.inflight) state.inflight.aborted = true;
  const token = { aborted: false };
  state.inflight = token;

  setStatus('در حال شبیه‌سازی…', 'loading');
  document.getElementById('refresh').disabled = true;
  try {
    const config = readConfigFromForm();
    const res = await fetch('/api/full', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    if (!res.ok) throw new Error(`/api/full ${res.status}`);
    const body = await res.json();
    if (token.aborted) return;
    state.data = body.report;
    state.population = body.population;
    renderAll();
    setStatus(`${state.data.length} سال شبیه‌سازی شد`, '');
  } catch (err) {
    if (token.aborted) return;
    console.error(err);
    setStatus(`خطا: ${err.message}`, 'error');
  } finally {
    if (state.inflight === token) state.inflight = null;
    document.getElementById('refresh').disabled = false;
  }
}

// Debounced wrapper for input-driven refresh.
let refreshTimer = null;
function onConfigInput() {
  setStatus('در انتظار…', 'loading');
  clearTimeout(refreshTimer);
  refreshTimer = setTimeout(runSimulation, 600);
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------

function renderAll() {
  if (!state.data) return;
  const rows = state.data;
  renderKpis(rows);
  renderPopulation(rows);
  renderRatio(rows);
  renderInbalance(rows);
  renderPaymentVsIncome(rows);
  renderAgeGroups();
}

function renderKpis(rows) {
  const last = rows[rows.length - 1] || {};
  // Reflect what was actually used in this run (read from the form, not defaults).
  const inflation = Number(document.getElementById('inflation_rate').value) || 0;
  const fee = Number(document.getElementById('insurance_fee_from_salary').value) || 0;
  const retire = Number(document.getElementById('retirement_age').value) || 0;
  setKpi('kpi_inflation', formatPercent(inflation));
  setKpi('kpi_fee', formatPercent(fee));
  setKpi('kpi_years', formatNumber(rows.length));
  setKpi('kpi_retire', formatNumber(retire));
  setKpi('kpi_end_pop', formatNumber(last.insured_alive_population));
  setKpi('kpi_end_inbalance', formatHemat(last.inbalance),
    (last.inbalance ?? 0) >= 0 ? 'positive' : 'negative');
}

function setKpi(id, value, mod) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = value ?? '—';
  el.classList.remove('positive', 'negative');
  if (mod) el.classList.add(mod);
}

function renderPopulation(rows) {
  const labels = rows.map(d => d.year);
  upsertChart('chart_population', {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'جمعیت کل صندوق',
          data: rows.map(d => d.sum_alive_population),
          fill: true,
          backgroundColor: 'rgba(216, 80, 78, 0.22)',
          borderColor: COLORS.retired,
          tension: 0.25,
        },
        {
          label: 'جمعیت بیمه‌شدگان',
          data: rows.map(d => d.insured_alive_population),
          fill: true,
          backgroundColor: 'rgba(47, 107, 255, 0.25)',
          borderColor: COLORS.insured,
          tension: 0.25,
        },
      ],
    },
    options: rtlChartOptions({
      scales: { y: { beginAtZero: true, ticks: { callback: formatNumberCompact, font: { size: 10 } } }, x: { ticks: { font: { size: 10 } } } },
      plugins: { legend: { position: 'bottom', rtl: true, labels: { boxWidth: 12, padding: 6, font: { size: 11 } } } },
    }),
  });
}

function renderRatio(rows) {
  const labels = rows.map(d => d.year);
  const values = rows.map(d => {
    const retired = (d.bazneshasteh_alive_population || 0) + (d.azkaroftadeh_alive_population || 0);
    if (!retired) return 0;
    return d.insured_alive_population / retired;
  });
  upsertChart('chart_ratio', {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'نسبت بیمه‌شده به بازنشسته',
        data: values,
        backgroundColor: COLORS.insured,
      }],
    },
    options: rtlChartOptions({
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: false } },
    }),
  });
}

function renderInbalance(rows) {
  const labels = rows.map(d => d.year);
  const values = rows.map(d => d.inbalance);
  upsertChart('chart_inbalance', {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'ناترازی (همت)',
        data: values,
        backgroundColor: values.map(v => v >= 0 ? COLORS.income : COLORS.retired),
      }],
    },
    options: rtlChartOptions({
      scales: { y: { ticks: { callback: formatNumberCompact } } },
      plugins: { legend: { display: false } },
    }),
  });
}

function renderPaymentVsIncome(rows) {
  const sum = key => rows.reduce((a, r) => a + (r[key] || 0), 0);
  upsertChart('chart_payment_vs_income', {
    type: 'pie',
    data: {
      labels: [
        'بازنشستگان',
        'ازکارافتادگان',
        'بازماندگان',
        'دریافتی صندوق',
      ],
      datasets: [{
        data: [
          sum('bazneshasteh_payment_obligation'),
          sum('azkaroftadeh_payment_obligation'),
          sum('survivor_payment_obligation'),
          sum('insured_sandogh_income'),
        ],
        backgroundColor: [COLORS.retired, COLORS.azkaroftadeh, COLORS.survivor, COLORS.income],
      }],
    },
    options: rtlChartOptions({
      plugins: { legend: { position: 'right', rtl: true, labels: { boxWidth: 12, padding: 6 } } },
    }),
  });
}

function renderAgeGroups() {
  if (!state.population) return;
  const years = Object.keys(state.population).map(Number).sort((a, b) => a - b);
  if (!years.length) return;
  const targetYear = years[years.length - 1];
  const groups = state.population[targetYear] || [];
  const pairs = Array.isArray(groups) ? groups : Object.entries(groups);
  // RTL paragraphs reorder digits in "30_34" → "34_30". Wrap each label with
  // U+2066 ⟨LTR Isolate⟩ + U+2069 ⟨Pop⟩ and use an en-dash separator.
  const labels = pairs.map(p => '⁦' + p[0].replace('_', '–') + '⁩');
  const values = pairs.map(p => p[1]);

  upsertChart('chart_age_groups', {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: labels.map((_, i) => COLORS.ageGroups[i % COLORS.ageGroups.length]),
      }],
    },
    options: rtlChartOptions({
      plugins: {
        title: { display: true, text: `سال ${targetYear}`, font: { size: 11 } },
        legend: { position: 'right', rtl: true, labels: { boxWidth: 12, padding: 4, font: { size: 11 } } },
      },
    }),
  });
}

// ---------------------------------------------------------------------------
// Chart.js helpers
// ---------------------------------------------------------------------------

function upsertChart(canvasId, config) {
  if (charts[canvasId]) {
    charts[canvasId].data = config.data;
    charts[canvasId].options = config.options;
    charts[canvasId].update();
  } else {
    const ctx = document.getElementById(canvasId).getContext('2d');
    charts[canvasId] = new Chart(ctx, config);
  }
}

function rtlChartOptions(extra) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    locale: 'fa-IR',
    plugins: {
      legend: { position: 'bottom', rtl: true, labels: { font: { family: 'inherit' } } },
      tooltip: { rtl: true, textDirection: 'rtl' },
      ...(extra && extra.plugins ? extra.plugins : {}),
    },
    ...extra,
  };
}

// ---------------------------------------------------------------------------
// Formatters
// ---------------------------------------------------------------------------

function formatPercent(percentValue) {
  // Input is already a percent (0-100), unlike the wire format.
  if (percentValue === undefined || percentValue === null) return '—';
  return percentValue.toLocaleString('fa-IR', { maximumFractionDigits: 1 }) + '٪';
}

function formatNumber(x) {
  if (x === undefined || x === null) return '—';
  return Math.round(x).toLocaleString('fa-IR');
}

function formatNumberCompact(value) {
  const abs = Math.abs(value);
  if (abs >= 1e9) return (value / 1e9).toFixed(1) + 'B';
  if (abs >= 1e6) return (value / 1e6).toFixed(1) + 'M';
  if (abs >= 1e3) return (value / 1e3).toFixed(1) + 'k';
  return value;
}

function formatHemat(x) {
  if (x === undefined || x === null) return '—';
  return x.toLocaleString('fa-IR', { maximumFractionDigits: 1 }) + ' همت';
}

// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------

(async function main() {
  document.getElementById('refresh').addEventListener('click', () => {
    clearTimeout(refreshTimer);
    runSimulation();
  });

  for (const id of [...PERCENT_FIELDS, ...NUMBER_FIELDS]) {
    pairSliderAndNumber(id);
  }
  for (const id of FLAG_FIELDS) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', onConfigInput);
  }

  await loadDefaults();
  await runSimulation();
})();
