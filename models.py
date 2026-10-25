from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import Column, BigInteger, String, DateTime
class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    id = Column(BigInteger, primary_key=True, autoincrement=False)