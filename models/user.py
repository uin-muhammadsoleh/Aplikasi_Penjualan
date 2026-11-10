from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from database.db import Base


class User(Base):
    """Model/tabel pengguna (user) pada database."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nama_lengkap = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username!r})"
