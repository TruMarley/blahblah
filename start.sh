#!/bin/bash
# RingDesk startup script
# Usage: ./start.sh [--reload]

set -e

# Load .env if it exists
if [ -f .env ]; then
  set -a
  source .env
  set +a
  echo "✓ Loaded .env"
else
  echo "⚠ No .env found — copy .env.example to .env and fill in your credentials"
  echo "  cp .env.example .env"
  exit 1
fi

# Check required vars
missing=0
for var in TWILIO_ACCOUNT_SID TWILIO_AUTH_TOKEN TWILIO_PHONE_NUMBER OPENAI_API_KEY; do
  if [ -z "${!var}" ] || [[ "${!var}" == *"..."* ]] || [[ "${!var}" == *"xxx"* ]]; then
    echo "⚠ $var not set in .env"
    missing=1
  else
    echo "✓ $var"
  fi
done

if [ $missing -eq 1 ]; then
  echo ""
  echo "→ Visit http://localhost:${PORT:-5050}/twilio-setup for setup instructions"
fi

PORT=${PORT:-5050}
HOST=${HOST:-0.0.0.0}

echo ""
echo "Starting RingDesk on http://${HOST}:${PORT}"
echo "Dashboard: http://localhost:${PORT}/dashboard"
echo ""

if [ "$1" == "--reload" ]; then
  exec uvicorn server:app --host "$HOST" --port "$PORT" --reload
else
  exec uvicorn server:app --host "$HOST" --port "$PORT"
fi
