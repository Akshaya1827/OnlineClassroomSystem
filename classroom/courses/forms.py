from django import forms
from .models import Course,CourseMaterial, MaterialFile

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
        fields = ['title', 'description']



def clean_file(self):
    file = self.cleaned_data.get('file')

    if file:
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        if file.size > 5*1024*1024:
            raise forms.ValidationError("File size must be under 5MB.")
    return file