from .models import Course
from assignments.models import Assignment, Submission
from django.utils import timezone

def sidebar_courses(request):
    courses = []
    todos = []

    if request.user.is_authenticated:

        # COURSES
        if request.user.role == "student":
            courses = Course.objects.filter(
                enrollment__student=request.user
            )
        else:
            courses = Course.objects.filter(
                teacher=request.user
            )

        # SUBMITTED ASSIGNMENTS
        submitted_ids = Submission.objects.filter(
            student=request.user
        ).values_list('assignment_id', flat=True)

        # TODOS (ONLY PENDING + NOT EXPIRED)
        todos = Assignment.objects.filter(
            course__in=courses,
            due_date__gte=timezone.now()
        ).exclude(
            id__in=submitted_ids
        ).order_by('due_date')[:5]

    return {
        'courses': courses,
        'todos': todos
    }