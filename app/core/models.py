from sqlalchemy import (
    Column, Integer, DateTime, func, ForeignKey, String, UniqueConstraint
)
from sqlalchemy.orm import relationship

from .config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bp_translations = relationship(
        "Translation", back_populates="bp_user",
        cascade="all, delete-orphan"
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_word = Column(String(25), nullable=False, index=True)
    translated_word = Column(String(25), nullable=False, index=True)
    bp_user = relationship("User", back_populates="bp_translations")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'original_word', name='uq_user_original_word'
        )
    )
