from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import secrets, qrcode, io, base64
from database import Base, engine, get_db, SessionLocal
from models import User, Course, AttendanceSession, Attendance, AuditLog, TimetableEntry, LeaveRequest, Announcement
from schemas import LoginInput, UserCreate, StudentRegister, CourseCreate, SessionCreate, ManualAttendance, TimetableCreate, LeaveCreate, LeaveReview, AnnouncementCreate
from student_registry import RegistrySession, StudentRegistration
from fastapi.middleware.cors import CORSMiddleware

SECRET_KEY = "CHANGE_THIS_SECRET_BEFORE_DEPLOYMENT_2026"
ALGORITHM = "HS256"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI(title="AttendX API", version="1.0.0", description="Smart Campus Attendance Management API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://attend-x-ruddy.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
), allow_origins = [
    "http://localhost:5173",
    "https://attend-x-ruddy.vercel.app",
]

def seed():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@attendx.edu").first():
            db.add(User(name="System Administrator", email="admin@attendx.edu", password_hash=pwd.hash("Admin@123"), role="admin", department="Administration"))
            db.commit()
    finally: db.close()
seed()

def token_for(user):
    return jwt.encode({"sub": str(user.id), "role": user.role, "exp": datetime.utcnow()+timedelta(hours=12)}, SECRET_KEY, algorithm=ALGORITHM)

def current_user(authorization: str = Header(default=""), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "): raise HTTPException(401, "Missing bearer token")
    try: payload = jwt.decode(authorization[7:], SECRET_KEY, algorithms=[ALGORITHM]); uid = int(payload["sub"])
    except (JWTError, ValueError, KeyError): raise HTTPException(401, "Invalid or expired token")
    user = db.query(User).filter(User.id == uid, User.active == True).first()
    if not user: raise HTTPException(401, "User not found or inactive")
    return user

def allow(*roles):
    def checker(user=Depends(current_user)):
        if user.role not in roles: raise HTTPException(403, "Insufficient permissions")
        return user
    return checker

def log(db, actor, action, detail=""):
    db.add(AuditLog(actor_id=actor.id if actor else None, action=action, detail=detail))

@app.get("/")
def root(): return {"message":"AttendX API is running", "docs":"/docs"}

@app.post("/api/auth/login")
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(func.lower(User.email) == data.email.lower()).first()
    if not user or not pwd.verify(data.password, user.password_hash): raise HTTPException(401, "Incorrect email or password")
    return {"access_token": token_for(user), "token_type":"bearer", "user": {"id":user.id,"name":user.name,"email":user.email,"role":user.role,"roll_no":user.roll_no}}

@app.post("/api/auth/register", status_code=201)
def register_student(data: StudentRegister, db: Session = Depends(get_db)):
    """Public self-registration. The role is always student; clients cannot set roles."""
    name = data.name.strip()
    email = data.email.strip().lower()
    roll_no = data.roll_no.strip().upper()
    department = data.department.strip() or "CSE"
    semester = data.semester.strip()
    if len(name) < 2:
        raise HTTPException(400, "Please enter your full name")
    if not email or "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        raise HTTPException(400, "Please enter a valid email address")
    if len(data.password) < 8:
        raise HTTPException(400, "Password must contain at least 8 characters")
    if not roll_no:
        raise HTTPException(400, "Roll number is required")
    if db.query(User).filter(func.lower(User.email) == email).first():
        raise HTTPException(409, "An account with this email already exists")
    if db.query(User).filter(func.upper(User.roll_no) == roll_no).first():
        raise HTTPException(409, "This roll number is already registered")

    registry = RegistrySession()
    created_user = None
    try:
        created_user = User(name=name, email=email, password_hash=pwd.hash(data.password),
                            role="student", roll_no=roll_no, department=department, semester=semester)
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
        registry.add(StudentRegistration(user_id=created_user.id, name=name, email=email,
                                          roll_no=roll_no, department=department, semester=semester))
        registry.commit()
        return {"message": "Student account created successfully. You can now sign in.",
                "user": {"id": created_user.id, "name": created_user.name,
                         "email": created_user.email, "role": "student"}}
    except Exception:
        registry.rollback()
        if created_user is not None:
            try:
                db.delete(created_user)
                db.commit()
            except Exception:
                db.rollback()
        raise HTTPException(500, "Could not complete registration. Please try again.")
    finally:
        registry.close()


@app.get("/api/auth/me")
def me(user=Depends(current_user)):
    return {"id":user.id,"name":user.name,"email":user.email,"role":user.role,"roll_no":user.roll_no,"department":user.department}

@app.post("/api/users")
def create_user(data: UserCreate, db: Session = Depends(get_db), actor=Depends(allow("admin"))):
    if data.role not in ("admin","faculty","student"): raise HTTPException(400,"Invalid role")
    if db.query(User).filter(User.email == data.email).first(): raise HTTPException(409,"Email already exists")
    if data.roll_no and db.query(User).filter(User.roll_no == data.roll_no).first(): raise HTTPException(409,"Roll number already exists")
    user=User(name=data.name,email=data.email,password_hash=pwd.hash(data.password),role=data.role,roll_no=data.roll_no,department=data.department,semester=data.semester)
    db.add(user); db.flush(); log(db,actor,"USER_CREATED",f"{user.email} ({user.role})"); db.commit()
    return {"id":user.id,"name":user.name,"email":user.email,"role":user.role}

@app.get("/api/users")
def users(role: str = "", db: Session = Depends(get_db), actor=Depends(allow("admin","faculty"))):
    q=db.query(User).filter(User.active == True)
    if role: q=q.filter(User.role==role)
    return [{"id":u.id,"name":u.name,"email":u.email,"role":u.role,"roll_no":u.roll_no,"department":u.department,"semester":u.semester} for u in q.order_by(User.name).all()]

@app.post("/api/courses")
def create_course(data: CourseCreate, db: Session = Depends(get_db), actor=Depends(allow("admin"))):
    if db.query(Course).filter(Course.code==data.code).first(): raise HTTPException(409,"Course code already exists")
    if data.faculty_id and not db.query(User).filter(User.id==data.faculty_id,User.role=="faculty").first(): raise HTTPException(400,"Faculty not found")
    c=Course(**data.model_dump()); db.add(c); db.flush(); log(db,actor,"COURSE_CREATED",c.code); db.commit()
    return {"id":c.id,"code":c.code,"name":c.name,"semester":c.semester,"faculty_id":c.faculty_id}

@app.get("/api/courses")
def courses(db: Session=Depends(get_db), actor=Depends(current_user)):
    q=db.query(Course).options(joinedload(Course.faculty))
    if actor.role=="faculty": q=q.filter(Course.faculty_id==actor.id)
    return [{"id":c.id,"code":c.code,"name":c.name,"semester":c.semester,"faculty":c.faculty.name if c.faculty else "Unassigned","faculty_id":c.faculty_id} for c in q.order_by(Course.code).all()]

@app.post("/api/sessions")
def create_session(data: SessionCreate, db: Session=Depends(get_db), actor=Depends(allow("admin","faculty"))):
    course=db.query(Course).filter(Course.id==data.course_id).first()
    if not course: raise HTTPException(404,"Course not found")
    if actor.role=="faculty" and course.faculty_id!=actor.id: raise HTTPException(403,"This course is not assigned to you")
    if not 1 <= data.duration_minutes <= 180: raise HTTPException(400,"Duration must be 1-180 minutes")
    s=AttendanceSession(course_id=course.id,faculty_id=actor.id,token=secrets.token_urlsafe(24),expires_at=datetime.utcnow()+timedelta(minutes=data.duration_minutes))
    db.add(s); db.flush(); log(db,actor,"SESSION_CREATED",f"{course.code}, session {s.id}"); db.commit()
    qr=qrcode.make(s.token); buf=io.BytesIO(); qr.save(buf,format="PNG"); image="data:image/png;base64,"+base64.b64encode(buf.getvalue()).decode()
    return {"id":s.id,"token":s.token,"expires_at":s.expires_at.isoformat()+"Z","qr_image":image,"course":course.name}

@app.post("/api/attendance/scan/{token}")
def scan(token: str, db: Session=Depends(get_db), actor=Depends(allow("student"))):
    s=db.query(AttendanceSession).filter(AttendanceSession.token==token).first()
    if not s: raise HTTPException(404,"Invalid attendance QR")
    if s.closed or datetime.utcnow()>s.expires_at: raise HTTPException(400,"Attendance session has expired or is closed")
    if db.query(Attendance).filter(Attendance.session_id==s.id,Attendance.student_id==actor.id).first(): raise HTTPException(409,"Attendance already submitted")
    a=Attendance(session_id=s.id,student_id=actor.id,status="present",source="qr"); db.add(a); log(db,actor,"QR_ATTENDANCE_MARKED",f"Session {s.id}"); db.commit()
    return {"message":"Attendance marked successfully","course":s.course.name,"status":"present"}

@app.post("/api/attendance/manual/{session_id}")
def manual(session_id:int,data:ManualAttendance,db:Session=Depends(get_db),actor=Depends(allow("admin","faculty"))):
    s=db.query(AttendanceSession).filter(AttendanceSession.id==session_id).first()
    if not s: raise HTTPException(404,"Session not found")
    if actor.role=="faculty" and s.faculty_id!=actor.id: raise HTTPException(403,"Not your session")
    if data.status not in ("present","absent","late","leave"): raise HTTPException(400,"Invalid status")
    if not db.query(User).filter(User.id==data.student_id,User.role=="student").first(): raise HTTPException(404,"Student not found")
    a=db.query(Attendance).filter(Attendance.session_id==session_id,Attendance.student_id==data.student_id).first()
    if a: a.status=data.status; a.source="manual"
    else: a=Attendance(session_id=session_id,student_id=data.student_id,status=data.status,source="manual"); db.add(a)
    log(db,actor,"ATTENDANCE_MANUAL_UPDATE",f"Session {session_id}, student {data.student_id}: {data.status}"); db.commit()
    return {"message":"Attendance saved"}

@app.post("/api/sessions/{session_id}/close")
def close_session(session_id:int,db:Session=Depends(get_db),actor=Depends(allow("admin","faculty"))):
    s=db.query(AttendanceSession).filter(AttendanceSession.id==session_id).first()
    if not s: raise HTTPException(404,"Session not found")
    if actor.role=="faculty" and s.faculty_id!=actor.id: raise HTTPException(403,"Not your session")
    s.closed=True; log(db,actor,"SESSION_CLOSED",str(session_id)); db.commit(); return {"message":"Session closed"}

@app.get("/api/attendance")
def attendance(db:Session=Depends(get_db),actor=Depends(current_user)):
    q=db.query(Attendance).options(joinedload(Attendance.student),joinedload(Attendance.session).joinedload(AttendanceSession.course))
    if actor.role=="student": q=q.filter(Attendance.student_id==actor.id)
    elif actor.role=="faculty": q=q.join(AttendanceSession).filter(AttendanceSession.faculty_id==actor.id)
    rows=q.order_by(Attendance.marked_at.desc()).limit(500).all()
    return [{"id":a.id,"student":a.student.name,"student_id":a.student_id,"roll_no":a.student.roll_no,"course":a.session.course.name,"course_code":a.session.course.code,"status":a.status,"source":a.source,"marked_at":a.marked_at.isoformat()} for a in rows]

@app.get("/api/dashboard")
def dashboard(db:Session=Depends(get_db),actor=Depends(current_user)):
    students=db.query(User).filter(User.role=="student",User.active==True).count()
    courses_count=db.query(Course).count()
    sessions=db.query(AttendanceSession)
    if actor.role=="faculty": sessions=sessions.filter(AttendanceSession.faculty_id==actor.id)
    if actor.role=="student":
        total=db.query(AttendanceSession).count(); present=db.query(Attendance).filter(Attendance.student_id==actor.id,Attendance.status.in_(["present","late"])).count()
        pct=round(present/total*100,1) if total else 0
        return {"students":1,"courses":db.query(Course).count(),"sessions":total,"present":present,"attendance_pct":pct,"role":"student"}
    total_sessions=sessions.count(); present=db.query(Attendance).filter(Attendance.status.in_(["present","late"])).count()
    records=db.query(Attendance).count(); pct=round(present/records*100,1) if records else 0
    return {"students":students,"courses":courses_count,"sessions":total_sessions,"records":records,"attendance_pct":pct,"role":actor.role}

@app.get("/api/reports/summary")
def report_summary(db:Session=Depends(get_db),actor=Depends(allow("admin","faculty"))):
    courses=db.query(Course).all(); result=[]
    for c in courses:
        if actor.role=="faculty" and c.faculty_id!=actor.id: continue
        total=db.query(Attendance).join(AttendanceSession).filter(AttendanceSession.course_id==c.id).count()
        present=db.query(Attendance).join(AttendanceSession).filter(AttendanceSession.course_id==c.id,Attendance.status.in_(["present","late"])).count()
        result.append({"course":c.name,"code":c.code,"records":total,"present":present,"percentage":round(present/total*100,1) if total else 0})
    return result

@app.get("/api/audit")
def audit(db:Session=Depends(get_db),actor=Depends(allow("admin"))):
    rows=db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return [{"id":r.id,"actor_id":r.actor_id,"action":r.action,"detail":r.detail,"created_at":r.created_at.isoformat()} for r in rows]


# ---- Extended academic operations ----
@app.get("/api/sessions")
def list_sessions(db: Session = Depends(get_db), actor=Depends(current_user)):
    q = db.query(AttendanceSession).options(joinedload(AttendanceSession.course))
    if actor.role == "faculty": q = q.filter(AttendanceSession.faculty_id == actor.id)
    rows = q.order_by(AttendanceSession.starts_at.desc()).limit(100).all()
    return [{"id":x.id,"course":x.course.name,"course_code":x.course.code,"faculty_id":x.faculty_id,"starts_at":x.starts_at.isoformat(),"expires_at":x.expires_at.isoformat(),"closed":x.closed,"active":(not x.closed and datetime.utcnow() <= x.expires_at)} for x in rows]

@app.get("/api/timetable")
def get_timetable(db: Session = Depends(get_db), actor=Depends(current_user)):
    q = db.query(TimetableEntry).options(joinedload(TimetableEntry.course), joinedload(TimetableEntry.faculty))
    if actor.role == "faculty": q = q.filter(TimetableEntry.faculty_id == actor.id)
    rows = q.order_by(TimetableEntry.day_of_week, TimetableEntry.start_time).all()
    return [{"id":x.id,"course_id":x.course_id,"course":x.course.name,"code":x.course.code,"faculty":x.faculty.name if x.faculty else "Unassigned","faculty_id":x.faculty_id,"day_of_week":x.day_of_week,"start_time":x.start_time,"end_time":x.end_time,"room":x.room} for x in rows]

@app.post("/api/timetable")
def add_timetable(data: TimetableCreate, db: Session=Depends(get_db), actor=Depends(allow("admin","faculty"))):
    course=db.query(Course).filter(Course.id==data.course_id).first()
    if not course: raise HTTPException(404,"Course not found")
    if actor.role=="faculty" and course.faculty_id!=actor.id: raise HTTPException(403,"This course is not assigned to you")
    if data.day_of_week not in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]: raise HTTPException(400,"Invalid day")
    if data.start_time >= data.end_time: raise HTTPException(400,"End time must be after start time")
    faculty_id=course.faculty_id if actor.role=="faculty" else course.faculty_id
    conflict=db.query(TimetableEntry).filter(TimetableEntry.day_of_week==data.day_of_week, TimetableEntry.course_id==data.course_id, TimetableEntry.start_time < data.end_time, TimetableEntry.end_time > data.start_time).first()
    if conflict: raise HTTPException(409,"This course already has a timetable entry at that time")
    item=TimetableEntry(course_id=data.course_id,faculty_id=faculty_id,day_of_week=data.day_of_week,start_time=data.start_time,end_time=data.end_time,room=data.room)
    db.add(item); log(db,actor,"TIMETABLE_CREATED",f"{course.code} {data.day_of_week} {data.start_time}-{data.end_time}"); db.commit(); db.refresh(item)
    return {"id":item.id,"message":"Timetable entry created"}

@app.delete("/api/timetable/{entry_id}")
def delete_timetable(entry_id:int, db:Session=Depends(get_db), actor=Depends(allow("admin"))):
    item=db.query(TimetableEntry).filter(TimetableEntry.id==entry_id).first()
    if not item: raise HTTPException(404,"Timetable entry not found")
    db.delete(item); log(db,actor,"TIMETABLE_DELETED",str(entry_id)); db.commit(); return {"message":"Timetable entry deleted"}

@app.post("/api/leaves")
def create_leave(data:LeaveCreate, db:Session=Depends(get_db), actor=Depends(allow("student"))):
    try:
        start=datetime.strptime(data.start_date,"%Y-%m-%d").date(); end=datetime.strptime(data.end_date,"%Y-%m-%d").date()
    except ValueError: raise HTTPException(400,"Dates must use YYYY-MM-DD")
    if end < start: raise HTTPException(400,"End date cannot be before start date")
    if not data.reason.strip(): raise HTTPException(400,"Please provide a reason")
    item=LeaveRequest(student_id=actor.id,start_date=data.start_date,end_date=data.end_date,reason=data.reason.strip()); db.add(item); log(db,actor,"LEAVE_REQUESTED",f"{data.start_date} to {data.end_date}"); db.commit(); db.refresh(item)
    return {"id":item.id,"status":item.status,"message":"Leave request submitted"}

@app.get("/api/leaves")
def list_leaves(db:Session=Depends(get_db), actor=Depends(current_user)):
    q=db.query(LeaveRequest).options(joinedload(LeaveRequest.student),joinedload(LeaveRequest.reviewer))
    if actor.role=="student": q=q.filter(LeaveRequest.student_id==actor.id)
    rows=q.order_by(LeaveRequest.created_at.desc()).limit(200).all()
    return [{"id":x.id,"student_id":x.student_id,"student":x.student.name,"roll_no":x.student.roll_no,"start_date":x.start_date,"end_date":x.end_date,"reason":x.reason,"status":x.status,"reviewer_note":x.reviewer_note,"reviewer":x.reviewer.name if x.reviewer else "","created_at":x.created_at.isoformat()} for x in rows]

@app.patch("/api/leaves/{request_id}")
def review_leave(request_id:int,data:LeaveReview,db:Session=Depends(get_db),actor=Depends(allow("admin","faculty"))):
    if data.status not in ["approved","rejected"]: raise HTTPException(400,"Status must be approved or rejected")
    item=db.query(LeaveRequest).filter(LeaveRequest.id==request_id).first()
    if not item: raise HTTPException(404,"Leave request not found")
    item.status=data.status; item.reviewer_id=actor.id; item.reviewer_note=data.reviewer_note; log(db,actor,"LEAVE_REVIEWED",f"Request {request_id}: {data.status}"); db.commit(); return {"message":"Leave request updated","status":item.status}

@app.get("/api/announcements")
def get_announcements(db:Session=Depends(get_db),actor=Depends(current_user)):
    q=db.query(Announcement).options(joinedload(Announcement.author))
    if actor.role!="admin": q=q.filter(Announcement.audience.in_(["all",actor.role]))
    return [{"id":x.id,"title":x.title,"body":x.body,"audience":x.audience,"author":x.author.name,"created_at":x.created_at.isoformat()} for x in q.order_by(Announcement.created_at.desc()).limit(100).all()]

@app.post("/api/announcements")
def post_announcement(data:AnnouncementCreate,db:Session=Depends(get_db),actor=Depends(allow("admin","faculty"))):
    if data.audience not in ["all","student","faculty"]: raise HTTPException(400,"Invalid audience")
    if not data.title.strip() or not data.body.strip(): raise HTTPException(400,"Title and message are required")
    item=Announcement(title=data.title.strip(),body=data.body.strip(),audience=data.audience,author_id=actor.id); db.add(item); log(db,actor,"ANNOUNCEMENT_POSTED",item.title); db.commit(); db.refresh(item); return {"id":item.id,"message":"Announcement published"}

@app.get("/api/defaulters")
def defaulters(threshold:float=75,db:Session=Depends(get_db),actor=Depends(allow("admin","faculty"))):
    if threshold<0 or threshold>100: raise HTTPException(400,"Threshold must be between 0 and 100")
    q=db.query(Attendance).options(joinedload(Attendance.student),joinedload(Attendance.session).joinedload(AttendanceSession.course))
    if actor.role=="faculty": q=q.join(AttendanceSession).filter(AttendanceSession.faculty_id==actor.id)
    rows=q.all(); grouped={}
    for r in rows:
        key=(r.student_id,r.session.course_id)
        x=grouped.setdefault(key,{"student_id":r.student_id,"student":r.student.name,"roll_no":r.student.roll_no,"course":r.session.course.name,"code":r.session.course.code,"total_recorded":0,"attended":0})
        x["total_recorded"]+=1
        if r.status in ["present","late"]: x["attended"]+=1
    out=[]
    for x in grouped.values():
        x["percentage"]=round(x["attended"]/x["total_recorded"]*100,1)
        if x["percentage"]<threshold: out.append(x)
    return sorted(out,key=lambda x:x["percentage"])
