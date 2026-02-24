# 🎓 University Management System (UMS)

A comprehensive, role-based University Management System built with **Django 6.0** and **Bootstrap 5**. It provides dedicated dashboards for **Admins**, **Faculty**, **Students**, and **Accountants** — covering academics, attendance, examinations, fees, timetables, and notices across **44+ screens**.


---

## 🚀 How to Run This Project

Follow these steps to set up and run the University Management System on your local machine:

### 1. Prerequisites
- **Python 3.12+**: Make sure Python is installed. You can check with `python --version`.
- **pip**: Python package manager (usually comes with Python).

### 2. Setup Instructions

```bash
# 1. Clone or Download the project
# If you have git:
git clone https://github.com/yourusername/UMS.git
cd UMS

# 2. Create a Virtual Environment
# This keeps the project dependencies separate from your system
python -m venv .venv

# 3. Activate the Virtual Environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 4. Install Dependencies
# This project requires Django, Pillow (for images), and xhtml2pdf (for PDFs)
pip install django pillow xhtml2pdf

# 5. Navigate to the project directory
cd ums

# 6. Apply Database Migrations
# This creates the necessary tables in the SQLite database
python manage.py migrate

# 7. Create a Superuser (Admin)
# We have a script for a quick setup (admin/adminpassword)
python create_superuser.py
# OR create your own manually:
# python manage.py createsuperuser

# 8. Run the Development Server
python manage.py runserver
```

### 3. Accessing the System
- Open your web browser and go to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**
- **Admin Login**: Use `admin` as username and `adminpassword` as password.
- Once logged in, you can manage the entire university system from the dashboard.

---

## Table of Contents
1. [How to Run This Project](#how-to-run-this-project)
2. [Project Overview](#2-project-overview)
3. [Technology Stack (with explanation)](#3-technology-stack)
4. [Project Architecture & Structure](#4-project-architecture--structure)
5. [How Django Works (the basics)](#5-how-django-works)
6. [Settings File Explained](#6-settings-file-explained)
7. [URL Routing — How Pages Are Served](#7-url-routing)
8. [Custom User Model & Authentication](#8-custom-user-model--authentication)
9. [All Models Explained (Database Tables)](#8-all-models-explained)
10. [All Views Explained (Business Logic)](#9-all-views-explained)
11. [Forms Explained](#10-forms-explained)
12. [Templates & Frontend](#11-templates--frontend)
13. [Utility Functions](#12-utility-functions)
14. [Admin Panel Configuration](#13-admin-panel-configuration)
15. [Role-Based Access Control](#14-role-based-access-control)
16. [Complete Data Flow Examples](#15-complete-data-flow-examples)
17. [Database Relationships (ER Diagram in Text)](#16-database-relationships)
18. [PDF Generation](#17-pdf-generation)
19. [Key Design Patterns Used](#18-key-design-patterns-used)
20. [Likely Viva Questions & Answers](#19-likely-viva-questions--answers)

---

## 1. Project Overview

### What is UMS?
UMS (University Management System) is a **web-based application** that manages all academic and administrative activities of a university. It is built using **Django (Python)** and provides separate dashboards for 4 types of users.

### What does it do?
- Manages **Students**, **Faculty**, **Departments**, and **Courses**
- Handles **Attendance** marking and tracking
- Manages **Examinations** and **Results**
- Tracks **Fee Payments** and generates receipts
- Manages **Timetables** with clash detection
- Posts **Notices** targeted to specific audiences
- Generates **PDF documents** (transcripts, ID cards, receipts)
- Provides **Global Search** across the system

### The 4 User Roles

| Role | What they can do |
|------|-----------------|
| **Admin** | Full control — CRUD on all entities, view reports, manage settings |
| **Faculty** | View their courses, mark attendance, upload marks, post notices, view reports |
| **Student** | View their courses, attendance, results, fees, timetable, notices; download PDFs |
<!-- | **Accountant** | Collect fees, view payment history, generate financial reports, post notices | -->

### How many screens?
The system has **44+ screens** (HTML pages) distributed across the 4 roles.

---

## 2. Technology Stack

### Backend — Python & Django 6.0

| Technology | What it is | Why we use it |
|-----------|-----------|--------------|
| **Python** | A high-level programming language | Easy to read, large ecosystem, ideal for web development |
| **Django 6.0.2** | A Python web framework (MVT pattern) | Provides built-in ORM, authentication, admin panel, routing, templating — everything needed for a web app |
| **SQLite3** | A lightweight file-based relational database | Zero configuration, perfect for development/small projects. Data stored in `db.sqlite3` file |
| **xhtml2pdf** | A Python library to convert HTML to PDF | Used to generate student transcripts, ID cards, fee receipts as downloadable PDFs |
| **Pillow** | Python Imaging Library | Required by Django's `ImageField` to handle profile image uploads |

### Frontend — Django Templates + Bootstrap 5

| Technology | What it is | Why we use it |
|-----------|-----------|--------------|
| **Django Template Engine** | Server-side HTML rendering | Django renders HTML on the server before sending it to the browser. Uses `{% %}` and `{{ }}` syntax |
| **Bootstrap 5** | CSS framework | Provides pre-built responsive UI components (buttons, cards, tables, forms, navigation) |
| **Bootstrap Icons** | Icon library | Provides icons (like sidebar icons, action buttons) |

### Key Concept: No separate frontend framework
This project does **NOT** use React, Angular, or Vue. Instead, Django itself generates the HTML pages on the server using its **template engine**, and Bootstrap provides the styling. This is called **Server-Side Rendering (SSR)**.

---

## 3. Project Architecture & Structure

### MVT Pattern (Model-View-Template)
Django follows the **MVT** pattern, which is similar to MVC:

```
┌───────────┐       ┌───────────┐       ┌───────────┐
│  MODEL    │──────▶│   VIEW    │──────▶│ TEMPLATE  │
│ (Database)│       │ (Logic)   │       │  (HTML)   │
└───────────┘       └───────────┘       └───────────┘
     │                    ▲                    │
     │                    │                    │
     └── stores data      │                   └── renders the
         in tables        handles requests         final page
                          & passes data
```

- **Model** = Database table (defined in `models.py`)
- **View** = Business logic / controller (defined in `views.py`)
- **Template** = HTML page with Django tags (files in `templates/` folder)

### Folder Structure Explained

```
ums/                          ← Root project folder
├── manage.py                 ← Django's command-line tool (runserver, migrate, etc.)
├── create_superuser.py       ← Python script to auto-create admin user
├── db.sqlite3                ← The SQLite database FILE (all data is here)
│
├── ums/                      ← Django PROJECT configuration folder
│   ├── settings.py           ← All project settings (database, apps, middleware)
│   ├── urls.py               ← ROOT URL router — connects URLs to apps
│   ├── wsgi.py               ← Entry point for traditional web servers
│   └── asgi.py               ← Entry point for async web servers
│
├── accounts/                 ← APP: User authentication & custom user model
├── students/                 ← APP: Student profiles, student panel views
├── faculty/                  ← APP: Faculty profiles, teacher panel views
├── departments/              ← APP: Department CRUD
├── courses/                  ← APP: Course CRUD & enrollment
├── attendance/               ← APP: Attendance sessions & records
├── examinations/             ← APP: Exams & results
├── fees/                     ← APP: Fee structures, payments & accountant panel
├── timetable/                ← APP: Weekly schedule with clash detection
├── notices/                  ← APP: Targeted announcements
├── core/                     ← APP: Admin dashboard, settings, public pages, search
│
├── templates/                ← ALL HTML templates
│   ├── base.html             ← Master layout for Admin panel
│   ├── student/              ← Student panel templates (8 pages)
│   ├── teacher/              ← Faculty panel templates (9 pages)
│   ├── accountant/           ← Accountant panel templates (6 pages)
│   ├── registration/         ← Login, password change/reset pages
│   ├── includes/             ← Reusable components (sidebar, navbar)
│   ├── common/               ← Public pages (about, contact)
│   └── [app_name]/           ← Admin-facing CRUD pages
│
├── static/                   ← CSS, JavaScript, images (served by Django)
└── media/                    ← User-uploaded files (profile pics, attachments)
```

### What is a Django "App"?
Each folder like `students/`, `faculty/`, `courses/` is a **Django App** — a self-contained module with its own:
- `models.py` — Database tables
- `views.py` — Business logic
- `urls.py` — URL routes
- `admin.py` — Django admin configuration
- `apps.py` — App configuration
- `migrations/` — Database migration files (auto-generated)

### Inside Each App

| File | Purpose |
|------|---------|
| `models.py` | Defines database tables as Python classes |
| `views.py` | Contains functions/classes that handle HTTP requests and return responses |
| `urls.py` | Maps URL patterns (like `/students/list/`) to view functions |
| `admin.py` | Registers models with Django's built-in admin panel |
| `apps.py` | App metadata (name, label) |
| `forms.py` | Custom form classes for data validation (only in `examinations/` and `timetable/`) |
| `tests.py` | Unit tests (not used in this project) |
| `migrations/` | Auto-generated files that track database schema changes |

---

## 4. How Django Works

### Request → Response Cycle

When a user visits a URL (e.g., `http://localhost:8000/students/list/`), here's what happens:

```
1. Browser sends HTTP request to Django server
2. Django looks at ROOT_URLCONF (ums/urls.py)
3. ums/urls.py says: "students/ → include('students.urls')"
4. Django goes to students/urls.py
5. students/urls.py says: "list/ → views.student_list"
6. Django calls the student_list() function in students/views.py
7. The view function:
   a. Queries the database using the ORM (models)
   b. Puts data into a dictionary (context)
   c. Passes context to a template (HTML file)
8. Django renders the template with the data
9. Returns the rendered HTML as an HTTP response
10. Browser displays the page
```

### Important Django Commands

| Command | What it does |
|---------|-------------|
| `python manage.py runserver` | Starts the development server on port 8000 |
| `python manage.py migrate` | Creates/updates database tables from migration files |
| `python manage.py makemigrations` | Generates migration files from model changes |
| `python manage.py createsuperuser` | Creates an admin user interactively |
| `python manage.py shell` | Opens Python shell with Django loaded |

---

## 5. Settings File Explained

**File: `ums/ums/settings.py`**

This is the **brain** of the Django project. Every configuration lives here.

### Key Settings Breakdown

```python
BASE_DIR = Path(__file__).resolve().parent.parent
# ↑ Automatically calculates the project root directory
# Used to build file paths like BASE_DIR / 'templates'

SECRET_KEY = 'django-insecure-...'
# ↑ A unique secret key used for cryptographic signing
# (session cookies, CSRF tokens, password hashing)
# In production, this should be kept secret

DEBUG = True
# ↑ When True: shows detailed error pages, auto-reloads on code changes
# Must be False in production for security

INSTALLED_APPS = [
    'django.contrib.admin',         # Built-in admin panel
    'django.contrib.auth',          # Authentication system
    'django.contrib.contenttypes',  # Content type framework
    'django.contrib.sessions',      # Session management
    'django.contrib.messages',      # Flash messages
    'django.contrib.staticfiles',   # Static file serving

    # Our Custom Apps (11 apps total):
    'accounts',      # Custom user model
    'students',      # Student management
    'faculty',       # Faculty management
    'departments',   # Department CRUD
    'courses',       # Course management
    'attendance',    # Attendance system
    'examinations',  # Exams & results
    'fees',          # Fee management
    'timetable',     # Timetable management
    'core',          # Dashboard, settings, public pages
    'notices',       # Notice board
]

AUTH_USER_MODEL = 'accounts.CustomUser'
# ↑ CRITICAL: Tells Django to use OUR CustomUser model instead of
# the default User model. This allows us to add 'role', 'phone', 'profile_image'

MIDDLEWARE = [...]
# ↑ Middleware = layers that process every request/response
# SecurityMiddleware: adds security headers
# SessionMiddleware: manages user sessions
# CsrfViewMiddleware: prevents Cross-Site Request Forgery attacks
# AuthenticationMiddleware: attaches user object to request

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# ↑ Using SQLite — a single-file database
# No server needed, data stored in db.sqlite3

TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],  # Where to find HTML templates
    'APP_DIRS': True,                   # Also look in each app's templates/ folder
}]

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# ↑ Static files (CSS, JS, images) served from /static/ URL

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# ↑ User-uploaded files stored in media/ folder

LOGIN_REDIRECT_URL = 'dashboard_redirect'
# ↑ After login, redirect to this URL name (which then redirects by role)
LOGIN_URL = 'login'
# ↑ If user is not logged in, redirect them to this URL
LOGOUT_REDIRECT_URL = 'login'
# ↑ After logout, go back to login page
```

---

## 6. URL Routing

### How URL Routing Works

URLs are processed in two levels:

**Level 1: Root URLs (`ums/urls.py`)**
```
/                    → core.urls        (home, dashboard, settings, public pages)
/students/           → students.urls    (student management & student panel)
/faculty/            → faculty.urls     (faculty management & teacher panel)
/departments/        → departments.urls (department CRUD)
/courses/            → courses.urls     (course CRUD & enrollment)
/notices/            → notices.urls     (notice CRUD)
/attendance/         → attendance.urls  (attendance list & detail)
/examinations/       → examinations.urls (exam CRUD & results)
/fees/               → fees.urls        (fee management & accountant panel)
/timetable/          → timetable.urls   (timetable CRUD)
/accounts/           → accounts.urls    (login, logout, password)
/admin/              → Django admin site
```

**Level 2: App-level URLs**

### All URLs in the System (Complete List)

#### Accounts App (Authentication)
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/accounts/login/` | `CustomLoginView` | `login` | Login page with "Remember Me" |
| `/accounts/logout/` | `LogoutView` | `logout` | Logout and redirect to login |
| `/accounts/dashboard/` | `dashboard_redirect` | `dashboard_redirect` | Redirects to role-specific dashboard |
| `/accounts/profile/` | `profile` | `profile` | View user profile |
| `/accounts/password-change/` | `MainPasswordChangeView` | `password_change` | Change password (logged in) |
| `/accounts/password-change/done/` | `MainPasswordChangeDoneView` | `password_change_done` | Password change success |
| `/accounts/password-reset/` | `PasswordResetView` | `password_reset` | Forgot password form |
| `/accounts/password-reset/done/` | `PasswordResetDoneView` | `password_reset_done` | Reset email sent |
| `/accounts/reset/<uidb64>/<token>/` | `PasswordResetConfirmView` | `password_reset_confirm` | Set new password from email link |
| `/accounts/reset/done/` | `PasswordResetCompleteView` | `password_reset_complete` | Password reset complete |

#### Core App (Dashboard & Public)
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/` | `home_redirect` | `home` | Redirects to dashboard |
| `/dashboard/admin/` | `admin_dashboard` | `admin_dashboard` | Admin dashboard with stats |
| `/settings/` | `settings_view` | `settings` | University settings (name, logo, year) |
| `/about/` | `about_university` | `about_university` | Public about page |
| `/contact/` | `contact_page` | `contact_page` | Public contact form |
| `/profile/<username>/` | `public_profile` | `public_profile` | Public profile of any user |
| `/search/` | `global_search` | `global_search` | Search students, faculty, courses |

#### Students App (Admin + Student Panel)
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/students/list/` | `student_list` | `student_list` | Admin: List all students with filters |
| `/students/<pk>/` | `student_detail` | `student_detail` | Admin: View student details |
| `/students/add/` | `add_student` | `add_student` | Admin: Add new student |
| `/students/<pk>/edit/` | `edit_student` | `edit_student` | Admin: Edit student |
| `/students/<pk>/delete/` | `delete_student` | `delete_student` | Admin: Delete student |
| `/students/promote/` | `promote_students` | `promote_students` | Admin: Promote to next semester |
| `/students/dashboard/` | `student_dashboard` | `student_dashboard` | Student: Dashboard |
| `/students/courses/` | `student_my_courses` | `student_my_courses` | Student: Enrolled courses |
| `/students/courses/<id>/` | `student_course_detail` | `student_course_detail` | Student: Course details |
| `/students/attendance/` | `student_my_attendance` | `student_my_attendance` | Student: Attendance records |
| `/students/timetable/` | `student_timetable` | `student_timetable` | Student: Weekly timetable |
| `/students/results/` | `student_my_results` | `student_my_results` | Student: Exam results |
| `/students/fees/` | `student_fee_status` | `student_fee_status` | Student: Fee status |
| `/students/notices/` | `student_notices` | `student_notices` | Student: Notices |
| `/students/profile/` | `student_profile` | `student_profile` | Student: Edit profile |
| `/students/results/download/` | `download_results_pdf` | `download_results_pdf` | Student: PDF transcript |
| `/students/id-card/download/` | `download_id_card_pdf` | `download_id_card_pdf` | Student: PDF ID card |
| `/students/fee-receipt/download/<id>/` | `download_receipt_pdf` | `download_receipt_pdf` | Student: PDF receipt |

#### Faculty App (Admin + Teacher Panel)
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/faculty/list/` | `faculty_list` | `faculty_list` | Admin: List all faculty |
| `/faculty/add/` | `add_faculty` | `add_faculty` | Admin: Add faculty |
| `/faculty/<pk>/` | `faculty_detail` | `faculty_detail` | Admin: Faculty details |
| `/faculty/<pk>/edit/` | `edit_faculty` | `edit_faculty` | Admin: Edit faculty |
| `/faculty/<pk>/delete/` | `delete_faculty` | `delete_faculty` | Admin: Delete faculty |
| `/faculty/dashboard/` | `teacher_dashboard` | `teacher_dashboard` | Teacher: Dashboard |
| `/faculty/courses/` | `teacher_my_courses` | `teacher_my_courses` | Teacher: Assigned courses |
| `/faculty/courses/<id>/students/` | `teacher_course_students` | `teacher_course_students` | Teacher: Students in a course |
| `/faculty/attendance/` | `teacher_take_attendance` | `teacher_take_attendance` | Teacher: Mark attendance |
| `/faculty/marks/` | `teacher_upload_marks` | `teacher_upload_marks` | Teacher: Upload exam marks |
| `/faculty/marks/<id>/enter/` | `teacher_enter_marks` | `teacher_enter_marks` | Teacher: Enter marks for exam |
| `/faculty/notices/` | `teacher_notices` | `teacher_notices` | Teacher: View notices |
| `/faculty/notices/post/` | `teacher_post_notice` | `teacher_post_notice` | Teacher: Post a notice |
| `/faculty/students/` | `teacher_view_students` | `teacher_view_students` | Teacher: View students |
| `/faculty/students/<id>/profile/` | `teacher_student_profile` | `teacher_student_profile` | Teacher: Student profile |
| `/faculty/reports/` | `teacher_reports` | `teacher_reports` | Teacher: Performance/attendance reports |
| `/faculty/profile/` | `teacher_profile` | `teacher_profile` | Teacher: Edit profile |
| `/faculty/timetable/` | `teacher_timetable` | `teacher_timetable` | Teacher: Teaching schedule |

#### Departments App
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/departments/list/` | `DepartmentListView` | `department_list` | List departments |
| `/departments/add/` | `DepartmentCreateView` | `department_add` | Add department |
| `/departments/<pk>/edit/` | `DepartmentUpdateView` | `department_edit` | Edit department |
| `/departments/<pk>/delete/` | `DepartmentDeleteView` | `department_delete` | Delete department |

#### Courses App
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/courses/list/` | `CourseListView` | `course_list` | List courses |
| `/courses/add/` | `CourseCreateView` | `course_add` | Add course |
| `/courses/<pk>/edit/` | `CourseUpdateView` | `course_edit` | Edit course |
| `/courses/<pk>/delete/` | `CourseDeleteView` | `course_delete` | Delete course |
| `/courses/<pk>/enroll/` | `enroll_students` | `course_enroll` | Enroll students into course |

#### Attendance App
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/attendance/list/` | `attendance_list` | `attendance_list` | List attendance sessions |
| `/attendance/<pk>/detail/` | `attendance_detail` | `attendance_detail` | View attendance for a session |
| `/attendance/export/` | `attendance_export` | `attendance_export` | Export attendance as CSV |

#### Examinations App
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/examinations/list/` | `ExamListView` | `exam_list` | List all exams |
| `/examinations/add/` | `ExamCreateView` | `exam_add` | Schedule new exam |
| `/examinations/<pk>/edit/` | `ExamUpdateView` | `exam_edit` | Edit exam |
| `/examinations/<pk>/delete/` | `ExamDeleteView` | `exam_delete` | Delete exam |
| `/examinations/<pk>/results/` | `result_entry` | `result_entry` | Enter marks for an exam |
| `/examinations/<pk>/sheet/` | `result_sheet` | `result_sheet` | View result sheet |
| `/examinations/<pk>/publish/` | `publish_exam` | `exam_publish` | Publish/unpublish results |

#### Fees App (Admin + Accountant Panel)
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/fees/structures/` | `FeeStructureListView` | `fee_structure_list` | List fee structures |
| `/fees/structures/add/` | `FeeStructureCreateView` | `fee_structure_add` | Add fee structure |
| `/fees/structures/<pk>/edit/` | `FeeStructureUpdateView` | `fee_structure_edit` | Edit fee structure |
| `/fees/structures/<pk>/delete/` | `FeeStructureDeleteView` | `fee_structure_delete` | Delete fee structure |
| `/fees/payments/` | `FeePaymentListView` | `fee_payment_list` | List fee payments |
| `/fees/payments/add/` | `FeePaymentCreateView` | `fee_payment_add` | Add payment |
| `/fees/payments/<id>/download/` | `download_receipt_admin` | `fee_receipt_download_admin` | Download receipt PDF (admin) |
| `/fees/dashboard/` | `accountant_dashboard` | `accountant_dashboard` | Accountant dashboard |
| `/fees/collect/` | `accountant_collect_fees` | `accountant_collect_fees` | Collect fees from student |
| `/fees/history/` | `accountant_payment_history` | `accountant_payment_history` | Payment history |
| `/fees/receipt/<id>/` | `accountant_receipt` | `accountant_receipt` | View receipt |
| `/fees/reports/` | `accountant_reports` | `accountant_reports` | Financial reports |
| `/fees/reports/export/` | `accountant_reports_export` | `accountant_reports_export` | Export reports as CSV |
| `/fees/notices/` | `accountant_notices` | `accountant_notices` | View notices |
| `/fees/notices/post/` | `accountant_post_notice` | `accountant_post_notice` | Post a notice |
| `/fees/profile/` | `accountant_profile` | `accountant_profile` | Edit profile |

#### Timetable App
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/timetable/list/` | `TimetableListView` | `timetable_list` | List timetable entries |
| `/timetable/add/` | `TimetableCreateView` | `timetable_add` | Add timetable entry |
| `/timetable/<pk>/edit/` | `TimetableUpdateView` | `timetable_edit` | Edit entry |
| `/timetable/<pk>/delete/` | `TimetableDeleteView` | `timetable_delete` | Delete entry |

#### Notices App
| URL | View | Name | Purpose |
|-----|------|------|---------|
| `/notices/list/` | `NoticeListView` | `notice_list` | List all notices |
| `/notices/add/` | `NoticeCreateView` | `notice_add` | Create notice |
| `/notices/<pk>/delete/` | `NoticeDeleteView` | `notice_delete` | Delete notice |

---

## 7. Custom User Model & Authentication

### Why Custom User Model?
Django's default `User` model only has: `username`, `email`, `password`, `first_name`, `last_name`, `is_staff`, `is_superuser`, etc.

We needed extra fields: **`role`**, **`phone`**, **`profile_image`**. So we created a **Custom User** by extending `AbstractUser`.

### The CustomUser Model

```python
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FACULTY = "FACULTY", "Faculty"
        STUDENT = "STUDENT", "Student"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
```

**Key points:**
- Inherits ALL fields from `AbstractUser` (username, password, email, etc.)
- Adds `role` — determines which dashboard and permissions the user gets
- `TextChoices` provides an enum-like set of choices: ADMIN, FACULTY, STUDENT, ACCOUNTANT
- `profile_image` uses `ImageField` which requires the `Pillow` library
- `upload_to="profile_images/"` means images are saved in `media/profile_images/`

### How Authentication Works

1. **Login Flow:**
   - User visits `/accounts/login/`
   - `CustomLoginView` processes the form
   - "Remember Me" checkbox: if unchecked, session expires when browser closes (`set_expiry(0)`)
   - On success, `LOGIN_REDIRECT_URL` sends user to `dashboard_redirect`

2. **Dashboard Redirect:**
   ```python
   def dashboard_redirect(request):
       user = request.user
       if user.role == 'ADMIN' or user.is_superuser:
           return redirect('admin_dashboard')
       elif user.role == 'FACULTY':
           return redirect('teacher_dashboard')
       elif user.role == 'STUDENT':
           return redirect('student_dashboard')
       elif user.role == 'ACCOUNTANT':
           return redirect('accountant_dashboard')
   ```
   This function checks the user's `role` and sends them to the correct dashboard.

3. **Access Control Decorators:**
   Each panel has a custom decorator that restricts access:
   - `@admin_required` — Only ADMIN role or superuser
   - `@faculty_required` — Only users with a Faculty profile
   - `@student_required` — Only users with a Student profile
   - `@accountant_required` — Only ACCOUNTANT or ADMIN role

4. **Password Change:** Uses Django's built-in `PasswordChangeView` with a mixin to pass the correct base template.

5. **Password Reset:** Uses Django's built-in email-based password reset flow (4-step process).

---

## 8. All Models Explained

### How Django Models Map to Database Tables

Every model class → one database table.  
Every class attribute → one column in that table.  
Example: `Student` model → `students_student` table in SQLite.

### Model 1: CustomUser (accounts app)

| Field | Type | Purpose |
|-------|------|---------|
| `username` | CharField | Unique login username (inherited) |
| `password` | CharField | Hashed password (inherited) |
| `email` | EmailField | Email address (inherited) |
| `first_name` | CharField | First name (inherited) |
| `last_name` | CharField | Last name (inherited) |
| `role` | CharField (choices) | ADMIN / FACULTY / STUDENT / ACCOUNTANT |
| `phone` | CharField | Phone number |
| `profile_image` | ImageField | Profile picture |

**Relationships:** None (this is the root user model).

---

### Model 2: Department (departments app)

| Field | Type | Purpose |
|-------|------|---------|
| `name` | CharField(100) | Department name (e.g., "Computer Science") |
| `code` | CharField(10) unique | Short code (e.g., "CS") |
| `hod` | ForeignKey → Faculty | Head of Department |

**Relationships:**
- `hod` → ForeignKey to `Faculty` (meaning each department can have one HOD)
- `on_delete=SET_NULL` means if the HOD faculty is deleted, the field becomes NULL instead of deleting the department

---

### Model 3: Student (students app)

| Field | Type | Purpose |
|-------|------|---------|
| `user` | OneToOneField → CustomUser | Links to the user account |
| `enrollment_no` | CharField(20) unique | Enrollment number (also used as username) |
| `department` | ForeignKey → Department | Which department |
| `semester` | IntegerField | Current semester (1–8) |
| `admission_date` | DateField | Date of admission |

**Relationships:**
- `user` → OneToOneField (each student has exactly ONE user account, and vice versa)
- `department` → ForeignKey (many students can be in one department)

**Important:** When we access `request.user.student`, Django follows the OneToOneField to get the Student profile.

---

### Model 4: Faculty (faculty app)

| Field | Type | Purpose |
|-------|------|---------|
| `user` | OneToOneField → CustomUser | Links to the user account |
| `department` | ForeignKey → Department | Faculty's department |
| `designation` | CharField(100) | Designation (e.g., "Professor", "Assistant Professor") |
| `joining_date` | DateField | Date of joining |

**Relationships:**
- `user` → OneToOneField to CustomUser
- `department` → ForeignKey to Department

---

### Model 5: Course (courses app)

| Field | Type | Purpose |
|-------|------|---------|
| `name` | CharField(100) | Course name (e.g., "Data Structures") |
| `code` | CharField(20) unique | Course code (e.g., "CS301") |
| `department` | ForeignKey → Department | Which department offers it |
| `faculty` | ForeignKey → Faculty | Who teaches it |
| `semester` | IntegerField | Which semester (determines eligible students) |
| `credits` | IntegerField | Credit hours |
| `capacity` | IntegerField | Max students (default 60) |
| `students` | ManyToManyField → Student | Enrolled students |

**Relationships:**
- `department` → ForeignKey (one department has many courses)
- `faculty` → ForeignKey (one faculty teaches many courses)
- `students` → **ManyToManyField** (many students can enroll in many courses)

**ManyToMany explained:** Django automatically creates a junction/intermediate table `courses_course_students` with columns `course_id` and `student_id`. This allows any number of students to be enrolled in any number of courses.

---

### Model 6: Attendance (attendance app)

| Field | Type | Purpose |
|-------|------|---------|
| `course` | ForeignKey → Course | Which course |
| `date` | DateField | Date of the class |
| `marked_by` | ForeignKey → Faculty | Which faculty marked it |

**Constraint:** `unique_together = ('course', 'date')` — prevents duplicate attendance for the same course on the same date.

---

### Model 7: AttendanceRecord (attendance app)

| Field | Type | Purpose |
|-------|------|---------|
| `attendance` | ForeignKey → Attendance | Links to the attendance session |
| `student` | ForeignKey → Student | Which student |
| `status` | BooleanField | `True` = Present, `False` = Absent |

**How attendance works:**
1. One `Attendance` object = one class session (course + date)
2. Many `AttendanceRecord` objects = one per student in that session
3. This is a **one-to-many** relationship (one session has many records)

---

### Model 8: Exam (examinations app)

| Field | Type | Purpose |
|-------|------|---------|
| `course` | ForeignKey → Course | Which course |
| `exam_type` | CharField (choices) | MID / FINAL / INTERNAL |
| `total_marks` | IntegerField | Maximum marks |
| `date` | DateField | Exam date |
| `start_time` | TimeField | Start time (optional) |
| `end_time` | TimeField | End time (optional) |
| `room_number` | CharField | Room (optional) |
| `is_published` | BooleanField | Whether results are visible to students |

**`is_published`:** When False, students cannot see results. When True, results are locked (faculty cannot edit marks).

---

### Model 9: Result (examinations app)

| Field | Type | Purpose |
|-------|------|---------|
| `exam` | ForeignKey → Exam | Which exam |
| `student` | ForeignKey → Student | Which student |
| `marks_obtained` | DecimalField(5,2) | Marks scored (e.g., 87.50) |

**Relationship:** Links an Exam to a Student with their marks.

---

### Model 10: FeeStructure (fees app)

| Field | Type | Purpose |
|-------|------|---------|
| `department` | ForeignKey → Department | Which department |
| `semester` | IntegerField | Which semester |
| `amount` | DecimalField(10,2) | Fee amount |

**Purpose:** Defines how much a student in a specific department and semester should pay.

---

### Model 11: FeePayment (fees app)

| Field | Type | Purpose |
|-------|------|---------|
| `student` | ForeignKey → Student | Who paid |
| `amount_paid` | DecimalField(10,2) | Amount paid |
| `payment_date` | DateField (auto_now_add) | Auto-set to today when created |
| `status` | CharField (choices) | PAID / PENDING |
| `payment_mode` | CharField (choices) | CASH / CHEQUE / ONLINE |
| `receipt_no` | CharField unique | Auto-generated receipt number |
| `collected_by` | ForeignKey → CustomUser | Which accountant collected it |

**Auto-generated receipt:** The `save()` method auto-generates `receipt_no` using UUID:
```python
def save(self, *args, **kwargs):
    if not self.receipt_no:
        self.receipt_no = f"RCP-{uuid.uuid4().hex[:8].upper()}"
    super().save(*args, **kwargs)
```

---

### Model 12: Timetable (timetable app)

| Field | Type | Purpose |
|-------|------|---------|
| `course` | ForeignKey → Course | Which course |
| `faculty` | ForeignKey → Faculty | Who teaches |
| `day_of_week` | CharField (choices) | Monday–Sunday |
| `start_time` | TimeField | Class start time |
| `end_time` | TimeField | Class end time |
| `room_number` | CharField | Room number |

---

### Model 13: Notice (notices app)

| Field | Type | Purpose |
|-------|------|---------|
| `title` | CharField(200) | Notice title |
| `description` | TextField | Full notice content |
| `target_audience` | CharField (choices) | ALL / FACULTY / STUDENT |
| `target_course` | ForeignKey → Course | Optional course-specific notice |
| `attachment` | FileField | Optional uploaded file |
| `created_at` | DateTimeField (auto_now_add) | Auto-set timestamp |
| `posted_by` | ForeignKey → CustomUser | Who posted it |

---

### Model 14: UniversitySetting (core app) — Singleton

| Field | Type | Purpose |
|-------|------|---------|
| `university_name` | CharField | University name |
| `logo` | ImageField | University logo |
| `academic_year` | CharField | e.g., "2024-2025" |
| `current_semester` | IntegerField | Current running semester |

**Singleton Pattern:** The `save()` method ensures only ONE instance ever exists:
```python
def save(self, *args, **kwargs):
    if not self.pk and UniversitySetting.objects.exists():
        self.pk = UniversitySetting.objects.first().pk  # Overwrite existing
    super().save(*args, **kwargs)
```

---

## 9. All Views Explained

### Types of Views Used

1. **Function-Based Views (FBV)** — Regular Python functions decorated with `@login_required`
2. **Class-Based Views (CBV)** — Django classes like `ListView`, `CreateView`, `UpdateView`, `DeleteView`

### When CBV vs FBV?
- **CBV** used for simple CRUD (departments, courses, timetable, notices, fees) — less code
- **FBV** used for complex logic (attendance marking, fee collection, dashboards) — more flexibility

### Core App Views

| View | Type | Purpose |
|------|------|---------|
| `admin_dashboard` | FBV | Shows stats: total students, faculty, courses, revenue, attendance %, recent activities |
| `settings_view` | FBV | Manages university name, logo, academic year (singleton) |
| `about_university` | FBV | Public page showing university stats |
| `contact_page` | FBV | Contact form (displays success message) |
| `public_profile` | FBV | Shows any user's public profile |
| `global_search` | FBV | Searches Students, Faculty, Courses using `Q` objects |
| `custom_404` | FBV | Custom 404 error page |
| `custom_403` | FBV | Custom 403 forbidden page |

### Accounts App Views

| View | Type | Purpose |
|------|------|---------|
| `CustomLoginView` | CBV | Login with "Remember Me" — sets session expiry |
| `dashboard_redirect` | FBV | Checks role and redirects to correct dashboard |
| `profile` | FBV | Shows user profile page |
| `MainPasswordChangeView` | CBV | Password change with role-aware base template |
| `MainPasswordChangeDoneView` | CBV | Password change success page |

### Student App Views (Admin-facing)

| View | Purpose | How it works |
|------|---------|-------------|
| `student_list` | List all students | Queries `Student.objects`, supports filtering by department, semester, and search by name/enrollment |
| `student_detail` | Student's full details | Shows attendance %, results, fee status for a specific student |
| `add_student` | Create student | Creates `CustomUser` + `Student` objects, auto-generates password if needed |
| `edit_student` | Edit student | Updates user and student profile fields |
| `delete_student` | Delete student | Deletes user (cascades to student profile) |
| `promote_students` | Promote semester | Uses `F('semester') + 1` to bulk increment selected students |

### Student App Views (Student Panel)

| View | Purpose | Key Logic |
|------|---------|-----------|
| `student_dashboard` | Student home | Shows enrolled courses count, attendance %, pending fees, upcoming exams, recent results |
| `student_my_courses` | Enrolled courses | Queries courses where `students=student` |
| `student_course_detail` | Course detail | Shows attendance, results, schedule for one specific course |
| `student_my_attendance` | Attendance records | Course-wise attendance summary + detailed records with date filters |
| `student_my_results` | Exam results | Shows all results with filters; calculates average %, highest marks |
| `student_fee_status` | Fee status | Calculates total payable vs total paid → pending dues |
| `student_notices` | Notices | Shows notices targeted at ALL, STUDENT, or their enrolled courses |
| `student_timetable` | Weekly timetable | Organizes timetable entries by day of week |
| `student_profile` | Profile edit | Allows changing name, email, phone, profile image |
| `download_results_pdf` | PDF transcript | Generates PDF using `render_to_pdf` utility |
| `download_id_card_pdf` | PDF ID card | Generates student ID card PDF |
| `download_receipt_pdf` | PDF receipt | Generates fee receipt PDF for a specific payment |

### Faculty App Views (Admin-facing)

| View | Purpose |
|------|---------|
| `faculty_list` | List all faculty with department filter and search |
| `add_faculty` | Create user + faculty profile, auto-generate username and password |
| `faculty_detail` | View faculty details and assigned courses |
| `edit_faculty` | Update faculty information |
| `delete_faculty` | Delete faculty (cascades from user deletion) |

### Faculty App Views (Teacher Panel)

| View | Purpose | Key Logic |
|------|---------|-----------|
| `teacher_dashboard` | Teacher home | Shows course count, student count, pending grading, today's schedule |
| `teacher_my_courses` | Assigned courses | Lists courses where `faculty=faculty` |
| `teacher_course_students` | Students in a course | Shows enrolled students for a course |
| `teacher_timetable` | Teaching schedule | Organizes by day of week |
| `teacher_take_attendance` | Mark attendance | GET: loads student list; POST: creates `Attendance` + `AttendanceRecord` |
| `teacher_upload_marks` | View exams | Lists exams for faculty's courses |
| `teacher_enter_marks` | Enter marks | Creates/updates `Result` objects; blocked if exam is published |
| `teacher_notices` | View notices | Shows notices posted by self or targeted at ALL/FACULTY |
| `teacher_post_notice` | Post notice | Creates `Notice` object with optional course targeting |
| `teacher_view_students` | All students | Shows students across all assigned courses |
| `teacher_student_profile` | Student profile | Shows attendance + results for a specific student in faculty's courses |
| `teacher_reports` | Reports | Generates attendance or performance reports for a course |
| `teacher_profile` | Profile edit | Allows editing personal info |

### Department & Course Views (All CBVs)

| View | Type | Django Generic View |
|------|------|-------------------|
| `DepartmentListView` | CBV | `ListView` — auto-queries all departments |
| `DepartmentCreateView` | CBV | `CreateView` — auto-generates form and saves |
| `DepartmentUpdateView` | CBV | `UpdateView` — auto-loads, edits, saves |
| `DepartmentDeleteView` | CBV | `DeleteView` — confirms and deletes |
| `CourseListView/Create/Update/Delete` | CBV | Same pattern as departments |
| `enroll_students` | FBV | Shows eligible students (same dept + semester), adds them via `course.students.add()` |

### Attendance App Views

| View | Purpose |
|------|---------|
| `attendance_list` | Lists attendance sessions with role-based filtering |
| `attendance_detail` | Shows individual records (who was present/absent) |
| `attendance_export` | Exports attendance as CSV file |

### Examinations App Views

| View | Type | Purpose |
|------|------|---------|
| `ExamListView` | CBV | List all exams |
| `ExamCreateView` | CBV | Schedule new exam (uses `ExamForm`) |
| `ExamUpdateView` | CBV | Edit exam |
| `ExamDeleteView` | CBV | Delete exam |
| `result_entry` | FBV | Enter marks for all students in an exam |
| `result_sheet` | FBV | View result sheet for an exam |
| `publish_exam` | FBV | Toggle `is_published` flag |

### Fees App Views (Accountant Panel)

| View | Purpose | Key Logic |
|------|---------|-----------|
| `accountant_dashboard` | Dashboard | Total collected, pending, monthly bar chart, recent payments |
| `accountant_collect_fees` | Collect fees | Search student → show fee info → record payment with overpayment validation |
| `accountant_payment_history` | History | Searchable and filterable payment list |
| `accountant_receipt` | View receipt | Shows formatted receipt for a payment |
| `accountant_reports` | Financial reports | Monthly, Annual, Department-wise reports |
| `accountant_reports_export` | Export CSV | Exports financial reports as CSV |
| `accountant_notices` | View notices | Filter by ALL or own notices |
| `accountant_post_notice` | Post notice | Create notice |
| `download_receipt_admin` | PDF receipt | Generate PDF receipt |
| `accountant_profile` | Profile edit | Edit personal info |

---

## 10. Forms Explained

### What are Django Forms?
Forms validate user input before saving to database. Django can auto-generate forms from models.

### ExamForm (`examinations/forms.py`)

```python
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'exam_type', 'total_marks', 'date', 
                  'start_time', 'end_time', 'room_number', 'is_published']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            ...
        }
```
- `ModelForm` auto-generates form fields from the `Exam` model
- `widgets` dictionary customizes how each field renders (HTML attributes)
- `'type': 'date'` gives a native date picker in the browser

### TimetableForm (`timetable/forms.py`) — With Clash Detection!

```python
class TimetableForm(forms.ModelForm):
    def clean(self):
        # Validates 3 things:
        # 1. End time must be after start time
        # 2. Faculty is not double-booked (same day, overlapping time)
        # 3. Room is not double-booked
        # 4. Course is not double-scheduled
        
        overlap_query = Timetable.objects.filter(
            day_of_week=day,
            start_time__lt=end,   # existing starts before new ends
            end_time__gt=start    # existing ends after new starts
        )
```
- `clean()` is called automatically during form validation
- Uses **overlap detection**: checks if `existing.start < new.end AND existing.end > new.start`
- Prevents scheduling conflicts for faculty, rooms, and courses

---

## 11. Templates & Frontend

### Template Hierarchy

```
templates/
├── base.html                      ← Admin panel master layout
├── student/
│   └── base_student.html         ← Student panel master layout
├── teacher/
│   └── base_teacher.html         ← Teacher panel master layout
├── accountant/
│   └── base_accountant.html      ← Accountant panel master layout
├── includes/
│   ├── sidebar.html              ← Admin sidebar navigation
│   └── navbar.html               ← Top navbar with search, profile
└── registration/
    ├── login.html                ← Login page
    └── password_change_form.html ← Password change page
```

### Template Inheritance
Django uses **template inheritance** to avoid repeating HTML:

```
base.html (master layout)
  │
  ├── {% block title %}{% endblock %}       ← Page title
  ├── {% block extra_css %}{% endblock %}   ← Extra CSS
  ├── {% include 'includes/sidebar.html' %} ← Sidebar
  ├── {% include 'includes/navbar.html' %}  ← Navbar
  ├── {% block content %}{% endblock %}     ← Main content
  └── {% block extra_js %}{% endblock %}    ← Extra JS
```

Child templates "extend" the base:
```html
{% extends "base.html" %}
{% block content %}
  <h1>Student List</h1>
  ...actual page content...
{% endblock %}
```

### Django Template Tags Used

| Tag | Purpose | Example |
|-----|---------|---------|
| `{% extends %}` | Inherit from parent template | `{% extends "base.html" %}` |
| `{% block %}` | Define overridable sections | `{% block content %}...{% endblock %}` |
| `{% include %}` | Include another template | `{% include 'includes/sidebar.html' %}` |
| `{{ variable }}` | Output a variable | `{{ student.enrollment_no }}` |
| `{% for %}` | Loop | `{% for s in students %}...{% endfor %}` |
| `{% if %}` | Conditional | `{% if user.role == 'ADMIN' %}...{% endif %}` |
| `{% url 'name' %}` | Generate URL from name | `{% url 'student_detail' pk=student.id %}` |
| `{% csrf_token %}` | CSRF protection token | Required inside every `<form>` |
| `{% load %}` | Load template tag library | `{% load core_extras %}` |
| `{{ form.field\|addclass:"form-control" }}` | Custom filter | Adds CSS class to form field |
| `{% messages %}` | Display flash messages | Success/error notifications |

### Custom Template Tags (`core/templatetags/core_extras.py`)

1. **`addclass` filter:** Adds a CSS class to a form field widget
   ```html
   {{ form.email|addclass:"form-control" }}
   ```

2. **`get_item` filter:** Gets a value from a dictionary by key
   ```html
   {{ my_dict|get_item:key }}
   ```

---

## 12. Utility Functions

### File: `core/utils.py`

#### 1. `render_to_pdf(template_src, context_dict)`
```python
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)           # Load HTML template
    html = template.render(context_dict)            # Render with data
    result = BytesIO()                               # In-memory buffer
    pdf = pisa.pisaDocument(                         # Convert HTML → PDF
        BytesIO(html.encode("UTF-8")), result
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
```
- Uses **xhtml2pdf** library (alias: `pisa`)
- Takes a Django template path and context data
- Renders HTML first, then converts to PDF
- Returns PDF as HTTP response with `application/pdf` content type

#### 2. `log_activity(user, obj, action_flag, message)`
```python
def log_activity(user, obj, action_flag, message=''):
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=message
    )
```
- Logs admin activities to Django's built-in `LogEntry` table
- Used to show "Recent Activities" on admin dashboard
- `content_type_id` tells Django what type of object was modified

---

## 13. Admin Panel Configuration

### What is Django Admin?
Django automatically provides a `/admin/` web interface for managing database records. We customize it in each app's `admin.py`.

### CustomUser Admin
```python
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone', 'profile_image')}),
    )
```
- `list_display` — columns shown in the list view
- `list_filter` — sidebar filters
- `search_fields` — searchable columns
- `fieldsets` — adds our custom fields to the edit form

### Student Admin
```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_no', 'user', 'department', 'semester', 'admission_date')
    list_filter = ('department', 'semester')
    raw_id_fields = ('user',)  # Shows user selection as ID input, not dropdown
```

### Course Admin
```python
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('students',)  # Nice widget for ManyToMany selection
```

### UniversitySetting Admin (Singleton)
```python
class UniversitySettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if UniversitySetting.objects.exists():
            return False  # Can't add more than one
        return super().has_add_permission(request)
```

---

## 14. Role-Based Access Control

### How Access is Restricted

| Mechanism | Where Used | How It Works |
|-----------|-----------|-------------|
| `@login_required` | All views | Django decorator — redirects to login if not authenticated |
| `@admin_required` | Core app views | Custom decorator — checks `role == 'ADMIN'` or `is_superuser` |
| `@faculty_required` | Faculty panel views | Custom decorator — checks `hasattr(user, 'faculty')` |
| `@student_required` | Student panel views | Custom decorator — checks `hasattr(user, 'student')` |
| `@accountant_required` | Accountant panel views | Custom decorator — checks `role in ('ACCOUNTANT', 'ADMIN')` |
| `LoginRequiredMixin` | CBVs | Class-based equivalent of `@login_required` |
| `UMBaseTemplateMixin` | Password change views | Determines correct base template by role |

### How Each Decorator Works (Example)

```python
def student_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'student'):
            messages.error(request, 'Access denied. Student account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
```
1. First, `@login_required` ensures user is logged in
2. Then checks if user has a `student` attribute (OneToOneField creates this)
3. If yes, allows access. If no, shows error and redirects to login.

### Security Summary

| URL Pattern | Who Can Access |
|------------|---------------|
| `/dashboard/admin/` | Admin only |
| `/students/dashboard/` | Students only |
| `/faculty/dashboard/` | Faculty only |
| `/fees/dashboard/` | Accountant or Admin |
| `/departments/`, `/courses/`, `/examinations/`, `/timetable/`, `/notices/` | Any logged-in user (admin-facing) |
| `/about/`, `/contact/` | Anyone (public) |
| `/students/list/`, `/faculty/list/` | Any logged-in user (meant for admin) |

---

## 15. Complete Data Flow Examples

### Flow 1: Adding a New Student (Admin)

```
1. Admin clicks "Add Student" → GET /students/add/
2. Django calls add_student() view
3. View renders add_student.html with department list
4. Admin fills the form and clicks Submit → POST /students/add/
5. View receives POST data:
   - Creates CustomUser with role=STUDENT
   - Sets password (auto-generated or manual)
   - Uploads profile image if provided
   - Creates Student object linked to USER via OneToOneField
   - Logs the activity using log_activity()
6. Redirects to /students/list/ with success message
```

### Flow 2: Faculty Marks Attendance

```
1. Faculty goes to /faculty/attendance/ (GET)
2. teacher_take_attendance() shows courses taught by this faculty
3. Faculty selects a course and date → GET /faculty/attendance/?course=5&date=2026-02-20
4. View loads enrolled students for that course
5. View checks if attendance already exists for that date (unique_together constraint)
6. Faculty checks checkboxes for present students → POST
7. View creates:
   a. Attendance object (course + date + marked_by)
   b. AttendanceRecord per student (status=True/False)
8. If attendance already existed, old records are deleted and recreated
9. Redirects with success message
```

### Flow 3: Accountant Collects Fees

```
1. Accountant visits /fees/collect/
2. Searches for student by name or enrollment number
3. View shows matching students
4. Accountant selects a student → loads fee info:
   - Total payable (from FeeStructure matching department + semester)
   - Total paid so far (sum of PAID FeePayments)
   - Pending dues = total payable - total paid
5. Accountant enters amount and payment mode → POST
6. View validates:
   - Amount > 0
   - Amount ≤ pending dues (prevents overpayment)
7. Creates FeePayment with:
   - Auto-generated receipt_no (RCP-XXXXXXXX)
   - collected_by = current user
   - status = PAID
8. Redirects to receipt page showing the payment details
```

### Flow 4: Student Views Results

```
1. Student visits /students/results/
2. student_my_results() view:
   a. Gets student from request.user.student (OneToOneField)
   b. Queries Result objects where student=this_student
   c. Filters by course and exam_type if specified
   d. Calculates summary: total exams, avg %, highest, passed count
3. Renders student/my_results.html with results list and summary
4. Student can also click "Download PDF" → /students/results/download/
5. download_results_pdf() generates PDF using xhtml2pdf
```

### Flow 5: Timetable Creation with Clash Detection

```
1. Admin visits /timetable/add/
2. TimetableCreateView shows form (TimetableForm)
3. Admin fills: course, faculty, day, start_time, end_time, room
4. On submit, TimetableForm.clean() runs validation:
   a. Checks end_time > start_time
   b. Queries existing timetables for same day with overlapping times
   c. Checks if selected faculty is already busy → Error
   d. Checks if selected room is already booked → Error
   e. Checks if course is already scheduled → Error
5. If no clashes: saves and redirects with success
6. If clash detected: shows form with specific error messages
```

---

## 16. Database Relationships

### Entity-Relationship Diagram (Text)

```
                    ┌──────────────┐
                    │  CustomUser  │
                    │──────────────│
                    │ username     │
                    │ password     │
                    │ email        │
                    │ role         │
                    │ phone        │
                    │ profile_image│
                    └──────┬───┬──┘
                  1:1 ↙         ↘ 1:1
           ┌──────────┐      ┌──────────┐
           │  Student  │      │ Faculty  │
           │──────────│      │──────────│
           │enroll_no │      │designat. │
           │semester  │      │join_date │
           │admission │      └────┬─────┘
           └────┬─────┘           │
                │                 │ FK
     FK ↙       │ M2M             ↓
┌────────────┐  │         ┌──────────┐
│ Department │←─┼────FK───│  Course   │
│────────────│  │         │──────────│
│ name       │  └────────▶│ students │←── M2M
│ code       │            │ faculty  │←── FK
│ hod ──────FK──────────▶ │ semester │
└────────────┘            └────┬─────┘
                               │ FK
              ┌────────────────┼────────────────┐
              ↓                ↓                ↓
      ┌──────────────┐  ┌──────────┐   ┌───────────┐
      │  Attendance  │  │   Exam   │   │ Timetable │
      │──────────────│  │──────────│   │───────────│
      │ course (FK)  │  │course FK │   │ course FK │
      │ date         │  │ type     │   │faculty FK │
      │ marked_by FK │  │ marks    │   │ day       │
      └──────┬───────┘  │is_publis.│   │ time      │
             │          └────┬─────┘   │ room      │
             ↓               ↓         └───────────┘
    ┌────────────────┐ ┌──────────┐
    │AttendanceRecord│ │  Result  │
    │────────────────│ │──────────│
    │ attend. (FK)   │ │ exam FK  │
    │ student (FK)   │ │student FK│
    │ status (bool)  │ │ marks    │
    └────────────────┘ └──────────┘

      ┌───────────────┐   ┌───────────────┐   ┌────────────────┐
      │ FeeStructure  │   │  FeePayment   │   │    Notice      │
      │───────────────│   │───────────────│   │────────────────│
      │ dept (FK)     │   │ student (FK)  │   │ title          │
      │ semester      │   │ amount        │   │ description    │
      │ amount        │   │ status        │   │ target_audience│
      └───────────────┘   │ mode          │   │ target_course  │
                          │ receipt_no    │   │ attachment     │
                          │ collected_by  │   │ posted_by (FK) │
                          └───────────────┘   └────────────────┘

      ┌──────────────────┐
      │UniversitySetting │  (Singleton — only 1 row)
      │──────────────────│
      │ university_name  │
      │ logo             │
      │ academic_year    │
      │ current_semester │
      └──────────────────┘
```

### Relationship Types Summary

| Relationship | Type | Meaning |
|-------------|------|---------|
| CustomUser ↔ Student | One-to-One | Each student has exactly one user account |
| CustomUser ↔ Faculty | One-to-One | Each faculty has exactly one user account |
| Department → Faculty (hod) | FK (Many-to-One) | A department has one HOD |
| Student → Department | FK | Many students belong to one department |
| Faculty → Department | FK | Many faculty belong to one department |
| Course → Department | FK | Many courses belong to one department |
| Course → Faculty | FK | Many courses are taught by one faculty |
| Course ↔ Student | Many-to-Many | Many students enroll in many courses |
| Attendance → Course | FK | Many attendance sessions per course |
| AttendanceRecord → Attendance | FK | Many records per session |
| AttendanceRecord → Student | FK | Many records per student |
| Exam → Course | FK | Many exams per course |
| Result → Exam + Student | FK + FK | Links exam to student with marks |
| FeeStructure → Department | FK | Fee rates per department |
| FeePayment → Student | FK | Many payments per student |
| Notice → CustomUser (posted_by) | FK | Who posted the notice |
| Notice → Course (target_course) | FK | Optional course targeting |
| Timetable → Course + Faculty | FK + FK | Schedule entry |

---

## 17. PDF Generation

### How PDFs are Created

1. **Library used:** `xhtml2pdf` (imported as `pisa`)
2. **Process:**
   ```
   HTML Template → Django renders with data → xhtml2pdf converts to PDF → HTTP Response
   ```
3. **Function:** `render_to_pdf()` in `core/utils.py`

### PDFs Generated in the System

| PDF | Template | Generated By |
|-----|----------|-------------|
| Student Transcript | `student/my_results_pdf.html` | `download_results_pdf` view |
| Student ID Card | `student/id_card_pdf.html` | `download_id_card_pdf` view |
| Fee Receipt (Student) | `student/receipt_pdf.html` | `download_receipt_pdf` view |
| Fee Receipt (Admin) | `student/receipt_pdf.html` | `download_receipt_admin` view |

### ID Card Validity Calculation
```python
expire_year = student.admission_date.year + 4
expire_date = student.admission_date.replace(year=expire_year)
```
ID card is valid for 4 years from admission date.

---

## 18. Key Design Patterns Used

### 1. Singleton Pattern — `UniversitySetting`
Only one configuration record exists. The `save()` method overwrites the existing record.

### 2. Decorator Pattern — Access Control
Custom decorators (`admin_required`, `faculty_required`, etc.) wrap view functions to add access control logic.

### 3. Template Inheritance — Layout Reuse
`base.html` provides common layout. All pages extend it and override specific blocks.

### 4. Mixin Pattern — `UMBaseTemplateMixin`
A class that adds role-aware `base_template` context to CBVs. Used with password change views.

### 5. Repository Pattern (via ORM)
Django's ORM abstracts database queries. Instead of SQL, we write Python:
```python
# Instead of: SELECT * FROM students WHERE department_id = 1
Student.objects.filter(department_id=1)

# Instead of: SELECT COUNT(*) FROM attendance_record WHERE status = 1
AttendanceRecord.objects.filter(status=True).count()
```

### 6. Auto-generated Receipt Numbers
```python
receipt_no = f"RCP-{uuid.uuid4().hex[:8].upper()}"
```
Uses UUID (Universally Unique Identifier) to generate unique receipt numbers like `RCP-A1B2C3D4`.

---

### Quick Glossary

| Term | Meaning |
|------|---------|
| **ORM** | Object-Relational Mapping — Python classes represent database tables |
| **CRUD** | Create, Read, Update, Delete — basic database operations |
| **FK** | ForeignKey — a reference to another table |
| **M2M** | ManyToManyField — junction table relationship |
| **CBV** | Class-Based View |
| **FBV** | Function-Based View |
| **CSRF** | Cross-Site Request Forgery — a web security attack |
| **MVT** | Model-View-Template — Django's architecture pattern |
| **SSR** | Server-Side Rendering — HTML generated on server |
| **UUID** | Universally Unique Identifier — unique random string |
| **Decorator** | A function that wraps another function to add behavior |
| **Mixin** | A class that adds functionality to other classes via inheritance |
| **Middleware** | Code that runs on every request/response |
| **Migration** | Auto-generated file that tracks database schema changes |
| **Singleton** | Design pattern ensuring only one instance exists |
| **Context** | Dictionary of data passed from view to template |
| **QuerySet** | Django's lazy database query object |

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