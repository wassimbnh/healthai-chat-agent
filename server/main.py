from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import Base, engine
from session.router import router as session_router
from message.router import router as message_router
from chat.router import router as chat_router


app = FastAPI(
    title="mama health backend",
    version="0.1.0",
    description="Backend API for the mama health chat prototype.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(session_router)
app.include_router(message_router)
app.include_router(chat_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
