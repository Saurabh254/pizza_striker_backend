from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import config

engine = create_engine(config.DATABASE_URL)

SessionLocal = sessionmaker(engine)

Base = declarative_base()


def get_db():
    with SessionLocal() as db:
        yield db
