from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm
from courses.models import Course
from django.utils import timezone


@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role != 'teacher':
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm()

    return render(request, 'assignments/create_assignment.html', {
        'form': form,
        'course': course
    })


@login_required
def assignment_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = Assignment.objects.filter(course=course)

    submissions = None
    if request.user.role == 'student':
        submissions = Submission.objects.filter(student=request.user)

    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments,
        'course': course,
        'submissions': submissions
    })




@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.role != 'student':
        return redirect('teacher_dashboard')

    is_closed = False
    if assignment.due_date and timezone.now() > assignment.due_date:
        is_closed = True

    existing_submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    if request.method == 'POST' and not is_closed:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            if existing_submission:
                existing_submission.file = form.cleaned_data['file']
                existing_submission.save()
                messages.success(request, "Assignment updated successfully!")
            else:
                submission = form.save(commit=False)
                submission.assignment = assignment
                submission.student = request.user
                submission.save()
                messages.success(request, "Assignment submitted successfully!")

            return redirect('student_dashboard')
    else:
        form = SubmissionForm()

    return render(request, 'assignments/submit_assignment.html', {
        'form': form,
        'assignment': assignment,
        'existing_submission': existing_submission,
        'is_closed': is_closed
    })

@login_required
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.role != 'teacher':
        return redirect('student_dashboard')

    submissions = Submission.objects.filter(assignment=assignment)
    total = submissions.count()

    return render(request, 'assignments/view_submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
        'total': total
    })
