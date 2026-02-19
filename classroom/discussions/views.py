from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course
from .models import DoubtMessage
from courses.models import Enrollment


# Create your views here.
@login_required
def doubt_box(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # STUDENT ACCESS CHECK
    if request.user.role == "student":
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()

        if not is_enrolled:
            return redirect('student_dashboard')

    # TEACHER ACCESS CHECK
    elif request.user != course.teacher:
        return redirect('teacher_dashboard')

    messages = DoubtMessage.objects.filter(course=course).order_by('timestamp')

    if request.method == "POST":
        text = request.POST.get('message')

        if text:
            DoubtMessage.objects.create(
                course=course,
                sender=request.user,
                message=text
            )

        return redirect('doubt_box', course_id=course.id)

    return render(request, 'doubts/doubt_box.html', {
        'course': course,
        'messages': messages
    })