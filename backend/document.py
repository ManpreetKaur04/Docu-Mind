from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base  # Importing Base from database.py

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    filepath = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    text_content = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "upload_date": self.upload_date.isoformat(),
        }
