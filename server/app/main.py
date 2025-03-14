from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.gateway import router as gateway_router

app = FastAPI(title="Система управления рассылками")

# Register gateway router
app.include_router(gateway_router, prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def root() -> str:
    return "Mailing System!"
