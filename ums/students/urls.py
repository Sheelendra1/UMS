from django.urls import path
from . import views

urlpatterns = [
    # ── Admin-facing routes ────────────────────────────
    path('list/', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('add/', views.add_student, name='add_student'),
    path('<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('promote/', views.promote_students, name='promote_students'),

    # ── Student Panel (7 pages) ────────────────────────
    # 0. PDF Result Download
    path('results/download/', views.download_results_pdf, name='download_results_pdf'),

    # 0. PDF ID Card Download
    path('id-card/download/', views.download_id_card_pdf, name='download_id_card_pdf'),
    
    # 0. PDF Fee Receipt Download
    path('fee-receipt/download/<int:payment_id>/', views.download_receipt_pdf, name='download_receipt_pdf'),

    # 1. Dashboard
    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    # 2. My Courses
    path('courses/', views.student_my_courses, name='student_my_courses'),
    path('courses/<int:course_id>/', views.student_course_detail, name='student_course_detail'),

    # 3. My Attendance
    path('attendance/', views.student_my_attendance, name='student_my_attendance'),

    # 4. Timetable
    path('timetable/', views.student_timetable, name='student_timetable'),

    # 5. My Results
    path('results/', views.student_my_results, name='student_my_results'),

    # 6. Fee Status
    path('fees/', views.student_fee_status, name='student_fee_status'),

    # 7. Notices
    path('notices/', views.student_notices, name='student_notices'),

    # 8. Profile
    path('profile/', views.student_profile, name='student_profile'),
]
