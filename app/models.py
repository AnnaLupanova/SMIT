from sqlalchemy import Column, Integer, Float, String, Date, UniqueConstraint
from database import Base


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String, index=True)
    rate = Column(Float)
    date = Column(Date)

    __table_args__ = (
        UniqueConstraint('date', 'cargo_type'),
    )
