"""
Business configuration — edit this file to customize for your business.
"""

BUSINESS = {
    "name": "Cuts & Fades Barbershop",
    "type": "barbershop",          # barbershop | nail_salon | salon | spa
    "phone": "(555) 123-4567",
    "address": "123 Main Street, Miami FL 33101",
    "website": "cutsandfades.com",
    "owner_phone": "+13055550000",   # ← owner's cell for live transfers

    # Business hours (24h format). Set to None to mark as closed.
    "hours": {
        "monday":    {"open": "09:00", "close": "19:00"},
        "tuesday":   {"open": "09:00", "close": "19:00"},
        "wednesday": {"open": "09:00", "close": "19:00"},
        "thursday":  {"open": "09:00", "close": "19:00"},
        "friday":    {"open": "09:00", "close": "20:00"},
        "saturday":  {"open": "08:00", "close": "18:00"},
        "sunday":    None,  # closed
    },

    # Services offered with duration (minutes) and price
    "services": [
        {"name": "Men's Haircut",         "duration": 30, "price": 25},
        {"name": "Kids Haircut",          "duration": 20, "price": 18},
        {"name": "Beard Trim",            "duration": 20, "price": 15},
        {"name": "Haircut + Beard",       "duration": 45, "price": 35},
        {"name": "Shape Up / Edge Up",    "duration": 20, "price": 15},
        {"name": "Hot Towel Shave",       "duration": 30, "price": 30},
        {"name": "Fade",                  "duration": 30, "price": 25},
    ],

    # Staff (barbers/stylists)
    "staff": [
        {"name": "Marcus",  "specialties": ["fades", "designs"]},
        {"name": "Diego",   "specialties": ["beards", "hot towel shave"]},
        {"name": "Jordan",  "specialties": ["kids cuts", "scissor work"]},
    ],

    # Appointment slot interval (minutes)
    "slot_interval": 15,

    # How far in advance can someone book (days)
    "booking_window_days": 14,

    # Policies / FAQ
    "policies": {
        "walk_ins": True,
        "walk_in_note": "Walk-ins are welcome but appointments are recommended to reduce wait time.",
        "cancellation": "Please cancel at least 2 hours before your appointment.",
        "late_policy": "If you're more than 10 minutes late your slot may be given away.",
        "payment": "We accept cash, Venmo, Zelle, and all major credit cards.",
        "parking": "Free parking available in the lot next to the shop.",
    },

    # AI voice personality
    "ai_name": "Alex",
    "ai_voice_id": "aura-asteria-en",   # Deepgram TTS voice
    "greeting": "Thanks for calling {business_name}! I'm Alex, your AI assistant. I can answer questions and book appointments for you. How can I help?",
}


# ── Nail Salon Example (uncomment to use) ──────────────────────────────────
# BUSINESS = {
#     "name": "Luxe Nail Spa",
#     "type": "nail_salon",
#     "phone": "(555) 987-6543",
#     "address": "456 Brickell Ave, Miami FL 33131",
#     "hours": {
#         "monday":    {"open": "10:00", "close": "19:00"},
#         "tuesday":   {"open": "10:00", "close": "19:00"},
#         "wednesday": {"open": "10:00", "close": "19:00"},
#         "thursday":  {"open": "10:00", "close": "19:00"},
#         "friday":    {"open": "10:00", "close": "20:00"},
#         "saturday":  {"open": "09:00", "close": "18:00"},
#         "sunday":    {"open": "11:00", "close": "17:00"},
#     },
#     "services": [
#         {"name": "Classic Manicure",     "duration": 30, "price": 25},
#         {"name": "Gel Manicure",         "duration": 45, "price": 40},
#         {"name": "Classic Pedicure",     "duration": 45, "price": 35},
#         {"name": "Gel Pedicure",         "duration": 60, "price": 55},
#         {"name": "Mani + Pedi Combo",    "duration": 75, "price": 70},
#         {"name": "Acrylic Full Set",     "duration": 60, "price": 50},
#         {"name": "Acrylic Fill",         "duration": 45, "price": 35},
#         {"name": "Nail Art (per nail)",  "duration": 5,  "price": 5},
#     ],
#     "staff": [
#         {"name": "Lily",  "specialties": ["nail art", "acrylics"]},
#         {"name": "Nina",  "specialties": ["gel", "pedicures"]},
#         {"name": "Tina",  "specialties": ["manicures", "combos"]},
#     ],
#     "slot_interval": 15,
#     "booking_window_days": 14,
#     "policies": {
#         "walk_ins": True,
#         "walk_in_note": "Walk-ins welcome, appointments preferred on weekends.",
#         "cancellation": "Cancel 24 hours in advance please.",
#         "payment": "Cash, Venmo, Zelle, and all major credit cards accepted.",
#         "parking": "Street parking available.",
#     },
#     "ai_name": "Sophia",
#     "ai_voice_id": "aura-asteria-en",
#     "greeting": "Thank you for calling {business_name}! I'm Sophia, your AI assistant. How can I help you today?",
# }
