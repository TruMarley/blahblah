"""
Claude-powered voice agent.
Features: booking, Q&A, Spanish bilingual, live transfer, callback requests.
"""

import json
import anthropic
from datetime import datetime, date, timedelta
from typing import Optional
from config import BUSINESS
from appointments import (
    get_available_slots, book_appointment, get_upcoming_appointments, add_callback
)

client = anthropic.Anthropic()

# Languages we support for bilingual detection
SUPPORTED_LANGUAGES = {"en": "English", "es": "Spanish"}


def detect_language(text: str) -> str:
    """Simple Spanish detection — check for common Spanish words/patterns."""
    spanish_markers = [
        "hola", "buenos", "cita", "quiero", "necesito", "hablar", "español",
        "por favor", "gracias", "cuánto", "cuanto", "cuando", "dónde", "donde",
        "qué", "que", "hora", "precio", "servicio", "reservar", "corte",
        "puedo", "tienes", "tienen", "cómo", "como", "sí", "si"
    ]
    lower = text.lower()
    hits = sum(1 for w in spanish_markers if w in lower)
    return "es" if hits >= 2 else "en"


def build_system_prompt(config: dict, language: str = "en") -> str:
    cfg = config or BUSINESS

    services_text = "\n".join(
        f"  - {s['name']}: ${s['price']}, {s['duration']} min"
        for s in cfg["services"]
    )

    hours_lines = []
    for day, h in cfg["hours"].items():
        if h:
            hours_lines.append(f"  - {day.capitalize()}: {h['open']} - {h['close']}")
        else:
            hours_lines.append(f"  - {day.capitalize()}: Closed")
    hours_text = "\n".join(hours_lines)

    staff_text = ", ".join(
        f"{s['name']} ({', '.join(s['specialties'])})"
        for s in cfg.get("staff", [])
    )

    policies = cfg.get("policies", {})
    policy_lines = []
    if policies.get("walk_ins"):
        policy_lines.append(f"Walk-ins: {policies.get('walk_in_note', 'Welcome')}")
    if policies.get("cancellation"):
        policy_lines.append(f"Cancellation: {policies['cancellation']}")
    if policies.get("payment"):
        policy_lines.append(f"Payment: {policies['payment']}")
    if policies.get("parking"):
        policy_lines.append(f"Parking: {policies['parking']}")

    today = date.today().strftime("%A, %B %d, %Y")

    lang_instruction = ""
    if language == "es":
        lang_instruction = """
LANGUAGE: The caller is speaking Spanish. Respond ENTIRELY in Spanish.
Be warm and natural — speak like a native Spanish-speaking receptionist.
All booking confirmations, questions, and responses must be in Spanish."""

    transfer_tool_desc = f"""
LIVE TRANSFER: If the caller says they have an emergency, urgent issue, or explicitly asks
to speak with a real person or the owner, use the request_live_transfer tool immediately.
The owner's number is {cfg.get('owner_phone', 'on file')}."""

    return f"""You are {cfg['ai_name']}, a friendly AI receptionist for {cfg['name']}.
Today is {today}.
{lang_instruction}

YOUR ROLE:
- Answer questions about the business (hours, services, prices, location, policies)
- Book appointments — we accept multi-service bookings ("cut AND beard trim")
- Keep responses SHORT and conversational — this is a PHONE CALL
- Speak naturally, like a real receptionist
- Never use markdown, bullet points, or formatting
- Keep each response under 3 sentences when possible
- After booking, always mention that a confirmation text is being sent to their phone

BUSINESS INFO:
Name: {cfg['name']}
Phone: {cfg['phone']}
Address: {cfg['address']}

SERVICES (callers can book multiple):
{services_text}

HOURS:
{hours_text}

STAFF: {staff_text}
- If caller requests a specific barber/stylist, honor that preference
- If no preference, assign based on availability

POLICIES:
{chr(10).join(policy_lines)}

BOOKING PROCESS:
1. Ask what service(s) they want — they can book multiple in one call
2. Ask preferred date
3. Check availability using check_availability tool
4. Ask preferred time from available slots
5. Get their name and callback phone number
6. Confirm all details verbally
7. Use book_appointment tool to finalize
8. Tell them a confirmation text is on the way
{transfer_tool_desc}

UPSELL (natural, never pushy):
After confirming a booking for a single service, use suggest_upsell ONCE to offer a natural add-on:
- Haircut → offer Beard Trim ("Since you're coming in, want me to add a beard trim? Only $15 more.")
- Fade → offer Shape Up ("Want a shape up to go with that? Only $15 and it only adds 20 minutes.")
- Manicure → offer Gel upgrade ("We can do gel instead for $15 more — lasts 3 weeks. Want to upgrade?")
Only suggest if it genuinely pairs well. Skip if they already booked multiple services.

CALLBACK REQUESTS:
If someone says "have someone call me back", "I'll call back later", or just wants to leave a message,
use the request_callback tool to log it so the owner is notified.

REMINDERS: After booking, mention: "You'll also get a reminder text the day before and 2 hours before — so you won't forget."

TONE: Warm, helpful, professional. Brief — they're on a phone call.
Never make up information. If unsure, offer a callback."""


TOOLS = [
    {
        "name": "check_availability",
        "description": "Check available appointment slots for a given date and service.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format, or 'today'/'tomorrow'/'saturday' etc.",
                },
                "service": {
                    "type": "string",
                    "description": "Service name from the business services list.",
                },
            },
            "required": ["date", "service"],
        },
    },
    {
        "name": "book_appointment",
        "description": "Finalize and book an appointment after all details are confirmed with the caller.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name":    {"type": "string", "description": "Caller's full name"},
                "phone":   {"type": "string", "description": "Caller's phone number for SMS confirmation"},
                "service": {"type": "string", "description": "Service being booked"},
                "date":    {"type": "string", "description": "Date in YYYY-MM-DD format"},
                "time":    {"type": "string", "description": "Time in HH:MM (24h) format"},
                "staff":   {"type": "string", "description": "Preferred staff member (optional)"},
                "notes":   {"type": "string", "description": "Any special notes or requests"},
            },
            "required": ["name", "phone", "service", "date", "time"],
        },
    },
    {
        "name": "lookup_appointments",
        "description": "Look up a caller's existing appointments by phone number.",
        "input_schema": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "Caller's phone number"},
            },
            "required": ["phone"],
        },
    },
    {
        "name": "request_callback",
        "description": "Log a callback request when a caller wants to be called back or leave a message.",
        "input_schema": {
            "type": "object",
            "properties": {
                "phone":  {"type": "string", "description": "Caller's phone number"},
                "name":   {"type": "string", "description": "Caller's name if provided"},
                "reason": {"type": "string", "description": "Why they're calling / what they need"},
            },
            "required": ["phone"],
        },
    },
    {
        "name": "request_live_transfer",
        "description": "Initiate a live transfer to the owner/staff when caller has an emergency or insists on speaking with a person.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string", "description": "Why the caller needs to speak with someone live"},
            },
            "required": ["reason"],
        },
    },
    {
        "name": "suggest_upsell",
        "description": "Suggest a complementary add-on service when caller has booked a base service. Call this ONCE after booking to offer a natural upsell. Only if it genuinely makes sense — don't push if they already booked multiple services.",
        "input_schema": {
            "type": "object",
            "properties": {
                "booked_service": {"type": "string", "description": "The service they just booked"},
                "suggested_service": {"type": "string", "description": "The add-on to suggest"},
                "reason": {"type": "string", "description": "Brief natural reason why it pairs well"},
            },
            "required": ["booked_service", "suggested_service", "reason"],
        },
    },
]


def resolve_date(date_str: str) -> str:
    """Resolve relative date strings to YYYY-MM-DD."""
    today = date.today()
    s = date_str.lower().strip()
    if s == "today":
        return today.isoformat()
    if s == "tomorrow":
        return (today + timedelta(days=1)).isoformat()
    day_map = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6,
    }
    for day_name, weekday in day_map.items():
        if day_name in s:
            days_ahead = (weekday - today.weekday()) % 7 or 7
            return (today + timedelta(days=days_ahead)).isoformat()
    return date_str  # assume already YYYY-MM-DD


def process_tool_call(tool_name: str, tool_input: dict, config: dict, call_sid: str = "") -> str:
    cfg = config or BUSINESS

    if tool_name == "check_availability":
        date_str = resolve_date(tool_input["date"])
        slots = get_available_slots(date_str, tool_input["service"], cfg)

        if not slots:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = dt.strftime("%A").lower()
            if not cfg["hours"].get(day_name):
                return json.dumps({"available": False, "reason": "closed", "date": date_str,
                                   "date_formatted": dt.strftime("%A, %B %d")})
            return json.dumps({"available": False, "reason": "fully_booked", "date": date_str,
                               "date_formatted": dt.strftime("%A, %B %d"), "slots": []})

        def fmt_time(t):
            return datetime.strptime(t, "%H:%M").strftime("%-I:%M %p")

        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return json.dumps({
            "available": True,
            "date": date_str,
            "date_formatted": dt.strftime("%A, %B %d"),
            "slots": slots[:8],
            "slots_formatted": [fmt_time(s) for s in slots[:8]],
        })

    elif tool_name == "book_appointment":
        date_str = resolve_date(tool_input["date"])
        result = book_appointment(
            name=tool_input["name"],
            phone=tool_input["phone"],
            service=tool_input["service"],
            date_str=date_str,
            time_str=tool_input["time"],
            staff=tool_input.get("staff"),
            config=cfg,
            notes=tool_input.get("notes", ""),
        )
        # Signal to server to send SMS after this tool call
        if result["success"]:
            result["_send_sms"] = True
        return json.dumps(result)

    elif tool_name == "lookup_appointments":
        appts = get_upcoming_appointments(tool_input["phone"])
        if not appts:
            return json.dumps({"found": False, "message": "No upcoming appointments found."})
        return json.dumps({"found": True, "appointments": appts[:3]})

    elif tool_name == "request_callback":
        cb_id = add_callback(
            name=tool_input.get("name"),
            phone=tool_input["phone"],
            reason=tool_input.get("reason", "Caller requested callback"),
            call_sid=call_sid,
        )
        return json.dumps({"success": True, "callback_id": cb_id,
                           "message": "Callback logged. The team will call you back soon."})

    elif tool_name == "request_live_transfer":
        owner_phone = cfg.get("owner_phone", "")
        return json.dumps({
            "transfer": True,
            "owner_phone": owner_phone,
            "reason": tool_input.get("reason", ""),
            "message": "Connecting you now. One moment please.",
        })

    elif tool_name == "suggest_upsell":
        booked = tool_input.get("booked_service", "")
        suggested = tool_input.get("suggested_service", "")
        # Find price of suggested service
        price = None
        for svc in cfg.get("services", []):
            if svc["name"].lower() == suggested.lower():
                price = svc["price"]
                break
        price_str = f" — only ${price}" if price else ""
        return json.dumps({
            "upsell_offered": True,
            "suggested": suggested,
            "price": price,
            "message": f"Upsell suggestion ready: {suggested}{price_str}",
        })

    return json.dumps({"error": "Unknown tool"})


def get_agent_response(
    conversation_history: list,
    config: dict = None,
    call_sid: str = "",
    language: str = "en",
) -> tuple[str, list, dict]:
    """
    Process one conversation turn.
    Returns (text_response, updated_history, metadata).
    metadata may contain: sms_details, transfer_to, callback_logged
    """
    cfg = config or BUSINESS
    system_prompt = build_system_prompt(cfg, language)
    messages = list(conversation_history)
    metadata = {}

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=system_prompt,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            text = next(
                (b.text for b in response.content if hasattr(b, "text")), ""
            )
            return text, messages, metadata

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                result_str = process_tool_call(block.name, block.input, cfg, call_sid)
                result = json.loads(result_str)

                # Capture side-effects for the server to act on
                if block.name == "book_appointment" and result.get("_send_sms"):
                    metadata["sms_details"] = result.get("details")
                    del result["_send_sms"]
                    result_str = json.dumps(result)

                if block.name == "request_live_transfer" and result.get("transfer"):
                    metadata["transfer_to"] = result.get("owner_phone")

                if block.name == "request_callback" and result.get("success"):
                    metadata["callback_logged"] = True

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_str,
                })

            messages.append({"role": "user", "content": tool_results})
            continue

        text = next(
            (b.text for b in response.content if hasattr(b, "text")), ""
        )
        return text, messages, metadata
