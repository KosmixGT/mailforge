from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://uoognc3we7m8fex8zn9b:yF7GoBpVaphGxFaXZpoeL9ixj6dFw2@bxml7wtus4yekwz4icln-postgresql.services.clever-cloud.com:50013/bxml7wtus4yekwz4icln'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()