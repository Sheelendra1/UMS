# 🎓 University Management System (UMS)

A comprehensive, role-based University Management System built with **Django 6.0** and **Bootstrap 5**. It provides dedicated dashboards for **Admins**, **Faculty**, **Students**, and **Accountants** — covering academics, attendance, examinations, fees, timetables, and notices across **44+ screens**.

---

## 📸 Overview

| Role | Key Capabilities |
|------|-----------------|
| **Admin** | Full CRUD on students, faculty, departments, courses, exams, fees, timetables, notices, and system settings |
| **Faculty** | View assigned courses, take attendance, upload marks, post notices, view reports |
| **Student** | View courses, attendance, results, timetable, fee status, notices; download PDF transcripts & ID card |
| **Accountant** | Collect fees, manage payment history, generate financial reports, view/post notices |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django 6.0.2 |
| Frontend | Django Templates, Bootstrap 5, Bootstrap Icons |
| Database | SQLite3 (zero configuration) |
| Authentication | Django Auth with Custom User Model (role-based) |
| PDF Generation | xhtml2pdf |
| Image Handling | Pillow |

---

## 📁 Project Structure

```
ums/
├── manage.py
├── create_superuser.py          # Quick superuser setup script
├── db.sqlite3                   # SQLite database
├── ums/                         # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                    # Custom user model & authentication
├── students/                    # Student profiles & student panel
├── faculty/                     # Faculty profiles & teacher panel
├── departments/                 # Department management
├── courses/                     # Course management & enrollment
├── attendance/                  # Attendance sessions & records
├── examinations/                # Exams & results
├── fees/                        # Fee structures, payments & accountant panel
├── timetable/                   # Weekly schedule management
├── notices/                     # Targeted announcements
├── core/                        # Admin dashboard, settings, public pages, search
├── templates/                   # All HTML templates organized by role
│   ├── base.html                # Admin base layout
│   ├── student/                 # Student panel templates
│   ├── teacher/                 # Faculty panel templates
│   ├── accountant/              # Accountant panel templates
│   ├── registration/            # Auth templates (login, password change)
│   └── includes/                # Shared components (sidebar, navbar)
├── static/                      # CSS, JS, images
└── media/                       # Uploaded files (profile images, attachments)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/UMS.git
cd UMS

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install django pillow xhtml2pdf

# 4. Navigate to the project directory
cd ums

# 5. Run database migrations
python manage.py migrate

# 6. Create a superuser (Option A: Quick script)
python create_superuser.py
# Creates user: admin / password: adminpassword

# 6. Create a superuser (Option B: Interactive)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** to access the application.

---

## 👥 User Roles & Default Credentials

| Role | Username | Password | Login URL |
|------|----------|----------|-----------|
| Admin | `admin` | `adminpassword` | `/accounts/login/` |

> After logging in as Admin, you can create Faculty, Student, and Accountant accounts from the admin panel.

---

## 📋 Features by Role

### 🔑 Admin Panel (14 pages)

- **Dashboard** — Statistics cards (students, teachers, courses, attendance %, revenue), recent activity
- **Department Management** — Add/Edit/Delete departments, assign Head of Department
- **Student Management** — Full CRUD, view student detail (attendance + results + fees), bulk semester promotion
- **Faculty Management** — Full CRUD, view assigned courses
- **Course Management** — Create courses, assign faculty, set capacity, enroll students
- **Timetable Management** — Create schedule slots (course, faculty, day, time, room)
- **Attendance Overview** — View all records, filter by department and date
- **Exam Management** — Create exams (Mid/Final/Internal), publish/lock results
- **Fee Management** — Fee structures per department/semester, view all payments
- **Notice Management** — Create/Edit/Delete notices with audience targeting
- **System Settings** — University name, logo, academic year, current semester
- **Global Search** — Search across students, faculty, and courses

### 👨‍🏫 Faculty Panel (8 pages)

- **Dashboard** — Assigned courses, total students, pending grading, today's schedule
- **My Courses** — View assigned courses with enrolled student lists
- **Timetable** — Weekly teaching schedule
- **Take Attendance** — Select course/date, mark present/absent, prevent duplicates
- **Upload Marks** — Enter/update marks per student (locked when published)
- **Notices** — View and post notices for courses
- **View Students** — Browse students, view individual profiles
- **Reports** — Class performance and attendance reports
- **Profile** — Update info, change password

### 🎓 Student Panel (7 pages + PDF downloads)

- **Dashboard** — Enrolled courses, attendance %, pending dues, upcoming exams, recent results
- **My Courses** — Course list with attendance and results per course
- **My Attendance** — Subject-wise summary, daily records, filter by date range
- **Timetable** — Weekly schedule based on enrolled courses
- **My Results** — Filter by course/exam type, summary stats, **PDF transcript download**
- **Fee Status** — Fee structure, payment history, pending dues, **PDF receipt download**
- **Notices** — General + course-specific notices
- **Profile** — Update contact info, profile image, change password
- **ID Card** — Downloadable PDF student ID card

### 💰 Accountant Panel (6 pages)

- **Dashboard** — Total collected, pending dues, monthly revenue chart
- **Collect Fees** — Search student, enter payment, select mode (Cash/Cheque/Online), auto-generate receipt
- **Payment History** — List transactions, filter by date and student
- **Financial Reports** — Monthly/annual summaries with export
- **Notices** — View and post finance-related notices
- **Profile** — Update info, change password

---

## 🗄️ Database Models

| Model | App | Key Fields |
|-------|-----|-----------|
| `CustomUser` | accounts | `role` (Admin/Faculty/Student/Accountant), `phone`, `profile_image` |
| `Student` | students | `enrollment_no`, `department`, `semester`, `admission_date` |
| `Faculty` | faculty | `department`, `designation`, `joining_date` |
| `Department` | departments | `name`, `code`, `hod` |
| `Course` | courses | `name`, `code`, `department`, `faculty`, `semester`, `credits`, `capacity`, `students` (M2M) |
| `Timetable` | timetable | `course`, `faculty`, `day_of_week`, `start_time`, `end_time`, `room_number` |
| `Attendance` | attendance | `course`, `date`, `marked_by` (unique per course/date) |
| `AttendanceRecord` | attendance | `attendance`, `student`, `status` (Present/Absent) |
| `Exam` | examinations | `course`, `exam_type`, `total_marks`, `date`, `is_published` |
| `Result` | examinations | `exam`, `student`, `marks_obtained` |
| `FeeStructure` | fees | `department`, `semester`, `amount` |
| `FeePayment` | fees | `student`, `amount_paid`, `status`, `payment_mode`, `receipt_no` (auto UUID) |
| `Notice` | notices | `title`, `description`, `target_audience`, `target_course`, `attachment` |
| `UniversitySetting` | core | `university_name`, `logo`, `academic_year`, `current_semester` (Singleton) |

---

## 🔒 Access Control

- **Custom decorators** (`admin_required`, `faculty_required`, `student_required`, `accountant_required`) protect views based on user role
- Each role has a dedicated **base template** with role-specific sidebar navigation
- Role-based **dashboard redirect** after login — users are automatically routed to their panel
- Password change pages dynamically render within the user's own panel layout

---

## 📄 License

This project is for educational purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request