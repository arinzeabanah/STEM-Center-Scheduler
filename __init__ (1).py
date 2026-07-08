"""
Google Calendar API integration.

Uses a service account (``credentials.json``) to create and delete events
on the STEM Center's shared calendar. If credentials are not configured,
every method degrades to a no-op so the app still runs locally — the
event simply isn't mirrored to Google Calendar.

Setup (see README for full steps):
    1. Create a Google Cloud project and enable the Calendar API.
    2. Create a service account and download its JSON key as
       ``credentials.json`` in the project root.
    3. Share the target Google Calendar with the service account's email
       and set GOOGLE_CALENDAR_ID in your .env file.
"""

import logging
import os

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TIMEZONE = "America/New_York"  # Tallahassee, FL


class CalendarService:
    def __init__(self, credentials_file=None, calendar_id=None):
        self.credentials_file = credentials_file or os.getenv(
            "GOOGLE_CREDENTIALS_FILE", "credentials.json"
        )
        self.calendar_id = calendar_id or os.getenv("GOOGLE_CALENDAR_ID", "primary")
        self.service = self._build_service()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _build_service(self):
        """Build the Calendar API client, or return None if unconfigured."""
        if not os.path.exists(self.credentials_file):
            logger.info(
                "Google credentials not found (%s) — running without "
                "Calendar sync.", self.credentials_file
            )
            return None
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            creds = service_account.Credentials.from_service_account_file(
                self.credentials_file, scopes=SCOPES
            )
            return build("calendar", "v3", credentials=creds,
                         cache_discovery=False)
        except Exception:
            logger.exception("Failed to initialize Google Calendar client.")
            return None

    @property
    def enabled(self):
        return self.service is not None

    # ------------------------------------------------------------------
    # Operations
    # ------------------------------------------------------------------

    def create_event(self, event):
        """Mirror a local Event to Google Calendar. Returns the Google
        event id, or None if sync is disabled or fails."""
        if not self.enabled:
            return None

        body = {
            "summary": f"[STEM Center] {event.title}",
            "description": (
                f"{event.description}\n\n"
                f"Room: {event.room.name}\n"
                f"Organizer: {event.organizer_name} "
                f"<{event.organizer_email}>"
            ),
            "location": f"STEM Center — {event.room.name}",
            "start": {"dateTime": event.start_time.isoformat(),
                      "timeZone": TIMEZONE},
            "end": {"dateTime": event.end_time.isoformat(),
                    "timeZone": TIMEZONE},
            "attendees": [{"email": event.organizer_email}],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 60},
                    {"method": "popup", "minutes": 15},
                ],
            },
        }
        try:
            created = (
                self.service.events()
                .insert(calendarId=self.calendar_id, body=body)
                .execute()
            )
            logger.info("Created Google Calendar event %s", created.get("id"))
            return created.get("id")
        except Exception:
            logger.exception("Google Calendar insert failed.")
            return None

    def delete_event(self, event):
        """Remove the mirrored Google Calendar event, if one exists."""
        if not self.enabled or not event.google_event_id:
            return False
        try:
            self.service.events().delete(
                calendarId=self.calendar_id, eventId=event.google_event_id
            ).execute()
            return True
        except Exception:
            logger.exception("Google Calendar delete failed.")
            return False
