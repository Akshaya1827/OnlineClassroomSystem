from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from accounts.models import User
User = get_user_model()

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

class DoubtMessage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chat_messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.course.name}"