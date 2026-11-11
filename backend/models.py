from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")
    roll_no = Column(String(40), unique=True, nullable=True)
    department = Column(String(100), default="CSE")
    semester = Column(String(20), default="")
    active = Column(Boolean, default=True)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    faculty_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    semester = Column(String(20), default="")
    faculty = relationship("User")

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(80), unique=True, index=True, nullable=False)
    starts_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    closed = Column(Boolean, default=False)
    course = relationship("Course")
    faculty = relationship("User")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="present")
    marked_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(20), default="qr")
    __table_args__ = (UniqueConstraint("session_id", "student_id", name="unique_session_student"),)
    student = relationship("User")
    session = relationship("AttendanceSession")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(120), nullable=False)
    detail = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class TimetableEntry(Base):
    __tablename__ = "timetable_entries"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    day_of_week = Column(String(12), nullable=False)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)
    room = Column(String(80), default="")
    course = relationship("Course")
    faculty = relationship("User")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(String(10), nullable=False)
    end_date = Column(String(10), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(20), default="pending")
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewer_note = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("User", foreign_keys=[student_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(180), nullable=False)
    body = Column(Text, nullable=False)
    audience = Column(String(20), default="all")
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author = relationship("User")
