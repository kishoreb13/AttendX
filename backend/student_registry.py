"""Separate SQLite store for student self-registration profile records.

Authentication credentials remain in attendx.db; this database stores a
separate student-registration profile/audit record without plaintext passwords.
"""
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_PATH = Path(__file__).resolve().parent / "student_registry.db"
engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}", connect_args={"check_same_thread": False})
RegistrySession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RegistryBase(DeclarativeBase):
    pass

class StudentRegistration(RegistryBase):
    __tablename__ = "student_registrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, nullable=False, index=True)
    roll_no = Column(String(40), unique=True, nullable=False, index=True)
    department = Column(String(100), default="CSE")
    semester = Column(String(20), default="")
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

RegistryBase.metadata.create_all(bind=engine)
