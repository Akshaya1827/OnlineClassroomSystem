from django.db import models
from courses.models import Course
from accounts.models import User

class Doubt(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Response(models.Model):
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    replied_at = models.DateTimeField(auto_now_add=True)
