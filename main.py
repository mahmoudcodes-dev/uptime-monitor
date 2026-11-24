import asyncio, os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import db, checker

INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

async def loop():
    while True:
        await checker.check_all()
        await asyncio.sleep(INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init()
    task = asyncio.create_task(loop())
    yield
    task.cancel()

app = FastAPI(title="Uptime Monitor", lifespan=lifespan)

class NewMonitor(BaseModel):
    url: HttpUrl

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/monitors", status_code=201)
async def add_monitor(body: NewMonitor):
    try:
        monitor_id = db.add(str(body.url))
    except Exception:
        raise HTTPException(409, "URL already monitored")
    return {"id": monitor_id, "watching": str(body.url)}

@app.get("/monitors")
async def list_monitors():
    return db.all_monitors()

@app.delete("/monitors/{monitor_id}")
async def delete_monitor(monitor_id: int):
    if not db.remove(monitor_id):
        raise HTTPException(404, "Not found")
    return {"deleted": monitor_id}
