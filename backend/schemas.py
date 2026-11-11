from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class LoginInput(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"
    roll_no: Optional[str] = None
    department: str = "CSE"
    semester: str = ""

class CourseCreate(BaseModel):
    code: str
    name: str
    faculty_id: Optional[int] = None
    semester: str = ""

class SessionCreate(BaseModel):
    course_id: int
    duration_minutes: int = 10

class ManualAttendance(BaseModel):
    student_id: int
    status: str = "present"

class TimetableCreate(BaseModel):
    course_id: int
    day_of_week: str
    start_time: str
    end_time: str
    room: str = ""

class LeaveCreate(BaseModel):
    start_date: str
    end_date: str
    reason: str

class LeaveReview(BaseModel):
    status: str
    reviewer_note: str = ""

class AnnouncementCreate(BaseModel):
    title: str
    body: str
    audience: str = "all"


class StudentRegister(BaseModel):
    name: str
    email: str
    password: str
    roll_no: str
    department: str = "CSE"
    semester: str = ""
