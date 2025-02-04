from fastapi import FastAPI
from app.database import Base, engine
from app.user.routes import router as user_router
from app.mailing.routes import router as mailing_router
from app.recipient.routes import router as recipient_router
from app.address.routes import router as address_router
from app.smtpmailing import router as smtpmailing_router
from app.tgmailing import router as tgmailing_router
from app.history.routes import router as history_router
from app.user.authorization import router as authorization_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Система управления рассылками")
Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/api")
app.include_router(authorization_router, prefix="/api")
app.include_router(mailing_router, prefix="/api")
app.include_router(recipient_router, prefix="/api")
app.include_router(address_router, prefix="/api")
app.include_router(smtpmailing_router, prefix="/api")
app.include_router(tgmailing_router, prefix="/api")
app.include_router(history_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', tags=["root"])
async def root():
    return "Hello World!"

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)