# Admin Panel User Guide - University Management System

## Overview
The Admin Panel provides a comprehensive interface for university administrators to manage students, faculty, courses, departments, exams, fees, and more.

## Access
- **URL**: `/accounts/login/`
- **Default Credentials** (if created via script): `admin` / `adminpassword`

## Key Features & How to Use

### 1. Dashboard
- **Overview**: View total count of students, teachers, courses, and revenue.
- **Recent Activity**: detailed log of admin actions.

### 2. Student Management (`/students/`)
- **List View**: See all enrolled students.
- **Add Student**: Register a new student. Auto-generate password option available.
- **Student Profile**: Click the "Eye" icon to view detailed profile, including:
    - Personal Information
    - Attendance Statistics (Visual cards)
    - Fee Status (Due/Cleared)
    - Exam Results History

### 3. Faculty Management (`/faculty/`)
- **List View**: Manage faculty members.
- **Add Faculty**: Onboard new teachers.

### 4. Academic Structure
- **Departments (`/departments/`)**: CRUD operations for university departments.
- **Courses (`/courses/`)**: Manage courses, assign faculty, and set capacity.

### 5. Examination & Results (`/examinations/`)
- **Schedule Exam**: Set dates, times, and rooms for exams.
- **Enter Results**: Click "Award Icon" on an exam to enter marks for all enrolled students in bulk.

### 6. Attendance Tracking (`/attendance/`)
- **Overview**: View all attendance records.
- **Filter**: Filter by Course and Date to find specific records.
- **Details**: View present/absent status for each student in a class.

### 7. Fee Management (`/fees/`)
- **Fee Structures**: Define fees for specific Departments and Semesters.
- **Record Payment**: Log student fee payments.
- **Status**: System automatically calculates pending dues based on structures vs payments.

### 8. Communication (`/notices/`)
- **Post Notice**: Create announcements for Students, Faculty, or Everyone.
- **Attachments**: Support for file uploads (e.g., PDF circulars).

### 9. Settings (`/settings/`)
- **Configure**: Update University Name, Academic Year, Semester, and Logo.

## Technical Notes
- **Authentication**: Role-based redirection is implemented. Admins go to Admin Dashboard.
- **Security**: All views are protected with `@login_required` or `LoginRequiredMixin`.
- **UI**: Built with Bootstrap 5 and Bootstrap Icons for a clean, responsive interface.
