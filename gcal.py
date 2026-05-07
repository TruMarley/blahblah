"""
Google Calendar integration — optional module.
Set GOOGLE_CREDENTIALS_FILE in .env to enable.
Without credentials, all functions are no-ops that return gracefully.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional

log = logging.getLogger("voice_ai.gcal")

CREDENTIALS_FILE = os.environ.get("GOOGLE_CREDENTIALS_FILE", "")
TOKEN_FILE = "gcal_token.json"

_service = None


def _get_service():
    global _service
    if _service:
        return _service
    if not CREDENTIALS_FILE or not os.path.exists(CREDENTIALS_FILE):
        return None

    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None

        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as f:
                f.write(creds.to_json())

        _service = build("calendar", "v3", credentials=creds)
        log.info("Google Calendar connected")
        return _service

    except ImportError:
        log.warning("google-api-python-client not installed — Calendar sync disabled")
        return None
    except Exception as e:
        log.error(f"Google Calendar init error: {e}")
        return None


def add_event(
    name: str,
    service_name: str,
    date_str: str,
    time_str: str,
    duration_minutes: int,
    staff: Optional[str] = None,
    phone: Optional[str] = None,
    calendar_id: str = "primary",
) -> Optional[str]:
    """
    Create a Google Calendar event for the appointment.
    Returns the event URL or None if unavailable.
    """
    svc = _get_service()
    if not svc:
        return None

    try:
        start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(minutes=duration_minutes)

        staff_note = f" with {staff}" if staff else ""
        phone_note = f"\nPhone: {phone}" if phone else ""

        event = {
            "summary": f"{name} — {service_name}{staff_note}",
            "description": f"Booked via RingDesk AI Receptionist\nClient: {name}{phone_note}",
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": os.environ.get("TIMEZONE", "America/New_York"),
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": os.environ.get("TIMEZONE", "America/New_York"),
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 60},
                    {"method": "popup", "minutes": 15},
                ],
            },
            "colorId": "2",  # sage green
        }

        result = svc.events().insert(calendarId=calendar_id, body=event).execute()
        url = result.get("htmlLink")
        log.info(f"Google Calendar event created: {url}")
        return url

    except Exception as e:
        log.error(f"Google Calendar event creation failed: {e}")
        return None


def delete_event(event_id: str, calendar_id: str = "primary") -> bool:
    svc = _get_service()
    if not svc:
        return False
    try:
        svc.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return True
    except Exception as e:
        log.error(f"Google Calendar delete failed: {e}")
        return False


def is_connected() -> bool:
    return _get_service() is not None
