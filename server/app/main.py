from fastapi import FastAPI
from database import Base, engine
from user.routes import router as user_router
from mailing.routes import router as mailing_router
from recipient.routes import router as recipient_router
from address.routes import router as address_router
from smtpmailing import router as smtpmailing_router
from user.authorization import router as authorization_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from user.schemas import Settings

app = FastAPI(title="Система управления рассылками")
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(authorization_router)
app.include_router(mailing_router)
app.include_router(recipient_router)
app.include_router(address_router)
app.include_router(smtpmailing_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], #allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create initialized database table
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@AuthJWT.load_config
def get_config():
    return Settings()

@app.get('/', tags=["root"])
async def root():
    return "Hello World!"

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)