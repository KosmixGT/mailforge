from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mailforge_shared.core.infrastructure.rabbitmq import RabbitMQQueue

# Initialize RabbitMQ
message_queue = RabbitMQQueue("amqp://guest:guest@rabbitmq:5672/")

# Startup event to connect to RabbitMQ
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await message_queue.connect()
    yield
    # Shutdown
    await message_queue.close()

app = FastAPI(title="Mailing Service", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.api.v1.mailing import router as mailing_router
from app.api.v1.recipient import router as recipient_router 
from app.api.v1.address import router as address_router 

app.include_router(mailing_router, prefix="/api/v1")
app.include_router(recipient_router, prefix="/api/v1")
app.include_router(address_router, prefix="/api/v1")
