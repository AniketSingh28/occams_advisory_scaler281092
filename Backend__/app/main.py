# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, onboard


app = FastAPI(title="Occams Onboard API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


app.include_router(onboard.router, prefix="/onboard")
app.include_router(chat.router, prefix="/chat")


@app.get("/health")
async def health():
    return {"status": "ok"}