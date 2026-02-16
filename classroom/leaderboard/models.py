from django.db import models
from courses.models import Course
from accounts.models import User

class Leaderboard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.FloatField()
    rank = models.IntegerField()

    def __str__(self):
        return f"{self.student.email} - {self.rank}"
