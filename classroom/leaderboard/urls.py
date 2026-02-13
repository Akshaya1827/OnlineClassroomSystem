from django.urls import path
from . import views

urlpatterns = [
    path('<int:course_id>/', views.leaderboard, name='leaderboard'),
]
