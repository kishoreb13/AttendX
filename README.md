# ⚡ AttendX
### Attendance, reimagined for the modern campus.

<p align="center">
  <img src="https://img.shields.io/badge/PLATFORM-SMART%20CAMPUS-6366F1?style=flat-square" />
  <img src="https://img.shields.io/badge/STATUS-IN%20DEVELOPMENT-F59E0B?style=flat-square" />
  <img src="https://img.shields.io/badge/BUILT%20WITH-OPEN%20TECHNOLOGY-10B981?style=flat-square" />
</p>

<p align="center">
  <a href="https://github.com/kishoreb13/AttendX">Repository</a> ·
  <a href="http://127.0.0.1:8000/docs">API Docs (Local)</a> ·
  <a href="#getting-started">Get Started</a>
</p>

---

<p align="center">
  <b>ONE CAMPUS. THREE ROLES. ONE CONNECTED SYSTEM.</b>
</p>

AttendX is a digital attendance and campus management platform that brings students, faculty, and administrators together in one centralized environment.

From QR-enabled attendance sessions to student records and attendance insights, AttendX transforms everyday campus operations into a streamlined digital experience.

---

## ◈ The Experience

<table>
<tr>
<td width="33%" align="center">

### 🎓 Student

Access attendance information, participate in attendance workflows, submit leave requests, and stay updated with campus announcements.

</td>
<td width="33%" align="center">

### 🧑‍🏫 Faculty

Manage attendance sessions, record student attendance, view class statistics, and organize classroom activities.

</td>
<td width="33%" align="center">

### 🛡️ Administrator

Manage campus users, oversee attendance records, monitor activities, and access centralized reports.

</td>
</tr>
</table>

## ◈ What Powers AttendX?

**01 / Attendance Engine**

- QR-based attendance sessions
- Manual attendance recording
- Session expiry and validation
- Duplicate attendance prevention

**02 / Campus Management**

- Student and faculty management
- Student registration
- Timetable management
- Leave request management
- Campus announcements

**03 / Insights & Monitoring**

- Attendance analytics
- CSV report exports
- Low-attendance watchlist
- Activity audit logs

---

## ◈ Built With Purpose

| Layer | Technologies |
|---|---|
| Interface | React.js, Vite, JavaScript, HTML, CSS |
| Application Server | Python, FastAPI |
| Data Layer | SQLite, SQLAlchemy |
| Authentication | JWT-based authentication |
| Developer Tools | Git, GitHub, VS Code |

---

## ◈ Under the Hood

```text
       ┌──────────────────────────┐
       │       USER INTERFACE     │
       │       React + Vite       │
       └────────────┬─────────────┘
                    │
                    ▼
       ┌──────────────────────────┐
       │       REST API LAYER     │
       │         FastAPI          │
       └────────────┬─────────────┘
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Auth      Attendance  Campus
       Module     Module    Modules
          │         │         │
          └─────────┼─────────┘
                    ▼
       ┌──────────────────────────┐
       │       DATA LAYER         │
       │         SQLite           │
       └──────────────────────────┘
```

---

## ◈ Get It Running

**Requirements:** Python 3.11, Node.js and npm.

**1 — Clone**

```bash
git clone https://github.com/kishoreb13/AttendX.git
cd AttendX
```

**2 — Start the backend**

```bash
cd backend
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install and run:

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**3 — Start the frontend**

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

**4 — Launch**

| Service | Address |
|---|---|
| AttendX Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000 |
| Swagger Documentation | http://127.0.0.1:8000/docs |

---

## ◈ Repository Map

```text
AttendX/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── student_registry.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   └── index.html
│
├── README.md
├── .gitignore
├── setup_windows.bat
└── start_attendx.bat
```

---

## ◈ The Road Ahead

The next evolution of AttendX could include:

- Intelligent attendance pattern analysis
- Advanced camera-based QR scanning
- Cloud-hosted deployment
- Mobile-first campus experience
- Real-time alerts and notifications

---

<p align="center">
  <b>Designed to simplify the everyday campus experience.</b>
  <br/><br/>
  <a href="https://github.com/kishoreb13">Developer · GitHub</a>
  <br/>
  <sub>AttendX | Smart Campus Attendance Management System</sub>
</p>
