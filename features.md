# University Management System - Feature Specification

## 1. Common Features (Available to All Roles)

These features are accessible to every logged-in user.

### Authentication (Accounts)
- Login
- Logout
- Change password
- View profile
- Edit own profile (limited fields)

### Dashboard
- Role-based dashboard
- Basic stats (depending on role)

---

## 2. Student Features

Students have **read-only** access with limited interaction capabilities.

### 📌 Profile
- View personal details
- View department & semester

### 📌 Courses
- View enrolled courses

### 📌 Timetable
- View personal timetable (based on enrolled courses)

### 📌 Attendance
- View attendance percentage
- View subject-wise attendance

### 📌 Examinations
- View exam schedule
- View results / marks

### 📌 Fees
- View fee structure
- View payment status
- View payment history

### ❌ Restrictions (Cannot)
- Mark attendance
- Edit marks
- Create courses
- Modify timetable

---

## 3. Faculty Features

Faculty members have academic control features.

### 📌 Profile
- View & edit limited personal info

### 📌 Courses
- View assigned courses

### 📌 Timetable
- View teaching schedule

### 📌 Attendance (Important)
- Mark attendance for assigned course
- Edit attendance (same day only — optional rule)
- View attendance reports

### 📌 Examinations
- Create exams (for assigned course)
- Enter marks
- Update marks (before result lock)

### ❌ Restrictions (Cannot)
- Create departments
- Create students
- Assign other faculty
- Modify fee structure

---

## 4. Admin Features (Full Control)

Admins have full control over the entire system (Superuser level).

### 📌 Department Management
- Add / Edit / Delete department
- Assign HOD

### 📌 Student Management
- Add student
- Assign department
- Promote semester
- Enroll in courses

### 📌 Faculty Management
- Add faculty
- Assign department
- Assign courses

### 📌 Course Management
- Create course
- Assign faculty
- Assign semester

### 📌 Timetable Management
- Create timetable slots
- Assign room
- Prevent clashes

### 📌 Attendance
- View all attendance
- Generate reports

### 📌 Examinations
- Create exam types
- Lock results
- Generate final results

### 📌 Fees
- Create fee structure
- View all payments
- Update payment status

### 📌 Reports
- Attendance report
- Result report
- Fee report
- Student list

---

## 🔥 Quick Summary Table

| Feature | Admin | Faculty | Student |
| :--- | :---: | :---: | :---: |
| **Login** | ✅ | ✅ | ✅ |
| **View Profile** | ✅ | ✅ | ✅ |
| **Manage Departments** | ✅ | ❌ | ❌ |
| **Manage Students** | ✅ | ❌ | ❌ |
| **Manage Faculty** | ✅ | ❌ | ❌ |
| **Create Courses** | ✅ | ❌ | ❌ |
| **View Courses** | ✅ | ✅ | ✅ |
| **Timetable View** | ✅ | ✅ | ✅ |
| **Create Timetable** | ✅ | ❌ | ❌ |
| **Mark Attendance** | ❌ | ✅ | ❌ |
| **View Attendance** | ✅ | ✅ | ✅ |
| **Create Exam** | ✅ | ✅ | ❌ |
| **Enter Marks** | ❌ | ✅ | ❌ |
| **View Results** | ✅ | ❌ | ✅ |
| **Manage Fees** | ✅ | ❌ | ❌ |
| **View Fees** | ✅ | ❌ | ✅ |
