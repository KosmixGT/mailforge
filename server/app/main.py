from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database.base import Base, engine
from app.api.v1 import mailing, user, recipient, address, history, smtp, telegram, auth


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(title="Система управления рассылками", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 routers
app.include_router(mailing.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(recipient.router, prefix="/api/v1")
app.include_router(address.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
app.include_router(smtp.router, prefix="/api/v1")
app.include_router(telegram.router, prefix="/api/v1")


@app.get("/", tags=["root"])
async def root():
    return {"message": "Mailing System API"}
