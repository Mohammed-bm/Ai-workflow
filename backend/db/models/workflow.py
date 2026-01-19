from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from db.base import Base 

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    nodes = Column(JSON, nullable=False)
    edges = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())