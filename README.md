# 🚀 AttendX — Smart Campus Attendance Management System

<p align="center">
  <img src="https://img.shields.io/badge/AttendX-Smart%20Campus%20Solution-2563EB?style=for-the-badge&logo=googleclassroom&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</p>

<p align="center">
  <b>A smarter way to manage attendance, connect students and faculty, and simplify campus operations.</b>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#-technology-stack">Tech Stack</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-installation--setup">Installation</a>
</p>

---

## 🎓 Overview

**AttendX** is a full-stack Smart Campus Attendance Management System designed to modernize traditional classroom attendance.

The platform provides a centralized environment where administrators, faculty members, and students can interact with attendance-related services through role-based access.

With QR-based attendance, manual attendance management, student registration, and attendance analytics, AttendX aims to make campus attendance more efficient, transparent, and accessible.

### 💡 Why AttendX?

Traditional attendance systems often involve manual record maintenance, time-consuming processes, and limited visibility into attendance statistics.

AttendX addresses these challenges through a centralized digital platform that simplifies attendance tracking and campus-level management.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 Role-Based Authentication | Separate access for administrators, faculty, and students |
| 👨‍🎓 Student Management | Manage student information and registrations |
| 👩‍🏫 Faculty Management | Faculty account and classroom management |
| 📱 QR-Based Attendance | QR-enabled attendance session workflow |
| ✍️ Manual Attendance | Record attendance manually when required |
| 📊 Attendance Analytics | View attendance statistics and reports |
| 📥 CSV Export | Export attendance records for reporting |
| 🗓️ Timetable Management | Organize and manage class schedules |
| 📨 Leave Requests | Manage student leave requests |
| 📢 Announcements | Share important campus updates |
| ⚠️ Defaulter Watchlist | Identify students with low attendance |
| 📋 Audit Logs | Maintain activity records for accountability |

---

## 🛠️ Technology Stack

### Frontend
<p>
  <img src="https://skillicons.dev/icons?i=react,vite,js,html,css" />
</p>

- React.js
- Vite
- JavaScript
- HTML5
- CSS3

### Backend
<p>
  <img src="https://skillicons.dev/icons?i=python,fastapi" />
</p>

- Python 3.11
- FastAPI
- REST API
- JWT-based authentication

### Database & Development Tools
<p>
  <img src="https://skillicons.dev/icons?i=sqlite,git,github,vscode" />
</p>

- SQLite
- SQLAlchemy
- Git & GitHub
- Visual Studio Code

---

## 🏗️ System Architecture

AttendX follows a client-server architecture.

```text
             ┌─────────────────────────┐
             │       React Frontend    │
             │       (Vite + JS)       │
             └────────────┬────────────┘
                          │
                    HTTP / REST API
                          │
             ┌────────────▼────────────┐
             │      FastAPI Backend    │
             │                         │
             │  Authentication         │
             │  Attendance Management  │
             │  Student Management     │
             │  Faculty Management     │
             │  Analytics & Reports    │
             └────────────┬────────────┘
                          │
             ┌────────────▼────────────┐
             │       SQLite DB         │
             │                         │
             │  Users & Roles          │
             │  Attendance Records     │
             │  Student Information    │
             │  Campus Data            │
             └─────────────────────────┘
```

---

## 📂 Project Structure

```text
AttendX/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── student_registry.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
├── README.md
├── setup_windows.bat
└── start_attendx.bat
```

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have installed:

- Python 3.11
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/kishoreb13/AttendX.git
cd AttendX
```

### 2. Setup Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

`http://127.0.0.1:8000`

API Documentation:

`http://127.0.0.1:8000/docs`

### 3. Setup Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

`http://localhost:5173`

### 4. Access AttendX

Open the frontend URL in your browser and access the application.

---

## 🔄 Application Workflow

1. Users access the platform through the frontend.
2. Authentication identifies the user's role and permissions.
3. Faculty members manage attendance sessions.
4. Students participate in attendance workflows.
5. Attendance records are stored in the database.
6. Administrators and faculty can review attendance information and reports.

---

## 🔮 Future Enhancements

- 📸 Advanced QR scanning with camera integration.
- 🤖 AI-powered attendance insights and predictive analytics.
- ☁️ Cloud deployment and scalable database integration.
- 📱 Mobile application support.
- 🔔 Real-time notifications and alerts.
- 📈 Advanced student performance analytics.

---

## 👨‍💻 Developed By

<p align="center">
  <b>AttendX — Smart Campus Attendance Management System</b>
  <br/>
  Developed with ❤️ using React, FastAPI and SQLite.
  <br/><br/>
  <a href="https://github.com/kishoreb13">
    <img src="https://img.shields.io/badge/GitHub-kishoreb13-181717?style=for-the-badge&logo=github" />
  </a>
</p>

<p align="center">
  ⭐ If you find this project interesting, consider giving it a star!
</p>
