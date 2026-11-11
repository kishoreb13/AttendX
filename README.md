# AttendX — Smart Campus Attendance Management System

AttendX is a full-stack academic operations demo for administrators, faculty and students. It combines attendance sessions, QR scanning, academic scheduling, leave workflows, campus announcements and attendance reporting in one application.

## Included modules

- **Authentication and roles:** JWT login, password hashing, admin/faculty/student route permissions.
- **People directory:** Admin creates student and faculty accounts; directory views are role-protected.
- **Courses:** Create courses and assign faculty members.
- **Attendance:** Timed QR sessions, QR image generation, student token submission, browser camera scanning, duplicate-submission protection, expiry/closed-session checks and manual attendance corrections.
- **Timetable:** Create weekly class slots, view the schedule and remove entries as administrator. Basic same-course time-overlap validation is applied.
- **Leave requests:** Students submit date-range requests; administrators/faculty approve or reject them.
- **Announcements:** Admin/faculty publish campus notices to everyone, students or faculty.
- **Analytics:** Dashboard statistics, course-level attendance summaries, CSV exports and a configurable 75% attendance watchlist.
- **Audit logs:** Administrative and attendance actions are recorded for review.

> The attendance watchlist is a **rule-based indicator calculated from recorded attendance entries**, not an ML prediction. The current schema does not include course enrolment, so it does not count sessions a student never had an attendance row for. The reported percentage is therefore a percentage of recorded entries for that student/course pair.

## Technology

- Frontend: React, Vite, JavaScript, Recharts, Lucide, html5-qrcode
- Backend: Python 3.11, FastAPI, SQLAlchemy
- Database: SQLite (created automatically in `backend/attendx.db`)
- Authentication: JWT and bcrypt password hashing
- QR: server-generated QR token/image plus browser camera scanning

## Requirements

- Python **3.11.x** (recommended; tested target)
- Node.js LTS (20 or newer) and npm
- Windows 10/11, macOS or Linux

## Windows setup (VS Code)

1. Extract the ZIP and open the `AttendX` folder in VS Code.
2. Run `setup_windows.bat` once. It creates `backend\.venv`, installs Python requirements and installs frontend packages.
3. Run `start_attendx.bat`. It opens separate backend and frontend terminal windows.
4. Open the frontend URL printed by Vite, normally `http://localhost:5173`.
5. API docs: `http://127.0.0.1:8000/docs`.

### Manual setup

Backend terminal:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Frontend terminal:

```powershell
cd frontend
npm install
npm run dev
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again. Alternatively, use `backend\.venv\Scripts\python.exe -m pip ...` without activation.

## Demo administrator

- Email: `admin@attendx.edu`
- Password: `Admin@123`

On first backend startup, the demo administrator is seeded if it does not already exist. Create faculty and student accounts from **Students** after signing in. Create a course and assign it to a faculty account before generating attendance sessions.

## Suggested demo sequence

1. Sign in as admin and create one faculty account and two student accounts (use unique emails and roll numbers).
2. Create a course and assign it to the faculty member.
3. Add timetable slots and publish an announcement.
4. Sign in as faculty; generate a timed QR session for the assigned course.
5. Sign in as a student on a device with a camera; open Attendance → Open camera scanner and scan the QR displayed by faculty. If camera access is unavailable, use the manual token field.
6. Review attendance records, submit a leave request as student and approve/reject it as faculty/admin.
7. Review Analytics, Defaulters and Audit Logs; export CSV files.

## Important limitations and production hardening

- A QR code is a bearer token. It can be shared; scanning it does **not** prove physical presence. A real deployment should consider faculty confirmation, device/session binding, classroom network checks, rate limits and institutional policy.
- Camera access normally requires `localhost` or HTTPS and explicit browser permission.
- The SQLite database is suitable for a local demo, not a multi-campus production deployment. Use PostgreSQL, migrations and backups for production.
- Change the demo password and JWT secret, use environment-managed secrets, HTTPS, secure cookie/token handling, rate limiting, monitoring and automated tests before deployment. Do not use real student data in a public demo.
- Timetable entries are manually managed; there is no background scheduler automatically opening attendance sessions.
- Announcements are stored and displayed in-app; outbound email/SMS/push delivery is not configured.

## Project structure

```text
AttendX/
  backend/
    main.py
    models.py
    schemas.py
    database.py
    requirements.txt
  frontend/
    index.html
    package.json
    src/main.jsx
    src/style.css
  setup_windows.bat
  start_attendx.bat
  README.md
```

## Troubleshooting

- **`python` not recognized:** install Python 3.11 and enable Add Python to PATH, then restart VS Code.
- **`npm` not recognized:** install Node.js LTS and restart VS Code.
- **Frontend says Failed to fetch:** ensure the backend terminal still shows Uvicorn running on port 8000.
- **Browser says connection refused at port 8000:** restart the backend from the `backend` directory.
- **Camera is unavailable:** allow camera access and use `http://localhost:5173`; manual token submission remains available.
- **Reset local demo data:** stop the backend and delete `backend/attendx.db`, then restart. This permanently deletes local demo records.

## Student self-registration and separate student database

The login screen includes a **Student registration** tab. A student can register with a valid email address (including Gmail), full name, unique roll number, department, semester, and a password of at least 8 characters. The API always assigns the `student` role; public registration cannot create faculty or administrator accounts. Duplicate email addresses and roll numbers are rejected.

On first backend startup, AttendX creates two SQLite files in the `backend` folder:

- `attendx.db` — the main application database. It stores login accounts (with password hashes), courses, attendance, timetable, leave requests, announcements and audit logs.
- `student_registry.db` — a separate student registration/profile registry. It stores the student ID, name, email, roll number, department, semester and registration timestamp. It does **not** store plaintext passwords.

Both databases are created automatically; do not create them manually. Back up both files before moving or resetting the project. The student registry is a secondary profile record; the main `attendx.db` remains the source used by login and attendance features.

**Email verification note:** self-registration currently validates the email format and creates the account immediately. It does not send an OTP or verify mailbox ownership. Add SMTP/OTP verification before using this for a real institution or public deployment.
