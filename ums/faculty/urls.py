from django.urls import path
from . import views

urlpatterns = [
    # ── Admin-facing routes ────────────────────────────
    path('list/', views.faculty_list, name='faculty_list'),
    path('add/', views.add_faculty, name='add_faculty'),
    path('<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('<int:pk>/edit/', views.edit_faculty, name='edit_faculty'),
    path('<int:pk>/delete/', views.delete_faculty, name='delete_faculty'),

    # ── Teacher Panel (8 pages) ────────────────────────
    # 1. Dashboard
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # 2. My Courses
    path('courses/', views.teacher_my_courses, name='teacher_my_courses'),
    path('courses/<int:course_id>/students/', views.teacher_course_students, name='teacher_course_students'),

    # 3. Take Attendance
    path('attendance/', views.teacher_take_attendance, name='teacher_take_attendance'),

    # 4. Upload Marks
    path('marks/', views.teacher_upload_marks, name='teacher_upload_marks'),
    path('marks/<int:exam_id>/enter/', views.teacher_enter_marks, name='teacher_enter_marks'),

    # 5. Notices
    path('notices/', views.teacher_notices, name='teacher_notices'),
    path('notices/post/', views.teacher_post_notice, name='teacher_post_notice'),

    # 6. View Students
    path('students/', views.teacher_view_students, name='teacher_view_students'),
    path('students/<int:student_id>/profile/', views.teacher_student_profile, name='teacher_student_profile'),

    # 7. Reports
    path('reports/', views.teacher_reports, name='teacher_reports'),

    # 8. Profile
    path('profile/', views.teacher_profile, name='teacher_profile'),

    # 9. Timetable
    path('timetable/', views.teacher_timetable, name='teacher_timetable'),
]
