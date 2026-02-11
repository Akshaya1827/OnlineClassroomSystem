from django import forms
from .models import Assignment, Submission

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
