# University Management System - Architecture & Implementation Plan

## 1. App Structure

The project follows a clean, modular structure with the following apps:
- `accounts`
- `students`
- `faculty`
- `departments`
- `courses`
- `attendance`
- `examinations`
- `fees`
- `timetable`

This structure is robust and suitable for a college-level project.

---

## 2. Role Architecture (Important)

There are 3 main roles:
1.  **Admin**
2.  **Faculty**
3.  **Student**

**Implementation Strategy:**
-   Use a **Custom User model** in `accounts`.
-   Add a `role` field (choices: `ADMIN`, `FACULTY`, `STUDENT`).

---

## 3. Feature Distribution by App

### 1️⃣ accounts
**Purpose:** Authentication & role management

**Models:**
-   `CustomUser` (AbstractUser)
    -   `role`
    -   `phone`
    -   `profile_image`

**Features:**
-   Login / Logout
-   Role-based dashboard redirect
-   Permission restriction

### 2️⃣ departments
**Models:**
-   `Department`
    -   `name`
    -   `code`
    -   `hod` (FK to Faculty)

### 3️⃣ students
**Models:**
-   `Student`
    -   `user` (OneToOne → CustomUser)
    -   `enrollment_no`
    -   `department` (FK)
    -   `semester`
    -   `admission_date`

**Features:**
-   View profile
-   View attendance
-   View timetable
-   View results
-   View fees status

### 4️⃣ faculty
**Models:**
-   `Faculty`
    -   `user` (OneToOne → CustomUser)
    -   `department` (FK)
    -   `designation`
    -   `joining_date`

**Features:**
-   Mark attendance
-   Upload exam marks
-   View timetable
-   View assigned courses

### 5️⃣ courses
**Models:**
-   `Course`
    -   `name`
    -   `code`
    -   `department` (FK)
    -   `faculty` (FK)
    -   `semester`
    -   `credits`

**Relationships:**
-   Many students can enroll in one course.
-   Use `ManyToMany` (Student ↔ Course).

### 6️⃣ timetable 🔥
**Models:**
-   `Timetable`
    -   `course` (FK)
    -   `faculty` (FK)
    -   `day_of_week`
    -   `start_time`
    -   `end_time`
    -   `room_number`

**Features:**
-   Students see timetable (based on enrolled courses).
-   Faculty see their teaching schedule.

### 7️⃣ attendance 🔥
**Models:**
-   `Attendance`
    -   `course` (FK)
    -   `date`
    -   `marked_by` (Faculty FK)
-   `AttendanceRecord`
    -   `attendance` (FK)
    -   `student` (FK)
    -   `status` (Present / Absent)

**Flow:**
1.  Faculty selects course.
2.  System shows enrolled students.
3.  Faculty marks attendance.
4.  Students can view attendance %.

**Important Validation:**
-   Prevent duplicate attendance for same course + date.

### 8️⃣ examinations
**Models:**
-   `Exam`
    -   `course` (FK)
    -   `exam_type` (Mid, Final, Internal)
    -   `total_marks`
    -   `date`
-   `Result`
    -   `exam` (FK)
    -   `student` (FK)
    -   `marks_obtained`

**Features:**
-   Faculty enters marks.
-   Students view results.

### 9️⃣ fees
**Models:**
-   `FeeStructure`
    -   `department`
    -   `semester`
    -   `amount`
-   `FeePayment`
    -   `student` (FK)
    -   `amount_paid`
    -   `payment_date`
    -   `status` (Paid / Pending)

**Validation:**
-   Prevent negative amount.
-   Prevent overpayment.

---

## 🔥 System Flow (How Everything Connects)

This represents the complete academic cycle:

1.  **Department** created/managed.
2.  **Faculty & Students** added to system.
3.  **Courses** assigned to **Faculty**.
4.  **Students** enroll in **Courses**.
5.  **Timetable** auto-generated or linked from Course.
6.  **Faculty** marks **Attendance**.
7.  **Faculty** enters **Exam Marks**.
8.  **Students** view Attendance + Results + Fees.
