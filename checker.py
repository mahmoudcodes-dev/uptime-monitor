import time, httpx
import db, alerts

async def check_one(client: httpx.AsyncClient, m: dict):
    start = time.perf_counter()
    try:
        r = await client.get(m["url"], follow_redirects=True)
        code = r.status_code
        status = "up" if code < 400 else "down"
    except httpx.HTTPError:
        code, status = None, "down"
    latency = int((time.perf_counter() - start) * 1000)
    db.update(m["id"], status, code, latency)

    previous = m["status"]
    if status == "down" and previous != "down":
        await alerts.send(f"DOWN: {m['url']} (status {code})")
    elif status == "up" and previous == "down":
        await alerts.send(f"RECOVERED: {m['url']} ({latency} ms)")

async def check_all():
    async with httpx.AsyncClient(timeout=8) as client:
        for m in db.all_monitors():
            await check_one(client, m)
