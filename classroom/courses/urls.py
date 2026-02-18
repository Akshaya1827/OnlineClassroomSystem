from django.urls import path
from . import views

urlpatterns = [
    path('create-course/', views.create_course, name='create_course'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('join-course/', views.join_course, name='join_course'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('course/<int:course_id>/upload/', views.upload_material, name='upload_material'),
    path('course/<int:course_id>/materials/', views.view_materials, name='view_materials'),
     path('update/<int:course_id>/', views.update_course, name='update_course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path("", views.course_list, name="course_list"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path('material/file/delete/<int:file_id>/', views.delete_material_file, name='delete_material_file'),
path('material/file/update/<int:file_id>/', views.update_material_file, name='update_material_file'),

]
