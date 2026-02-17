from django.db import models
from accounts.models import User
from django.conf import settings
import uuid


class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    course_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.course_code:
            self.course_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Enrollment(models.Model):
     student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
     course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
     joined_at = models.DateTimeField(auto_now_add=True)

     class Meta:
        unique_together = ('student', 'course')
     def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    # file = models.FileField(upload_to='course_materials/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class MaterialFile(models.Model):
    material = models.ForeignKey(
        CourseMaterial,
        on_delete=models.CASCADE,
        related_name="files"
    )
    file = models.FileField(upload_to="course_materials/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.material.title}"
