import os, httpx

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API = os.getenv("TELEGRAM_API", "https://api.telegram.org")

async def send(text: str):
    if not TOKEN or not CHAT_ID:
        print("[alert]", text)   # no Telegram configured: just print
        return
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            f"{API}/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
        )
