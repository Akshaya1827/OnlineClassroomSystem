from django.db import models
from courses.models import Course
from accounts.models import User

class Leaderboard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_time = models.DateTimeField()
    rank = models.IntegerField()
