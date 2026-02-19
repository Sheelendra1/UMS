"""
URL configuration for ums project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('departments/', include('departments.urls')),
    path('courses/', include('courses.urls')),
    path('notices/', include('notices.urls')),
    path('attendance/', include('attendance.urls')),
    path('examinations/', include('examinations.urls')),
    path('fees/', include('fees.urls')),
    path('timetable/', include('timetable.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'core.views.custom_404'
handler403 = 'core.views.custom_403'
