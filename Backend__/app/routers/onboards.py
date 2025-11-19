# backend/app/routers/onboard.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import json, os, re

router = APIRouter()
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "users.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

phone_re = re.compile(r"^\+?[0-9 \-]{7,20}$")


class OnboardIn(BaseModel):
    name: str
    email: EmailStr
    phone: str


@router.post("/submit")
async def submit(info: OnboardIn):
    if not phone_re.match(info.phone):
        raise HTTPException(status_code=400, detail="invalid phone")

    # store locally
    users = []
    if os.path.exists(DATA_FILE):
        users = json.load(open(DATA_FILE, encoding="utf8"))

    users.append({
        "name": info.name,
        "email": info.email,
        "phone": info.phone
    })

    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(users, f, indent=2)

    return {"status": "ok"}
