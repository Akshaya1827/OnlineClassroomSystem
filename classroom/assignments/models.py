from django.db import models
from django.utils import timezone
from accounts.models import User
from courses.models import Course

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    document = models.FileField(
        upload_to="assignments/",
        blank=True,
        null=True
    )
    due_date = models.DateTimeField(null=True, blank=True)  # optional
    created_at = models.DateTimeField(auto_now_add=True)

    def is_overdue(self):
        if self.due_date:
            return timezone.now() > self.due_date
        return False

    def __str__(self):
        return f"{self.title} - {self.course.name}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)
    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.email} - {self.assignment.title}"
