from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from assignments.models import Assignment, Submission
from django.db.models import Sum
from courses.models import Course
from .models import Leaderboard
@login_required
def leaderboard(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role not in ['student', 'teacher']:
        return redirect('login')

    # Delete old leaderboard entries for this course
    Leaderboard.objects.filter(course=course).delete()

    # Aggregate total score per student
    totals = (
        Submission.objects
        .filter(assignment__course=course)
        .values('student__id')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )

    rank = 1
    for entry in totals:
        Leaderboard.objects.create(
            course=course,
            student_id=entry['student__id'],
            total_score=entry['total_score'],
            rank=rank
        )
        rank += 1

    # Fetch stored leaderboard
    leaderboard = Leaderboard.objects.filter(course=course).order_by('rank')

    return render(request, 'leaderboard/leaderboard.html', {
        'course': course,
        'leaderboard': leaderboard
    })
