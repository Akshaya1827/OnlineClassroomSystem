from django import forms
from .models import Course,CourseMaterial

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'subject', 'description']



class JoinCourseForm(forms.Form):
    course_code = forms.CharField(
        max_length=10,
        label="Course Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter course code'
        })
    )


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'file']