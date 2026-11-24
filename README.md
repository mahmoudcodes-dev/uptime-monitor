# Uptime Monitor

A small uptime monitor built with FastAPI, sqlite3 and httpx. It checks your URLs on an interval and sends a Telegram alert when a site goes down or comes back. Companion code for the "Mahmoud Codes" YouTube channel (Video 1).

## Run with Docker

```bash
cp .env.example .env   # optional, add your Telegram token and chat id
docker compose up --build
```

The API is then on http://localhost:8000 (docs at /docs).

## Run without Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000
```

## API

- `GET /health`
- `POST /monitors` with `{"url": "https://example.com"}`
- `GET /monitors`
- `DELETE /monitors/{id}`

## Config (env vars)

- `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`: alerts. Leave empty to disable.
- `CHECK_INTERVAL`: seconds between checks (default 60).
- `DB_PATH`: sqlite file path.

## Note

This is a teaching example, not a production service. The Telegram alert path has not been tested against the live Telegram API.
