from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Include routers
from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as user_router

app = FastAPI(title="Auth Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
