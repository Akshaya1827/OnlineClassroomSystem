from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:course_id>/', views.create_assignment, name='create_assignment'),
    path('course/<int:course_id>/', views.assignment_list, name='assignment_list'),
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    path(
    'update/<int:assignment_id>/',
    views.update_assignment,
    name='update_assignment'
   ),


    path('assignment/delete/<int:assignment_id>/', 
     views.delete_assignment, 
     name='delete_assignment'),

]
