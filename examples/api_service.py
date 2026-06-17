"""A minimal FastAPI service — a health check and a read-only inventory lookup.

Read-only by default: this serves facts, it doesn't mutate anything. Typed responses and a
real 404 instead of a 200 with an error body.

    pip install "fastapi[standard]"
    uvicorn api_service:app --reload
    curl localhost:8000/healthz
"""
from fastapi import FastAPI, HTTPException

app = FastAPI(title="lab-inventory", version="0.1.0")

_INVENTORY = {
    "leaf-01": {"role": "leaf", "site": "lab"},
    "spine-01": {"role": "spine", "site": "lab"},
}


@app.get("/healthz")
def healthz() -> dict:
    """Liveness probe — cheap, dependency-free, always answerable."""
    return {"status": "ok"}


@app.get("/devices/{name}")
def device(name: str) -> dict:
    if name not in _INVENTORY:
        raise HTTPException(status_code=404, detail="unknown device")
    return _INVENTORY[name]
