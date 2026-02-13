from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from assignments.models import Assignment, Submission
from django.db.models import Sum
from courses.models import Course
@login_required
def leaderboard(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Allow only student and teacher
    if request.user.role not in ['student', 'teacher']:
        return redirect('login')

    # Get all assignments of this course
    assignments = Assignment.objects.filter(course=course)

    # Aggregate total score per student
    leaderboard = (
        Submission.objects
        .filter(assignment__in=assignments)
        .values('student__id', 'student__username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )

    return render(request, 'leaderboard/leaderboard.html', {
        'course': course,
        'leaderboard': leaderboard
    })