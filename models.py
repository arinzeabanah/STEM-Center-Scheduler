# STEM Center Scheduler

A web-based scheduling system built for the **Tallahassee State College STEM Center**. Staff and students can reserve rooms, and the system automatically detects scheduling conflicts, suggests open time slots, mirrors bookings to a shared Google Calendar, and emails confirmations.

**Stack:** Python (Flask, SQLAlchemy) · JavaScript (vanilla) · Google Calendar API · SQLite

## Features

- **Room booking** for the STEM Center's tutoring labs, computer lab, study rooms, and conference room
- **Automated conflict detection** — overlapping bookings for the same room are caught before they're saved, both live in the form and again server-side on submission
- **Smart slot suggestions** — when a conflict is found, the system proposes the nearest open slots of the same duration within operating hours (8 AM–9 PM)
- **Google Calendar sync** — bookings are mirrored to a shared calendar with reminders and the organizer added as an attendee
- **Email notifications** — confirmation and cancellation emails via SMTP
- **Daily schedule view** with room filtering and day-by-day navigation

## Quick start

```bash
git clone https://github.com/<your-username>/stem-center-scheduler.git
cd stem-center-scheduler

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open http://localhost:5000. The app runs fully out of the box with a local SQLite database — Google Calendar sync and email are optional and turn on automatically once configured (below).

## Configuration

Copy the example env file and fill in what you need:

```bash
cp .env.example .env
```

### Google Calendar API (optional)

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/) and enable the **Google Calendar API**.
2. Create a **service account**, generate a JSON key, and save it as `credentials.json` in the project root.
3. In Google Calendar, share the STEM Center calendar with the service account's email address (give it "Make changes to events" access).
4. Set `GOOGLE_CALENDAR_ID` in `.env` to that calendar's ID (found under calendar settings → "Integrate calendar").

Bookings will now appear on the shared calendar with a 60-minute email reminder and a 15-minute popup reminder.

### Email notifications (optional)

Set the `SMTP_*` variables in `.env`. Without them, the app logs the email content to the console instead of sending, which is handy for development.

## How conflict detection works

Two bookings conflict when they're in the same room and their time intervals overlap:

```
a.start < b.end  AND  b.start < a.end
```

Comparisons are strict, so back-to-back bookings (one ends exactly when the next begins) are allowed. When a conflict is found, the detector searches forward and then backward from the requested time in 30-minute increments to suggest up to three open slots of the same duration on the same day.

The check runs twice: once live in the browser as the user fills out the form (`POST /api/check-conflicts`), and again authoritatively on the server when the booking is submitted, so race conditions between two users can't slip a double-booking through.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/rooms` | List all rooms |
| `GET` | `/api/events?date=YYYY-MM-DD&room_id=N` | List events, with optional filters |
| `POST` | `/api/events` | Create a booking (returns `409` with conflict details if the slot is taken) |
| `DELETE` | `/api/events/<id>` | Cancel a booking |
| `POST` | `/api/check-conflicts` | Check a time slot and get alternative suggestions |

## Running tests

```bash
pip install pytest
python -m pytest
```

## Project structure

```
stem-center-scheduler/
├── app.py                        # Flask app and API routes
├── config.py                     # Environment-based configuration
├── scheduler/
│   ├── models.py                 # Room and Event models (SQLAlchemy)
│   ├── conflict_detector.py      # Overlap detection + slot suggestions
│   ├── calendar_service.py       # Google Calendar API integration
│   └── notifications.py          # SMTP email confirmations
├── static/
│   ├── css/style.css
│   └── js/app.js                 # Frontend: schedule view, live conflict checks
├── templates/
│   └── index.html
└── tests/
    └── test_conflict_detector.py
```

## License

MIT
