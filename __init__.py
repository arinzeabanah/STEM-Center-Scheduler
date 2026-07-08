/* STEM Center Scheduler — Tallahassee State College
   Palette: TSC navy + gold on a cool paper background. */

:root {
  --navy: #14336b;
  --navy-deep: #0c2148;
  --gold: #f2b70c;
  --gold-soft: #fdf3d3;
  --paper: #f4f6fa;
  --card: #ffffff;
  --ink: #1c2333;
  --ink-soft: #5b6478;
  --line: #dde3ee;
  --danger: #b3261e;
  --danger-soft: #fceceb;
  --ok: #1a7f4b;
  --ok-soft: #e6f4ec;
  --radius: 10px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: "Inter", system-ui, sans-serif;
  background: var(--paper);
  color: var(--ink);
  min-height: 100vh;
}

h1, h2 { font-family: "Archivo", "Inter", sans-serif; }

/* ---------- Top bar ---------- */

.topbar {
  background: var(--navy);
  border-bottom: 4px solid var(--gold);
  color: #fff;
}

.topbar-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.brand { display: flex; align-items: center; gap: 14px; }

.brand-mark {
  font-family: "Archivo", sans-serif;
  font-weight: 800;
  font-size: 18px;
  background: var(--gold);
  color: var(--navy-deep);
  padding: 8px 10px;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.brand-text h1 { font-size: 20px; font-weight: 700; line-height: 1.2; }
.brand-text p { font-size: 12px; color: #c5d0e8; }

.date-nav { display: flex; align-items: center; gap: 8px; }

.date-nav input[type="date"] {
  background: var(--navy-deep);
  color: #fff;
  border: 1px solid #2c4a8a;
  border-radius: 8px;
  padding: 7px 10px;
  font-family: inherit;
  font-size: 14px;
  color-scheme: dark;
}

.nav-btn {
  background: var(--navy-deep);
  color: #fff;
  border: 1px solid #2c4a8a;
  border-radius: 8px;
  padding: 7px 12px;
  cursor: pointer;
  font-size: 14px;
  font-family: inherit;
}

.nav-btn:hover { background: #1b3d80; }
.nav-btn.today { background: var(--gold); color: var(--navy-deep); border-color: var(--gold); font-weight: 600; }
.nav-btn:focus-visible, button:focus-visible, input:focus-visible,
select:focus-visible, textarea:focus-visible {
  outline: 3px solid var(--gold);
  outline-offset: 1px;
}

/* ---------- Layout ---------- */

.layout {
  max-width: 1100px;
  margin: 28px auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  align-items: start;
}

.panel {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 22px;
}

.panel h2 { font-size: 17px; margin-bottom: 16px; color: var(--navy-deep); }

/* ---------- Form ---------- */

.field { margin-bottom: 14px; display: flex; flex-direction: column; }
.field-row { display: flex; gap: 10px; }
.field-row .field { flex: 1; min-width: 0; }

label { font-size: 13px; font-weight: 600; margin-bottom: 5px; color: var(--ink); }
.optional { font-weight: 400; color: var(--ink-soft); }

input, select, textarea {
  font-family: inherit;
  font-size: 14px;
  padding: 9px 11px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fff;
  color: var(--ink);
  width: 100%;
}

textarea { resize: vertical; }

.submit-btn {
  width: 100%;
  background: var(--navy);
  color: #fff;
  font-family: "Archivo", sans-serif;
  font-weight: 700;
  font-size: 15px;
  border: none;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  margin-top: 4px;
  transition: background 0.15s ease;
}

.submit-btn:hover { background: var(--navy-deep); }
.submit-btn:disabled { background: var(--ink-soft); cursor: not-allowed; }

.sync-note { font-size: 12px; color: var(--ink-soft); margin-top: 10px; }

/* ---------- Alerts & conflicts ---------- */

.alert {
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 13px;
  margin-bottom: 14px;
}

.alert.error { background: var(--danger-soft); color: var(--danger); border: 1px solid #eec4c1; }
.alert.success { background: var(--ok-soft); color: var(--ok); border: 1px solid #bfe3cf; }

.conflict-box {
  background: var(--danger-soft);
  border: 1px solid #eec4c1;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 14px;
  font-size: 13px;
}

.conflict-box h3 { font-size: 13px; color: var(--danger); margin-bottom: 6px; }
.conflict-box ul { list-style: none; margin-bottom: 8px; }
.conflict-box li { padding: 2px 0; color: var(--ink); }

.suggestion-btns { display: flex; flex-wrap: wrap; gap: 6px; }

.suggestion-btn {
  background: #fff;
  border: 1px solid var(--navy);
  color: var(--navy);
  border-radius: 999px;
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}

.suggestion-btn:hover { background: var(--navy); color: #fff; }

/* ---------- Schedule ---------- */

.schedule-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.schedule-header h2 { margin-bottom: 0; }
.schedule-header select { width: auto; }

.event-list { display: flex; flex-direction: column; gap: 10px; }

.event-card {
  display: flex;
  gap: 14px;
  border: 1px solid var(--line);
  border-left: 4px solid var(--gold);
  border-radius: 8px;
  padding: 12px 14px;
  background: #fff;
}

.event-time {
  min-width: 86px;
  font-family: "Archivo", sans-serif;
  font-weight: 700;
  font-size: 13px;
  color: var(--navy);
  line-height: 1.5;
}

.event-body { flex: 1; min-width: 0; }
.event-body h3 { font-size: 15px; margin-bottom: 2px; }
.event-meta { font-size: 12.5px; color: var(--ink-soft); }

.badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  background: var(--gold-soft);
  color: #7a5c00;
  border-radius: 999px;
  padding: 2px 8px;
  margin-top: 6px;
}

.cancel-btn {
  align-self: center;
  background: none;
  border: 1px solid var(--line);
  color: var(--ink-soft);
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 12px;
  cursor: pointer;
  font-family: inherit;
  white-space: nowrap;
}

.cancel-btn:hover { border-color: var(--danger); color: var(--danger); }

.empty-state {
  text-align: center;
  color: var(--ink-soft);
  padding: 48px 16px;
  font-size: 14px;
  border: 1px dashed var(--line);
  border-radius: 8px;
}

/* ---------- Responsive ---------- */

@media (max-width: 860px) {
  .layout { grid-template-columns: 1fr; }
  .field-row { flex-direction: column; gap: 0; }
}

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; }
}
