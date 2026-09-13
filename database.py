from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
if __name__ == "__main__":
    import models
    print("Connecting to:", engine.url)
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    from sqlalchemy import inspect
    inspector = inspect(engine)
    print("Tables visible to SQLAlchemy:", inspector.get_table_names())