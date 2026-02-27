from sqlalchemy import Column, String, Text, DateTime
from app.database import Base
from datetime import datetime


class AnalysisResult(Base):

    __tablename__ = "analysis_results"

    id = Column(String(50), primary_key=True)

    file_name = Column(String(255))

    query = Column(Text)

    result = Column(Text)

    status = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)