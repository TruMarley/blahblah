#!/bin/bash
set -e

echo ""
echo "═══════════════════════════════════════════"
echo "   Voice AI Receptionist — Setup"
echo "═══════════════════════════════════════════"
echo ""

# Install deps
echo "▶ Installing Python dependencies..."
pip install -r requirements.txt

# Copy .env if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "▶ Created .env — fill in your API keys"
else
    echo "▶ .env already exists"
fi

# Install ngrok if not present
if ! command -v ngrok &> /dev/null; then
    echo ""
    echo "▶ ngrok not found. Install it from https://ngrok.com/download"
    echo "  (needed to expose your local server to Twilio)"
else
    echo "▶ ngrok found: $(ngrok version)"
fi

echo ""
echo "═══════════════════════════════════════════"
echo "   NEXT STEPS"
echo "═══════════════════════════════════════════"
echo ""
echo "1. Fill in your API keys in .env"
echo "   - ANTHROPIC_API_KEY  → https://console.anthropic.com"
echo "   - DEEPGRAM_API_KEY   → https://console.deepgram.com"
echo "   - TWILIO_*           → https://console.twilio.com"
echo ""
echo "2. Edit config.py with your business info"
echo ""
echo "3. Start the server:"
echo "   python server.py"
echo ""
echo "4. In another terminal, expose it with ngrok:"
echo "   ngrok http 5050"
echo ""
echo "5. In Twilio console, set your phone number's"
echo "   Voice webhook to:"
echo "   https://YOUR-NGROK-URL.ngrok.io/incoming-call"
echo ""
echo "6. Call your Twilio number and talk to your AI!"
echo ""
echo "7. View booked appointments at:"
echo "   http://localhost:5050"
echo ""
