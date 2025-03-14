from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Include routers
from app.api.v1.history import router as history_router

app = FastAPI(title="History Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(history_router, prefix="/api/v1")
