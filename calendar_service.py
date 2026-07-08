/**
 * STEM Center Scheduler — frontend
 * Vanilla JS client for the Flask API: loads rooms, renders the daily
 * schedule, runs live conflict checks before booking, and offers
 * alternative time slots when a conflict is found.
 */

const $ = (id) => document.getElementById(id);

const state = {
  viewDate: todayISO(),
  rooms: [],
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function todayISO() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function fmtTime(iso) {
  return new Date(iso).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });
}

function shiftDate(isoDate, days) {
  const d = new Date(isoDate + "T12:00:00");
  d.setDate(d.getDate() + days);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

function showAlert(message, kind) {
  const box = $("form-alert");
  box.textContent = message;
  box.className = `alert ${kind}`;
  box.hidden = false;
  setTimeout(() => (box.hidden = true), 6000);
}

// ---------------------------------------------------------------------------
// Rooms
// ---------------------------------------------------------------------------

async function loadRooms() {
  const { data } = await api("/api/rooms");
  state.rooms = data;

  const roomSelect = $("f-room");
  const filterSelect = $("room-filter");
  roomSelect.innerHTML = "";

  for (const room of data) {
    const opt = new Option(`${room.name} (seats ${room.capacity})`, room.id);
    roomSelect.add(opt);
    filterSelect.add(new Option(room.name, room.id));
  }
}

// ---------------------------------------------------------------------------
// Schedule
// ---------------------------------------------------------------------------

async function loadSchedule() {
  const params = new URLSearchParams({ date: state.viewDate });
  const roomFilter = $("room-filter").value;
  if (roomFilter) params.set("room_id", roomFilter);

  const { data } = await api(`/api/events?${params}`);
  renderSchedule(data);
}

function renderSchedule(events) {
  const list = $("event-list");
  list.innerHTML = "";

  if (!events.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No bookings for this day yet. Use the form to reserve a room.";
    list.appendChild(empty);
    return;
  }

  for (const ev of events) {
    const card = document.createElement("article");
    card.className = "event-card";

    const time = document.createElement("div");
    time.className = "event-time";
    time.innerHTML = `${fmtTime(ev.start_time)}<br>${fmtTime(ev.end_time)}`;

    const body = document.createElement("div");
    body.className = "event-body";

    const title = document.createElement("h3");
    title.textContent = ev.title;

    const meta = document.createElement("p");
    meta.className = "event-meta";
    meta.textContent = `${ev.room_name} · ${ev.organizer_name}`;

    body.append(title, meta);

    if (ev.synced_to_google) {
      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = "Synced to Google Calendar";
      body.appendChild(badge);
    }

    const cancel = document.createElement("button");
    cancel.className = "cancel-btn";
    cancel.textContent = "Cancel";
    cancel.addEventListener("click", () => cancelEvent(ev));

    card.append(time, body, cancel);
    list.appendChild(card);
  }
}

async function cancelEvent(ev) {
  if (!confirm(`Cancel "${ev.title}"?`)) return;
  const { ok } = await api(`/api/events/${ev.id}`, { method: "DELETE" });
  if (ok) {
    showAlert("Booking cancelled.", "success");
    loadSchedule();
  }
}

// ---------------------------------------------------------------------------
// Booking + conflict detection
// ---------------------------------------------------------------------------

function readForm() {
  return {
    title: $("f-title").value.trim(),
    organizer_name: $("f-name").value.trim(),
    organizer_email: $("f-email").value.trim(),
    description: $("f-desc").value.trim(),
    room_id: Number($("f-room").value),
    start_time: `${$("f-date").value}T${$("f-start").value}`,
    end_time: `${$("f-date").value}T${$("f-end").value}`,
  };
}

async function liveConflictCheck() {
  const box = $("conflict-box");
  const { room_id, start_time, end_time } = readForm();

  if (!$("f-date").value || !$("f-start").value || !$("f-end").value || !room_id) {
    box.hidden = true;
    return;
  }

  const { ok, data } = await api("/api/check-conflicts", {
    method: "POST",
    body: JSON.stringify({ room_id, start_time, end_time }),
  });

  if (!ok || !data.has_conflict) {
    box.hidden = true;
    return;
  }

  renderConflicts(data);
}

function renderConflicts(data) {
  const box = $("conflict-box");
  box.innerHTML = "";

  const heading = document.createElement("h3");
  heading.textContent = "This time conflicts with an existing booking";

  const ul = document.createElement("ul");
  for (const c of data.conflicts) {
    const li = document.createElement("li");
    li.textContent = `• ${c.title} — ${fmtTime(c.start_time)}–${fmtTime(c.end_time)}`;
    ul.appendChild(li);
  }

  box.append(heading, ul);

  if (data.suggestions.length) {
    const label = document.createElement("p");
    label.textContent = "Open slots the same day:";
    label.style.marginBottom = "6px";

    const btns = document.createElement("div");
    btns.className = "suggestion-btns";

    for (const s of data.suggestions) {
      const btn = document.createElement("button");
      btn.className = "suggestion-btn";
      btn.textContent = `${fmtTime(s.start_time)} – ${fmtTime(s.end_time)}`;
      btn.addEventListener("click", () => {
        $("f-start").value = s.start_time.slice(11, 16);
        $("f-end").value = s.end_time.slice(11, 16);
        box.hidden = true;
      });
      btns.appendChild(btn);
    }

    box.append(label, btns);
  }

  box.hidden = false;
}

async function submitBooking() {
  const payload = readForm();

  if (!payload.title || !payload.organizer_name || !payload.organizer_email) {
    showAlert("Please fill in the event title, your name, and email.", "error");
    return;
  }
  if (!$("f-date").value) {
    showAlert("Please pick a date.", "error");
    return;
  }

  const btn = $("submit-btn");
  btn.disabled = true;
  btn.textContent = "Booking…";

  const { ok, status, data } = await api("/api/events", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  btn.disabled = false;
  btn.textContent = "Book room";

  if (status === 409) {
    renderConflicts({ conflicts: data.conflicts, suggestions: [] });
    liveConflictCheck(); // refresh with suggestions
    showAlert("Scheduling conflict detected — pick an open slot below.", "error");
    return;
  }

  if (!ok) {
    showAlert(data.error || "Booking failed. Check the form and try again.", "error");
    return;
  }

  showAlert("Room booked. A confirmation email is on its way.", "success");
  $("f-title").value = "";
  $("f-desc").value = "";
  $("conflict-box").hidden = true;

  // Jump the schedule view to the booked date so the new event is visible.
  state.viewDate = $("f-date").value;
  $("view-date").value = state.viewDate;
  loadSchedule();
}

// ---------------------------------------------------------------------------
// Wiring
// ---------------------------------------------------------------------------

function init() {
  $("view-date").value = state.viewDate;
  $("f-date").value = state.viewDate;

  $("view-date").addEventListener("change", (e) => {
    state.viewDate = e.target.value;
    loadSchedule();
  });
  $("prev-day").addEventListener("click", () => {
    state.viewDate = shiftDate(state.viewDate, -1);
    $("view-date").value = state.viewDate;
    loadSchedule();
  });
  $("next-day").addEventListener("click", () => {
    state.viewDate = shiftDate(state.viewDate, 1);
    $("view-date").value = state.viewDate;
    loadSchedule();
  });
  $("today-btn").addEventListener("click", () => {
    state.viewDate = todayISO();
    $("view-date").value = state.viewDate;
    loadSchedule();
  });

  $("room-filter").addEventListener("change", loadSchedule);
  $("submit-btn").addEventListener("click", submitBooking);

  for (const id of ["f-room", "f-date", "f-start", "f-end"]) {
    $(id).addEventListener("change", liveConflictCheck);
  }

  loadRooms().then(loadSchedule);
}

document.addEventListener("DOMContentLoaded", init);
