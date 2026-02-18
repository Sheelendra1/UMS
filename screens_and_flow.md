# University Management System - Screen Estimates & Flow

## ✅ Total Estimated Screens

| Module | Pages |
| :--- | :---: |
| **Authentication** | 4 |
| **Admin Panel** | 14 |
| **Teacher Panel** | 8 |
| **Student Panel** | 7 |
| **Accountant Panel** | 6 |
| **Common Pages** | 5 |
| **Total** | **≈ 44 Screens** |

This satisfies the requirement for a solid full system — not too small, not overly complex.

---

## 🔐 1. Authentication Module (4 Pages)

### 1 Login Page
- Username / Email input
- Password input
- "Remember me" checkbox
- "Forgot password?" link
- Role-based redirect logic

### 2 Forgot Password
- Email input field
- "Send Reset Link" button
- Navigation back to Login

### 3 Change Password
- Old password input
- New password input
- Confirm password input
- Save/Update button

---

## 👨‍💼 2. Admin Panel (14 Pages)

###  1. Admin Dashboard
- **Stats Cards:**
  - Total students
  - Total teachers
  - Total courses
  - Attendance percentage
  - Total revenue
- **Widgets:**
  - Recent activities log
  - Quick actions

###  2. Add Student Page
- Full name
- Email address
- Enrollment number
- Department selection
- Course selection
- Year/Semester
- Fee structure assignment
- Profile picture upload
- Auto-generate password toggle

###  3. Student List Page
- Search bar (by name, ID)
- Filter by department
- Filter by year/semester
- **Actions:** View profile, Edit, Delete, Activate/Deactivate account

###  4. Student Profile Page
- Personal details view
- Attendance summary visualization
- Result summary
- Fee status overview
- Edit profile button

###  5. Add Teacher
- Name
- Email
- Department selection
- Assign subjects/courses
- Auto-generate password toggle

###  6. Teacher List
- Search and filter options
- **Actions:** Edit, Delete, View profile
- Assign courses to teacher

###  7. Course Management
- Add new course
- Assign teacher to course
- Set student capacity
- Edit/Delete existing courses

###  8. Department Management
- Create new department
- Assign Head of Department (HOD)
- Edit/Delete departments

###  9. Attendance Overview
- View class-wise attendance records
- Filter by design/date range
- Export attendance report (PDF/Excel)

###  10. Exam Management
- Create new exam
- Assign course to exam
- Set exam date and time
- Manage exam halls/seats

###  11. Results Management
- Enter student marks
- Publish/Unpublish results
- Edit marks
- Generate result sheets

###  12. Fee Management
- View all payment records
- Track pending dues
- Generate fee receipts
- Manage fee structures

###  13. Notice Management
- Create new notice
- Select target audience (All, Teachers, Students)
- Edit/Delete notices

###  14. System Settings
- Configure Academic Year
- Semester configuration
- University logo upload
- General application settings

---

## 👩‍🏫 3. Teacher Panel (8 Pages)

###  1. Teacher Dashboard
- Assigned courses list
- Today's schedule
- Quick attendance shortcut
- Pending grading tasks

###  2. My Courses
- View assigned courses details
- Student list per course

###  3. Take Attendance
- Select Course and Date
- List of students with Present/Absent toggle
- Submit attendance

###  4. Upload Marks
- Select exam/assessment
- Enter marks for students
- Edit previously entered marks

###  5. Post Notice
- Create notice for specific classes
- View posted notices

###  6. View Students
- List of students in assigned classes
- View basic student profiles

###  7. Reports
- Class performance report
- Student attendance report

###  8. Profile Page
- Update personal profile
- Change password

---

## 👨‍🎓 4. Student Panel (7 Pages)

###  1. Student Dashboard
- Summary of enrolled courses
- Overall attendance percentage
- Upcoming exams schedule
- Current fee status

###  2. My Courses
- Detailed view of enrolled courses
- Teacher contact info per course
- Syllabus/Materials download

###  3. My Attendance
- View daily/monthly attendance
- Filter by subject
- Attendance percentage visualizer

###  4. My Results
- List of past exams
- View marks/grades
- Download result card/transcript

###  5. Fee Status
- View total fee amount
- View paid amount
- View pending dues
- Download payment receipts

###  6. Notices
- View general announcements
- View class-specific notices

###  7. Profile Page
- Update contact info
- Change password

---

## 💰 5. Accountant Panel (6 Pages)

###  1. Accountant Dashboard
- Total fees collected stats
- Pending dues stats
- Monthly revenue chart/graph

###  2. Collect Fees
- Search student by ID/Name
- Enter payment amount
- Select payment mode (Cash/Cheque/Online)
- Generate and print receipt

###  3. Payment History
- List of recent transactions
- Filter by date range
- Filter by student

###  4. Financial Reports
- Generate monthly collection report
- Generate annual financial summary
- Export options

###  5. Notices
- View finance-related notices
- Post finance-related announcements (optional)

###  6. Profile
- Update personal info
- Change password

---

## 🌐 6. Common Pages (5 Pages)
- **404 Page** (Not Found)
- **Access Denied Page** (403 Forbidden)
- **Public Profile Page** (for external viewing, if applicable)
- **About University Page**
- **Contact Page**

---

## 🧠 Structural Navigation Flow

`mermaid
graph TD
    A[Login] --> B{Role Check}
    B -->|Admin| C[Admin Dashboard]
    B -->|Teacher| D[Teacher Dashboard]
    B -->|Student| E[Student Dashboard]
    B -->|Accountant| F[Accountant Dashboard]
    
    C --> G[Sidebar Navigation]
    D --> G
    E --> G
    F --> G
`

*Each role sees a different set of sidebar menu items corresponding to their access rights.*

---

## 🎯 Final Structure Summary

| Role | Screens |
| :--- | :---: |
| **Admin** | 14 |
| **Teacher** | 8 |
| **Student** | 7 |
| **Accountant** | 6 |
| **Auth** | 4 |
| **Common** | 5 |
