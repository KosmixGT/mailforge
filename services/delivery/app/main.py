from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.queue.consumer import start_consumer
import asyncio
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

LOG = logging.getLogger(__name__)
LOG.info("DELIVERY API is starting up")

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(start_consumer())
    try:
        yield
    finally:
        consumer_task.cancel()
        await consumer_task

app = FastAPI(title="Delivery Service", log_level="trace", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.api.v1.smtp import router as smtp_router
from app.api.v1.telegram import router as telegram_router

app.include_router(smtp_router, prefix="/api/v1")
app.include_router(telegram_router, prefix="/api/v1")
