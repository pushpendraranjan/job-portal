from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base #, relationship
Base = declarative_base()


data = "postgresql://company:root@localhost:5433/job_portal_db"

engine = create_engine(data)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
