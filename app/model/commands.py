from sqlalchemy import Column, Float, VARCHAR, TIMESTAMP, Integer
from database.session import Base

class Command(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True, index=True)
    id_customers = Column(Integer)
    id_product = Column(Integer)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    
    class Config:
        from_attributes__ = True