from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.extensions.db.db_postgres import Base

class PermType(str, enum.Enum):
    VIEW = "VIEW"
    EDIT = "EDIT"

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    perm_type = Column(Enum(PermType), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="permissions")

    __table_args__ = ({"unique_constraint": ["list_id", "user_id"]},)