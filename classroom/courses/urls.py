from django.urls import path
from . import views

urlpatterns = [
    path('create-course/', views.create_course, name='create_course'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('join-course/', views.join_course, name='join_course'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('course/<int:course_id>/upload/', views.upload_material, name='upload_material'),
    path('course/<int:course_id>/materials/', views.view_materials, name='view_materials'),
    
]
