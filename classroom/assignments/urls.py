from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:course_id>/', views.create_assignment, name='create_assignment'),
    path('course/<int:course_id>/', views.assignment_list, name='assignment_list'),
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),

]
